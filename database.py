import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="flask_user",
        password="1234",
        database="cloud_attendance"
    )

    return connection