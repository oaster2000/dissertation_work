import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="password",
    database="socialmediainfovis"
)

mycursor = database.cursor()

mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), description VARCHAR(255), followercount INT(10), followingcount INT(10))")