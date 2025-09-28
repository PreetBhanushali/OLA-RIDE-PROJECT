import streamlit as st
import Sql_Explorer,Dataset_Browser,dashboard_display

# Define the pages in a dictionary
pages = {
    "Sql Explorer": Sql_Explorer,
    "Dataset Browser": Dataset_Browser,
    "Dashboard Display": dashboard_display
}
# Add a sidebar for navigation
st.sidebar.title("OLA RIDE Dashboard")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Run the selected page
pages[selection].app()
