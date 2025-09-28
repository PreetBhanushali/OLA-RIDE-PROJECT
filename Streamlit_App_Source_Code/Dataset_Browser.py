import streamlit as st
import pandas as pd


def app():
    # File paths (update if needed)
    st.title("Dataset Browser")
    
    DATASETS = {
        "Booking Status": "CSV FILES/Booking_status.csv",
        "Locations": "CSV FILES/Locations.csv",
        "Ola Cleaned Dataset": "CSV FILES/Ola_cleaned_dataset.csv",
        "Vehicle Types": "CSV FILES/Vehicle_types.csv",
        "Payment Methods": "CSV FILES/Payment_methods.csv"
    }

    st.title("📊 Ola Datasets Browser")

    # Selectbox for dataset choice
    dataset_choice = st.selectbox("Select a dataset to browse:", list(DATASETS.keys()))

    # Load selected dataset
    if dataset_choice:
        file_path = DATASETS[dataset_choice]
        try:
            df = pd.read_csv(file_path)

            st.subheader(f"Showing: {dataset_choice}")
            st.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")

            # --- Search/Filter Section ---
            with st.expander("🔍 Filter / Search Options"):
                # Free text search across all columns
                search_text = st.text_input("Search text:")
                if search_text:
                    df = df[df.astype(str).apply(
                        lambda x: x.str.contains(search_text, case=False, na=False)
                    ).any(axis=1)]

                # Column-based filters
                filter_cols = st.multiselect("Select columns to filter by:", df.columns.tolist())
                for col in filter_cols:
                    if df[col].dtype == "object":
                        options = df[col].dropna().unique().tolist()
                        selected = st.multiselect(f"Filter {col}:", options)
                        if selected:
                            df = df[df[col].isin(selected)]
                    else:
                        min_val, max_val = float(df[col].min()), float(df[col].max())
                        selected_range = st.slider(
                            f"Filter {col}:", min_val, max_val, (min_val, max_val)
                        )
                        df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]

            # Show filtered dataframe
            st.dataframe(df, use_container_width=True)

            # Optional: summary stats
            with st.expander("📈 Show Summary Statistics"):
                st.write(df.describe(include="all"))

            # --- Download button for filtered data ---
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download this dataset as CSV",
                data=csv,
                file_name=f"{dataset_choice.replace(' ', '_').lower()}_filtered.csv",
                mime="text/csv"
            )

        except FileNotFoundError:
            st.error(f"❌ File not found: {file_path}. Please make sure it exists.")

# Run the app if file executed directly
if __name__ == "__main__":
    app()

