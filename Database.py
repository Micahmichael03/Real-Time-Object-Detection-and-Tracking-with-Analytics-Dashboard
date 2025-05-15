import mysql.connector

# MySQL connection
db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

cursor = db.cursor()