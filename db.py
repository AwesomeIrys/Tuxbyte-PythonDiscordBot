import mysql.connector
import os

# Function to create a new DB connection and return it along with a cursor
def get_db_cursor():
    db = mysql.connector.connect(
        host="localhost",
        user="",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database=""  # Replace with your database name
    )
    cursor = db.cursor()
    return db, cursor

# Function to close the DB connection
def close_db_connection(db, cursor):
    cursor.close()
    db.close()
