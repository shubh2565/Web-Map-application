import folium
import pandas

data = pandas.read_csv('Volcanoes_USA.txt')  # creates a dataframe
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])


# function to give assign colors to the markers on the basis of elevation 
def icon_color(elevation):
	if elevation <= 2000:
		return 'green'

	elif 2000 < elevation <= 3000:
		return 'purple'

	else:
		return 'red'

map = folium.Map(location = [38, -99], zoom_start = 4, tiles = 'Mapbox Bright')  # creates a map object 

fgV = folium.FeatureGroup(name = 'Volcanoes USA') # creates a feature group. We can add child directly to map object but this is more refined way.

for lt, ln, el in zip(lat, lon, elev):     # zip is used when simultaneously iterating through more than one list
	fgV.add_child(folium.CircleMarker(location = [lt, ln], popup = str(el) + ' m', radius=6, color = icon_color(el), fill = True, fill_opacity = 0.75, fill_color = icon_color(el)))

fgP = folium.FeatureGroup(name = 'World Population')  # another feature group

fgP.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(), 
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000    # lamda method is used to assign different colors to different population range
else 'orange' if 10000000 <= x['properties']['POP2005'] < 30000000
else 'purple' if 30000000 <= x['properties']['POP2005'] < 50000000
else 'red'}))

map.add_child(fgV)
map.add_child(fgP)
map.add_child(folium.LayerControl()) 

map.save("WebMap.html")
