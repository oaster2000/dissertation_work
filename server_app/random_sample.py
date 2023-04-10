from pattern.text.en import sentiment
from geopy.geocoders import Nominatim
import mysql.connector
import re, html
import googletrans.client
import csv

database = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="password",
    database="socialmediainfovis"
)
translator = googletrans.client.Translator()
cursor = database.cursor()
geolocator = Nominatim(user_agent="dissertation-work", timeout=3)

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

def clean(data):
    text = data[1]

    if data[2] != "English":
        text = translate(text)

    result = clean_data(text)
    return result

def location(data):     
    location = geolocator.geocode(data[4], language='en')
    country = ""
    if location != None:
        loc_dict = location.raw

        country = loc_dict['display_name'].rsplit(',' , 1)
    
        if len(country) > 1:
            country = country[1]
        else:
            country = country[0]
        
    country = country.lstrip()
    if country == "United States":
            country = "United States of America"
    return country
    
for x in range(10, 16):
    sql = "SELECT * FROM tweets WHERE NOT location = 'No Geo Data' ORDER BY RAND() LIMIT 10000;"
    cursor.execute(sql)

    results = cursor.fetchall()
    
    i = 0

    with open('assets/random_sample_' + str(x) +'.csv', 'w+', encoding="utf8") as f:
        field_names = [i[0] for i in cursor.description]
        for x in range(0, len(field_names)):
            f.write(field_names[x] + '␟')
        
        f.write("topics" + '\n')
                    
        for result in results:
            text = clean(result)
            place = location(result)
            val = (result[0], text, result[2], result[3], place, result[5], result[6], result[7], sentiment(text)[0], sentiment(text)[1])
            if place == "United States of America":
                if i % 5 != 0:
                    i += 1
                    continue
            
            for x in range(0, len(val)):
                if x == len(val) - 1:
                    f.write(str(val[x]) + '\n')
                else:
                    f.write(str(val[x]) + '␟')
            i += 1