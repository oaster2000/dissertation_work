from flask import Flask, jsonify, request, render_template_string
import pandas as pd
import geopandas as gpd

from tweet_data import TweetData
        
class ServerApp(Flask):
  url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
  tweet_data = TweetData()
  
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    super(ServerApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = ServerApp(__name__)

@app.route("/")
def index():
    return render_template_string("Server Active")

@app.route("/date", methods=['GET'])
def date():
    return jsonify(app.tweet_data.dates)
  
@app.route("/sentiment/polarity", methods=['GET'])
def polarity():
    return jsonify(app.tweet_data.polarity)

@app.route("/sentiment/subjectivity", methods=['GET'])
def subjectivity():
    return jsonify(app.tweet_data.subjectivity)
  
@app.route("/topic", methods=['GET'])
def topic():
    return jsonify(app.tweet_data.topic)
  
@app.route("/place", methods=['GET'])
def place():
    return jsonify(app.tweet_data.place)

if __name__ == '__main__':
        app.run(host="0.0.0.0", debug=True, use_reloader=False)