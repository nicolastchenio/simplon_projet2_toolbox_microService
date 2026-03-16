"""
Database connection management.

This module is responsible for configuring and creating the connection
to the database using SQLAlchemy.

It defines:
- the database engine
- the session factory
- utilities used by the API to interact with the database

During development, the database may be SQLite. In production,
the configuration can be switched to PostgreSQL.
"""