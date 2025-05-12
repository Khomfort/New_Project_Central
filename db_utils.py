import streamlit as st
import pyodbc

def connect_db():
    try:
        server = 'DESKTOP-842C8KP\\SQLEXPRESS'  # <---  **CHANGE THIS**
        database = "WIP_CentralDB"
        driver = '{ODBC Driver 17 for SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        st.error(f"Error connecting to SQL Server: {sqlstate}")
        return None

def test_db_connection():
    st.title("DB Connection Test")
    conn = connect_db()
    if conn:
        st.success("Successfully connected to the WIP_CentralDB database on SQL Server!")
        conn.close()
    else:
        st.error("Failed to connect to the SQL Server database.")

if __name__ == "__main__":
    test_db_connection()