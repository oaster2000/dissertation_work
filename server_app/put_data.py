import json, random
from langcodes import *
import mysql.connector
from datetime import datetime
from pattern.text.en import sentiment
import re
import html
import googletrans.client

database = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="password",
    database="socialmediainfovis"
)

count = 0
cursor = database.cursor(buffered=True)
sql = "SELECT id FROM users WHERE id = %s"
sql_user = "REPLACE INTO users (id, username, description, followercount, followingcount) VALUES (%s, %s, %s, %s, %s)"
sql_tweet = "REPLACE INTO tweets (id, tweet_content, date, time, location, lang, retweets, user_id, polarity, subjectivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

translator = googletrans.client.Translator()

def clean_data(data):
    out_data = re.sub('\n', '', data)
    
    user_handles = re.compile('@(\s)?[A-Za-z0-9]+(\s)*')
    out_data = user_handles.sub('', out_data)
    
    links = re.compile('(https:\/\/t.co\/)[A-Za-z0-9]+(\s)*')
    out_data = links.sub('', out_data)
    
    out_data = html.unescape(out_data)
    
    return out_data

def translate(text):
    text = translator.translate(text).text
    return text

for i in range(1, 36):
    count = 0
    with open('assets/hydrated/tweet_ids_' + str(i) + '.jsonl', encoding="utf8") as f:
        for line in f:
            try:
                data = json.loads(line)
            except Exception as e:
                continue
            count += 1
            
            user_id = (data['user']['id'],)
            cursor.execute(sql, user_id)
            result = cursor.rowcount
            if result == 0:
                val = (data['user']['id'], data['user']['screen_name'], data['user']['description'], data['user']['followers_count'], data['user']['friends_count'])
                cursor.execute(sql_user, val)
            
            place = "No Geo Data"
            if data['place'] != None:
                place = data['place']['name']
            date = datetime.strftime(datetime.strptime(data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d')
            time = datetime.strftime(datetime.strptime(data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%H:%M:%S')
            language = Language.get(data['lang']).display_name()
            text = data['full_text']
            if language != "English":
                text = translate(text)
            clean_text = clean_data(text)
            val = (data['id'], text, date, time, place, language, data['retweet_count'], data['user']['id'], sentiment(clean_text)[0], sentiment(clean_text)[1])
            cursor.execute(sql_tweet, val)

            database.commit()
            if count % 10000 == 0:
                print(count, "records inserted from file " + str(i) + ".")
            
    print(count, "records inserted. File " + str(i) + " completed")
        