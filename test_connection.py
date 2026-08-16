from database.connection import get_connection

try:

    connection = get_connection()

    print("Connected Successfully!")

    connection.close()

except Exception as e:

    print(e)