"""
Streamlit page for inserting data.

This page provides a user interface that allows users to submit data
to the FastAPI backend. The data entered by the user is sent through
an HTTP POST request to the API endpoint.

The API then processes the request and stores the information in the
database.

Main responsibilities:
- Collect user input through Streamlit widgets
- Send a POST request to the FastAPI API
- Display confirmation or error messages
"""