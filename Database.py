import mysql.connector

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Michael2001",
    database="object_detection"
)

cursor = db.cursor()