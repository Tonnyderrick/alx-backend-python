import mysql.connector

def stream_users():
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',  # Replace with your actual MySQL root password
        database='ALX_prodev'
    )

    cursor = connection.cursor(dictionary=True)  # Automatically return rows as dictionaries

    # Execute the query
    cursor.execute("SELECT * FROM user_data")

    # Yield one row at a time
    for row in cursor:
        yield row

    # Clean up
    cursor.close()
    connection.close()
