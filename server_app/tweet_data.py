import csv

class TweetData:

    def __init__(self):
        self.tweet_count = 0
        self.ids = []
        self.dates = dict()
        self.polarity = dict()
        self.subjectivity = dict()
        self.place_by_day = dict()
        self.place = dict()
        self.topic = dict()
        
        #for x in range(1, 16):
        count = 0
        with open('server_app/assets/training_data.csv', 'r+', encoding="utf8") as file:
                reader = csv.reader((x.replace('\0', '') for x in file), delimiter='␟')
                headers = next(reader)
                for row in reader:
                    count += 1
                    if row[0] in self.ids:
                        continue
                    
                    if len(row) < 11:
                        continue
                    
                    self.tweet_count += 1
                    self.ids.append(row[0])                   
                    
                    self.dates[row[2]] = self.dates.get(row[2], 0) + 1
                    self.polarity[row[2]] = self.polarity.get(row[2], 0) + float(row[8])
                    self.subjectivity[row[2]] = self.subjectivity.get(row[2], 0) + float(row[9])
                    
                    self.place[row[4]] = self.place.get(row[4], 0) + 1
                    
                    self.topic[row[10]] = self.topic.get(row[10], 0) + 1
                    
                    _places = self.place_by_day.get(row[2], dict())
                    _places[row[4]] = _places.get(row[4], 0) + 1
                    self.place_by_day[row[2]] = _places
                    
        for item in self.polarity:
            self.polarity[item] = self.polarity.get(item) / self.dates.get(item)
            
        for item in self.subjectivity:
            self.subjectivity[item] = self.subjectivity.get(item) / self.dates.get(item)
        
        with open('client_app/static/data/location_data.csv', 'w+', encoding="utf8") as f:
            f.write("name,number" + '\n')
            for item in self.place:
                clean_data = item
                if clean_data == "United States":
                    clean_data = "United States of America"
                
                f.write(clean_data + "," + str(self.place.get(clean_data)) + '\n')
                
        print(str(self.tweet_count) + " / " +  str(count))