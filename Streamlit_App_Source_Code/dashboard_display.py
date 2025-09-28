import streamlit as st

def app():

    st.title("Power BI Dashboard in Streamlit")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiZDQ3YjZmMDgtYWJmYi00NWIxLTgzNGMtMDg4NTJmYTkyMTk4IiwidCI6IjQ4NWQ4NmNkLTZmN2YtNDYxZC04ZTdlLTc5MzZkMDlhOTE5ZCJ9"

    st.components.v1.iframe(powerbi_url, width=1200, height=800)






