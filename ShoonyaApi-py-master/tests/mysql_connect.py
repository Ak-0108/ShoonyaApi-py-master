import mysql.connector

try:
    # Establish the connection
    mydb = mysql.connector.connect(
        host="208.109.224.68",  # Or the IP address/hostname of your MySQL server
        user="maa",
        password="Radhe@123@1",
        database="mstockdb" # Optional: specify a database to connect to directly
    )

    print("Connection to MySQL successful!")

    # You can now create a cursor object to execute SQL queries
    mycursor = mydb.cursor()

    # Example: Execute a query
    mycursor.execute("SELECT VERSION()")
    result = mycursor.fetchone()
    print(f"MySQL Version: {result[0]}")

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")

finally:
    # Close the cursor and connection to release resources
    if 'mycursor' in locals() and mycursor is not None:
        mycursor.close()
    if 'mydb' in locals() and mydb.is_connected():
        mydb.close()
        print("MySQL connection closed.")