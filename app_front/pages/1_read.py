"""Streamlit page used to display stored operations.

This page retrieves all mathematical operations stored in the
database by calling the FastAPI backend API.

The retrieved data is displayed in a tabular format using
a pandas DataFrame.
"""

import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/operations/"

st.title("Stored Mathematical Operations")

if st.button("Load operations"):
    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            data = response.json()

            if len(data) == 0:
                st.warning("No operations found in the database.")
            else:
                df = pd.DataFrame(data)
                st.dataframe(df)

        else:
            st.error("Error while retrieving operations.")

    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the API. Make sure FastAPI is running.")
