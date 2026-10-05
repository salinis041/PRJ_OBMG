import os
import pyodbc


def get_connection():
    """
    Connection to the application's database.
    """
    connection_string = os.getenv(
        "OBMG_PORTAL_DB_CONNECTION"
    )

    if not connection_string:
        raise RuntimeError(
            "OBMG_PORTAL_DB_CONNECTION environment variable is not set."
        )

    return pyodbc.connect(connection_string)


def get_remote_connection():
    """
    Connection to the remote/source database.
    """
    connection_string = os.getenv(
        "REMOTE_DB_CONNECTION"
    )

    if not connection_string:
        raise RuntimeError(
            "REMOTE_DB_CONNECTION environment variable is not set."
        )

    return pyodbc.connect(connection_string)