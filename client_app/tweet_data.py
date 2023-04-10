import requests, json

class TweetData:

    URL = "http://127.0.0.1:5000"

    def __init__(self):
        self.tweet_count = 0
        self.dates = dict()
        self.polarity = dict()
        self.subjectivity = dict()
        self.place_by_day = dict()
        self.place = dict()
        self.topic = dict()
        
        response = requests.get(url = self.URL + "/date")
        self.dates = response.json()
        
        response = requests.get(url = self.URL + "/sentiment/polarity")
        self.polarity = response.json()
        
        response = requests.get(url = self.URL + "/sentiment/subjectivity")
        self.subjectivity = response.json()
        
        response = requests.get(url = self.URL + "/topic")
        self.topic = response.json()
        
        response = requests.get(url = self.URL + "/place")
        self.place = response.json()
            
    def getDateLabels(self):
        labels = []
        for item in self.dates:
            labels.append(item)
        return labels
            
            
    def getDateValues(self):
        values = []
        for item in self.dates:       
            values.append(self.dates[item])
        return values 
    
    def getTopicLabels(self):
        labels = []
        for item in self.topic:
            labels.append(item)
        return labels
            
            
    def getTopicValues(self):
        values = []
        for item in self.topic:       
            values.append(self.topic[item])
        return values 
            
    
data = TweetData()