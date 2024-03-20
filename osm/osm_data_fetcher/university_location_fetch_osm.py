import json
import requests
import time
import osmnx as ox
import matplotlib.pyplot as plt
import os


input_file_path = 'map_data/beijing_university.json'
amenities = ["restaurant", "cafe", "library", "hospital",
        	"cinema", "bar", "bus_station", 
			"parking", "police", "bicycle_parking", 
			"food_court", "toilets"]
with open(input_file_path, 'r', encoding='utf-8') as input_file:
	university_list = json.load(input_file)['university']

	for university in university_list:
		query = university['name']
		csv_node_path = f'map_data/university_map/{query}/{query}_nodes.csv'
		csv_edge_path = f'map_data/university_map/{query}/{query}_edges.csv'
		csv_features_path = 'map_data/university_map/{query}/{query}_{feature}.csv'
		if not os.path.exists(f'map_data/university_map/{query}'):
			os.makedirs(f'map_data/university_map/{query}')

		try:
			graph = ox.graph_from_place(query)
			nodes, edges = ox.graph_to_gdfs(graph)
			
			nodes.to_csv(csv_node_path)
			edges.to_csv(csv_edge_path)
			print(f"Nodes and Edges for {query} have been found and were stored at map_data/university_map/{query}/{csv_node_path} and map_data/university_map/{query}/{csv_edge_path}")
		except:
			print(f"Nodes and Edges for {query} have not been found")
		
		try:
			area = ox.geocode_to_gdf(query)
			area.to_csv(f"Area in {query} has been found and were stored at {csv_features_path.format(query=query, feature='area')}")
		except:
			print(f"No area was found in {query}")

		try:
			buildings = ox.features_from_place(query, {"building": True})
			buildings.to_csv(csv_features_path.format(query=query, features='bulidings'))
			print(f"{len(buildings)} buildings in {query} have been found and were stored at {csv_features_path.format(query=query, feature='bulidings')}")
		except:
			print(f"No building was found in {query}")
		for amenity in amenities:
			try:
				feature = ox.features_from_place(query, {"amenity": amenity})
				feature.to_csv(csv_features_path.format(query=query, feature=amenity))
				print(f"{len(feature)} {amenity} in {query} have been found and were stored at {csv_features_path.format(query=query, feature=amenity)}")
			except:
				print(f"No {amenity} was found in {query}")
		print("\n")