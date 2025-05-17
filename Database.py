import mysql.connector

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="put/your/password/here",
    database="object_detection"
)

cursor = db.cursor()
