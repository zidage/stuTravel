import json
from urllib import response
import requests
import time
import osmnx as ox
import matplotlib.pyplot as plt
import os


google_api_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&language=zh-CN&key={API_KEY}'
input_file_path = ['map_data/catagory/china_university.json', 'map_data/catagory/world_university.json']
amenities = ["restaurant", "cafe", "library", "hospital",
        	"cinema", "bar", "bus_station", 
			"parking", "police", "bicycle_parking", 
			"food_court", "toilets"]

for input_path in input_file_path:
	with open(input_path, 'r', encoding='utf-8') as input_file:
		university_list = json.load(input_file)
		
		for university in university_list:
			query = university
			query_formal_name = query.replace(' ', '_')
			geojson_features_path = 'map_data/university_map/{query}/{query}_{feature}.geojson'
			csv_features_path = 'map_data/university_map/{query}/{query}_{feature}.csv'
			
			try:
				if not os.path.exists(f'map_data/university_map/{query}'):
					os.makedirs(f'map_data/university_map/{query_formal_name}')
				else:
					continue
				response = requests.get(google_api_url.format(query=query, API_KEY='AIzaSyAa2ZdkUiY7jLWkZJABgUtKMwEdHQA1pvU'))
				assert(response.status_code == 200)
				result = response.json()['results'][0]
				data = {'name': result['name'], 'address': result['formatted_address'], 
						'formatted_address': result['plus_code']['compound_code'].replace(' ', '_'),
						'rating': result['rating']}
				data_with_parent = {'university': data}
				with open(f'map_data/university_map/{query_formal_name}/{query_formal_name}_info.json', 'w', encoding='gb2312') as f:
					json.dump(data_with_parent, f, indent=4, ensure_ascii=False)
					print(f'Basic info of {query} has been found and stored at map_data/university_map/{query}/{query_formal_name}_info.json')
			except:
				# time.sleep(1)
				print(f"{query} does not exits\n")
				continue
			try:
				graph = ox.graph_from_place(query)
				nodes, edges = ox.graph_to_gdfs(graph)
				nodes.to_csv(csv_features_path.format(query=query_formal_name, feature='nodes'))
				edges.to_csv(csv_features_path.format(query=query_formal_name, feature='edges'))
				print(f"Nodes and Edges for {query} have been found and were stored at {geojson_features_path.format(query=query_formal_name, feature='nodes/edges')}")
			except:
				print(f"Neither node nor edge for {query} was found")
			
			try:
				area = ox.geocode_to_gdf(query)
				area.to_file(geojson_features_path.format(query=query_formal_name, feature='area'), driver='GeoJSON')
				print(f"Area in {query} has been found and was stored at {geojson_features_path.format(query=query_formal_name, feature='area')}")
			except:
				print(f"No area was found in {query}")

			try:
				buildings = ox.features_from_place(query, {"building": True})
				assert(len(buildings) > 0)
				buildings.to_file(geojson_features_path.format(query=query_formal_name, feature='bulidings'), driver='GeoJSON')
				print(f"{len(buildings)} buildings in {query} have been found and stored at {geojson_features_path.format(query=query_formal_name, feature='bulidings')}")
			except:
				print(f"No building was found in {query}")
			for amenity in amenities:
				try:
					feature = ox.features_from_place(query, {"amenity": amenity})
					assert(len(feature) > 0)
					feature.to_file(geojson_features_path.format(query=query_formal_name, feature=amenity), driver='GeoJSON')
					print(f"{len(feature)} {amenity} in {query} have been found andstored at {geojson_features_path.format(query=query_formal_name, feature=amenity)}")
				except:
					print(f"No {amenity} was found in {query}")
			try:
				water = ox.features_from_place(query, {"natural": "water"})
				assert(len(water) > 0)
				water.to_file(geojson_features_path.format(query=query_formal_name, feature='water'), driver='GeoJSON')
				print(f"{len(water)} water area in {query} have been found and stored at {geojson_features_path.format(query=query_formal_name, feature='water')}")
			except:
				print(f"No water was found in {query}")
			print("\n")