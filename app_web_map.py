import folium
import pandas

data = pandas.read_csv('Volcanoes_USA.txt')
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])

def icon_color(elevation):
	if elevation <= 2000:
		return 'green'

	elif 2000 < elevation <= 3000:
		return 'purple'

	else:
		return 'red'

map = folium.Map(location = [38, -99], zoom_start = 4, tiles = 'Mapbox Bright')

fgV = folium.FeatureGroup(name = 'Volcanoes USA')

for lt, ln, el in zip(lat, lon, elev):
	fgV.add_child(folium.CircleMarker(location = [lt, ln], popup = str(el) + ' m', radius=6, color = icon_color(el), fill = True, fill_opacity = 0.75, fill_color = icon_color(el)))

fgP = folium.FeatureGroup(name = 'World Population')

fgP.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(), 
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 30000000
else 'purple' if 30000000 <= x['properties']['POP2005'] < 50000000
else 'red'}))

map.add_child(fgV)
map.add_child(fgP)
map.add_child(folium.LayerControl())

map.save("WebMap.html")