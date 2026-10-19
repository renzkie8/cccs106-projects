# src/db_connection.py
import mysql.connector
from mysql.connector import Error

def connect_db():
    """
    Creates and returns a MySQL connection object.
    
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fletapp"
        )
        return conn
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
