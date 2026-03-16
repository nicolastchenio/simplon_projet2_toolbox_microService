"""
Streamlit frontend entry point.

This module launches the Streamlit application and provides the main
interface for users to interact with the system.

The frontend communicates with the FastAPI backend through HTTP
requests to send and retrieve data.

Main responsibilities:
- Initialize the Streamlit application
- Provide navigation between pages
- Serve as the starting point for the user interface

The application is structured using multiple pages:
- 0_insert.py : page used to submit new data to the API
- 1_read.py   : page used to display stored data retrieved from the API
"""
