import os
import pyodbc


def get_connection():
    connection_string = os.getenv("OBMG_PORTAL_DB_CONNECTION")

    if not connection_string:
        raise RuntimeError(
            "OBMG_PORTAL_DB_CONNECTION environment variable is not set."
        )

    return pyodbc.connect(connection_string)