from geopy.geocoders import Nominatim
import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="password",
    database="socialmediainfovis"
)
cursor = database.cursor()
geolocator = Nominatim(user_agent="dissertation-work", timeout=3)

sql = "SELECT id, location FROM socialmediainfovis.tweets WHERE NOT location = 'No Geo Data'"
cursor.execute(sql)

results = cursor.fetchall()

max_count = len(results)
count = max_count

for result in results:
    count -= 1
    if count >= 568398:
        continue
    print(str(count) + "/" + str(max_count) + " tweets remaining.")
    
    if result[1] == "No Geo Data":
        continue
     
    location = geolocator.geocode(result[1], language='en')
    country = ""
    if location != None:
        loc_dict = location.raw

        country = loc_dict['display_name'].rsplit(',' , 1)
    
        if len(country) > 1:
            country = country[1]
        else:
            country = country[0]
    else:
        country = "No Geo Data"
        
    country = country.lstrip()

    sql_update = "UPDATE tweets SET location=%s WHERE id=%s"
    val = (country, result[0])
    cursor.execute(sql_update, val)
    database.commit()     