import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

DB_NAME = "ALX_prodev"

TABLES = {
    "user_data": (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "  user_id CHAR(36) NOT NULL PRIMARY KEY,"
        "  name VARCHAR(255) NOT NULL,"
        "  email VARCHAR(255) NOT NULL,"
        "  age DECIMAL NOT NULL,"
        "  INDEX(user_id)"
        ") ENGINE=InnoDB"
    )
}

def connect_db():
    """Connects to the MySQL server"""
    try:
        return mysql.connector.connect(user='root', password='your_password')
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        return mysql.connector.connect(user='root', password='your_password', database=DB_NAME)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Creates user_data table"""
    cursor = connection.cursor()
    try:
        cursor.execute(TABLES["user_data"])
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def insert_data(connection, filename):
    """Insert data from CSV into user_data table if not already present"""
    cursor = connection.cursor()
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute(
                    "SELECT COUNT(*) FROM user_data WHERE email = %s", (row["email"],)
                )
                if cursor.fetchone()[0] == 0:
                    user_id = str(uuid.uuid4())
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, row["name"], row["email"], row["age"]),
                    )
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
