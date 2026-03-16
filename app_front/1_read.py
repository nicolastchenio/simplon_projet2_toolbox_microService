"""
Streamlit page for reading stored data.

This page retrieves data from the FastAPI backend using an HTTP GET
request. The returned data is displayed in the Streamlit interface,
typically in a table format.

Main responsibilities:
- Call the API endpoint to retrieve stored records
- Convert the response to a dataframe if necessary
- Display the data to the user
"""