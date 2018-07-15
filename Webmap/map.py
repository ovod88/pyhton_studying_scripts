import folium
import pandas

data = pandas.read_csv("Volcanoes_USA.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
el = list(data["ELEV"])

map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Mapbox Bright")

def color(elevation):
	if elevation < 1000:
		return "green"
	elif 1000 <= elevation < 3000:
		return "orange"
	else:
		return "red"

fgv=folium.FeatureGroup(name="Volcanoes")

for lt,ln, el in zip(lat, lon, el):
	fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(str(el)+ ' m', parse_html=True), 
								fill_color=color(el), color='grey', fill_opacity=0.7, fill=True))

fgp=folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
							style_function=lambda x: {'fillColor': "green" if x["properties"]["POP2005"] < 10000000
							else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save('Map.html')
