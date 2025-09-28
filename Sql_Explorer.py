import streamlit as st
import sqlite3
import pandas as pd
import re

st.title("OLA Ride SQL Explorer")

def app():
    DB_PATH = "Sql Folder\OLA Ride Database.db"
    SQL_FILE = "Sql Folder\OLA RIDE Sql Analysis.sql"

    def load_queries(sql_file):
        """Parse SQL file and return dict {title: query}."""
        with open(sql_file, "r") as f:
            content = f.read()
        queries = {}
        parts = re.split(r"--\s*\d+\.\s*", content)
        for part in parts[1:]:
            lines = part.strip().splitlines()
            if not lines:
                continue
            title = lines[0].strip()
            query = "\n".join(lines[1:]).strip()
            if title and query:
                queries[title] = query
        return queries

    def apply_filters(query, filters, maps):
        """Inject filters into SQL WHERE clause safely using IDs."""
        conditions = []

        if filters["day_name"]:
            conditions.append(f"o.day_name = '{filters['day_name']}'")
        if filters["date"]:
            conditions.append(f"o.date = {filters['date']}")
        if filters["hour"]:
            conditions.append(f"o.hour = {filters['hour']}")
        if filters["vehicle_type"]:
            vt_id = maps["vehicle_type"].get(filters["vehicle_type"])
            if vt_id:
                conditions.append(f"o.vehicle_type_id = '{vt_id}'")
        if filters["status"]:
            st_id = maps["status"].get(filters["status"])
            if st_id:
                conditions.append(f"o.status_id = '{st_id}'")
        if filters["part_of_day"]:
            conditions.append(f"o.part_of_day = '{filters['part_of_day']}'")
        if filters["payment_method"]:
            pm_id = maps["payment_method"].get(filters["payment_method"])
            if pm_id:
                conditions.append(f"o.payment_method_id = {pm_id}")

        if not conditions:
            return query  # nothing to add

        lower_q = query.lower()

        # Find start of GROUP BY / ORDER BY / LIMIT
        split_keywords = ["group by", "order by", "limit"]
        split_pos = len(query)
        for kw in split_keywords:
            pos = lower_q.find(kw)
            if pos != -1 and pos < split_pos:
                split_pos = pos

        main_query = query[:split_pos].strip()
        trailing = query[split_pos:].strip()

        # If WHERE exists already, append with AND
        if "where" in lower_q:
            main_query += " AND " + " AND ".join(conditions)
        else:
            main_query += " WHERE " + " AND ".join(conditions)

        return f"{main_query} {trailing}".strip()

    # Connect once to fetch filter values + mappings
    conn = sqlite3.connect(DB_PATH)

    # Get dropdown values
    day_name_list = [""] + pd.read_sql("SELECT DISTINCT day_name FROM ola", conn)["day_name"].dropna().tolist()
    date_list = [""] + pd.read_sql("SELECT DISTINCT date FROM ola ORDER BY date", conn)["date"].dropna().tolist()
    hour_list = [""] + pd.read_sql("SELECT DISTINCT hour FROM ola ORDER BY hour", conn)["hour"].dropna().tolist()
    part_of_day_list = [""] + pd.read_sql("SELECT DISTINCT part_of_day FROM ola", conn)["part_of_day"].dropna().tolist()

    vehicle_types_df = pd.read_sql("SELECT vehicle_type_id, vehicle_type FROM vehicle_types", conn)
    booking_status_df = pd.read_sql("SELECT status_id, status FROM booking_status", conn)
    payment_methods_df = pd.read_sql("SELECT payment_method_id, payment_method FROM payment_methods", conn)

    conn.close()

    # Create mapping dictionaries
    vehicle_type_map = dict(zip(vehicle_types_df["vehicle_type"], vehicle_types_df["vehicle_type_id"]))
    booking_status_map = dict(zip(booking_status_df["status"], booking_status_df["status_id"]))
    payment_method_map = dict(zip(payment_methods_df["payment_method"], payment_methods_df["payment_method_id"]))

    maps = {
        "vehicle_type": vehicle_type_map,
        "status": booking_status_map,
        "payment_method": payment_method_map
    }

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    day_name = st.sidebar.selectbox("Day Name", day_name_list)
    date_val = st.sidebar.selectbox("Date", date_list)
    hour = st.sidebar.selectbox("Hour", hour_list)
    vehicle_type = st.sidebar.selectbox("Vehicle Type", [""] + list(vehicle_type_map.keys()))
    status = st.sidebar.selectbox("Booking Status", [""] + list(booking_status_map.keys()))
    part_of_day = st.sidebar.selectbox("Part of Day", part_of_day_list)
    payment_method = st.sidebar.selectbox("Payment Method", [""] + list(payment_method_map.keys()))

    filters = {
        "day_name": day_name,
        "date": date_val if date_val != "" else None,
        "hour": hour if hour != "" else None,
        "vehicle_type": vehicle_type,
        "status": status,
        "part_of_day": part_of_day,
        "payment_method": payment_method,
    }

    st.title("🚖 OLA Ride Database - SQL Query Explorer")

    # Load queries
    queries = load_queries(SQL_FILE)
    query_titles = list(queries.keys())

    # Select query
    selected_query_title = st.selectbox("Select a Query", query_titles)
    base_query = queries[selected_query_title]

    # Apply filters with ID optimization
    filtered_query = apply_filters(base_query, filters, maps)

    # Show query
    st.subheader("📝 SQL Query to Execute")
    st.code(filtered_query, language="sql")

    # Execute button
    if st.button("▶️ Execute Query"):
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query(filtered_query, conn)
            conn.close()

            st.success(f"✅ Query executed successfully. {df.shape[0]} rows returned.")
            st.dataframe(df, use_container_width=True)

            # Download button
            if not df.empty:
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Results as CSV",
                    data=csv,
                    file_name=f"{selected_query_title.replace(' ', '_').lower()}_results.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"❌ Error executing query: {e}")

# Run the app if executed directly
if __name__ == "__main__":
    app()
