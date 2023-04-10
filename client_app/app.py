from flask import Flask, render_template
import folium
import pandas as pd
import geopandas as gpd

from tweet_data import TweetData
        
class ClientApp(Flask):
  url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
  tweet_data = TweetData()
  geo_data = pd.read_csv('client_app/static/data/location_data.csv', index_col=None, header=0)
  country_geo = f'{url}/world-countries.json'
  country_df = gpd.read_file(country_geo, driver='GeoJSON')
  geo_df = country_df.merge(geo_data, on="name")
  
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    super(ClientApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = ClientApp(__name__)

@app.route("/")
def index():
        f = folium.Figure(width=1000, height=500)
        m = folium.Map(location= [45, 38], 
                tiles='openstreetmap',
                zoom_start=3, 
                min_zoom = 3,
                max_bounds = True,
                zoom_control=False
        ).add_to(f)
        
        folium.Choropleth(
          geo_data=app.country_geo,
          name="tweets",
          data=app.geo_data,
          columns=["name", "number"],
          key_on="feature.properties.name",
          fill_color="BuPu",
          fill_opacity=0.75,
          line_opacity=0.75,
          legend_name="Number of Tweets",
          bins=8,
          reset=True
        ).add_to(m)
        
        style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#0000cc', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.50, 
                                        'weight': 0.1}
        NIL = folium.features.GeoJson(
          data=app.geo_df,
          style_function=style_function, 
          control=False,
          highlight_function=highlight_function, 
          tooltip=folium.features.GeoJsonTooltip(
                fields=['name','number'],
                aliases=['Country','Tweets'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
          ),
          zoom_on_click=True
        )
        m.add_child(NIL)
        m.keep_in_front(NIL)
        
        labels = app.tweet_data.getDateLabels()
        values = app.tweet_data.getDateValues()
        
        topic_lables = app.tweet_data.getTopicLabels()
        topic_values = app.tweet_data.getTopicValues()

        # set the iframe width and height
        m.get_root().width = "100%"
        m.get_root().height = "720px"
        map = f.get_root()._repr_html_()

        return render_template("dashboard.html", map=map, date_labels=labels, date_values=values, topic_lables=topic_lables, topic_values=topic_values)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=12345)