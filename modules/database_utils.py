# modules/database_utils.py
import sqlite3

def connect_to_db(db_path):
    """ Connect to the SQLite database. """
    return sqlite3.connect(db_path)

def execute_query(conn, query):
    """ Execute a SQL query and return the results. """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def get_table_preview(conn, table_name):
    """ Get the first three rows from a table to include in the prompt. """
    return execute_query(conn, f"SELECT * FROM {table_name} LIMIT 3")
