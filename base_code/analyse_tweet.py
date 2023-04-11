from pattern.text.en import sentiment
import mysql.connector
import re
import html
import googletrans.client

database = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="password",
    database="socialmediainfovis"
)
translator = googletrans.client.Translator()
cursor = database.cursor()


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

count = 0
sql = "SELECT id, tweet_content, lang FROM socialmediainfovis.tweets"
cursor.execute(sql)

results = cursor.fetchall()

max_count = len(results)
count = max_count

for result in results:
    count -= 1
    print(str(count) + "/" + str(max_count) + " tweets remaining.")
    text = result[1]

    if result[2] != "English":
        text = translate(text)

    data = clean_data(text)
    sql_update = "UPDATE tweets SET polarity=%s, subjectivity=%s WHERE id=%s"
    val = (sentiment(data)[0], sentiment(data)[1], result[0])
    cursor.execute(sql_update, val)

    database.commit()
    print(count, "records inserted.")
