import json, random
from langcodes import *
import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="password",
    database="socialmediainfovis"
)

count = 0
cursor = database.cursor(buffered=True)
sql = "REPLACE INTO users (id, username, description, followercount, followingcount) VALUES (%s, %s, %s, %s, %s)"

for i in range(25, 35):
    count = 0
    line_count = 0
    with open('assets/hydrated/tweet_ids_' + str(i) + '.jsonl', encoding="utf8") as f:
        for line in f:
            line_count += 1
            try:
                data = json.loads(line)
            except Exception as e:
                continue
            place = "No Geo Data"
            if data['place'] != None:
                place = data['place']['name']
            

            val = (data['user']['id'], data['user']['screen_name'], data['user']['description'], data['user']['followers_count'], data['user']['friends_count'])
            try:
                cursor.execute(sql, val)
            except Exception as e:
                continue

            count += 1
            database.commit()

    print(count, "records inserted. File " + str(i) + " completed")