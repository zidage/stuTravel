"""
地图数据获取模块, 获取数据源: OpenStreetMap
功能: 使用osmnx库以及Google Map Platform中的Place API请求地点名称列表中各地点的详细数据

作者: 字禹润

创建日期: 2024-03-20
最后修改日期: 2024-03-24
"""


import json
from urllib import response
import requests
import time
import osmnx as ox
import matplotlib.pyplot as plt
import os


# Google Map Platform API request URL
google_api_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&language=zh-CN&key={API_KEY}'
input_file_path = ['map_data/catagory/china_university.json', 'map_data/catagory/world_university.json']


for input_path in input_file_path:
	with open(input_path, 'r', encoding='utf-8') as input_file:
		university_list = json.load(input_file)
		
		for university in university_list:
			query = university
			query_formal_name = query.replace(' ', '_')
			# gm_features_path = 'map_data/university_map_test/{query}/{query}_{feature}.graphml'
			gpkg_features_path = 'map_data/university_map/{query}/{query}_{feature}.gpkg'
			gm_features_path = 'map_data/university_map/{query}/{query}_{feature}.graphml'
			info_file_path = 'map_data/university_map/{query}/{query}_info.json'
			
			# 谷歌地图数据获取，获取地点名、地址、评分
			try:
				if not os.path.exists(f'map_data/university_map/{query_formal_name}'):
					os.makedirs(f'map_data/university_map/{query_formal_name}')
				else:
					continue
				response = requests.get(google_api_url.format(query=query, API_KEY='AIzaSyAa2ZdkUiY7jLWkZJABgUtKMwEdHQA1pvU'))
				assert(response.status_code == 200)
				result = response.json()['results'][0]
				data = {'name': result['name'], 'address': result['formatted_address'], 
						'rating': result['rating']}
				data_with_parent = {'university': data}
				with open(info_file_path.format(query=query_formal_name), 'w', encoding='gb2312') as f:
					json.dump(data_with_parent, f, indent=4, ensure_ascii=False)
					print(f'Basic info of {query} has been found and stored at {info_file_path.format(query=query_formal_name)}')
			except:
				# time.sleep(1)
				print(f"{query} does not exits\n")
				continue

			# 道路网络数据获取，获取选定地点为中心的1200*1200米的bbox内的所有道路数据
			try:
				graph = ox.graph_from_address(query, dist=1200)
				ox.save_graphml(graph, filepath=gm_features_path.format(query=query_formal_name, feature='graph')) # Graph类型数据须存储作.graphml格式，避免坐标系混乱
				print(f"Nodes and Edges for {query} have been found and were stored at {gpkg_features_path.format(query=query_formal_name, feature='graph')}")
			except:
				print(f"Neither node nor edge for {query} was found")
			
			# 以下数据类型均存储为.gpkg格式，可保留基本坐标系信息
			# 获取地点占据区域
			try:
				area = ox.geocode_to_gdf(query)
				area.to_file(gpkg_features_path.format(query=query_formal_name, feature='area'), driver='GeoJSON')
				print(f"Area in {query} has been found and was stored at {gpkg_features_path.format(query=query_formal_name, feature='area')}")
			except:
				print(f"No area was found in {query}")

			
			try:
				buildings = ox.features_from_place(query, {"building": True})
				buildings = buildings.apply(lambda c: c.astype(str) if c.name != "geometry" else c, axis=0)
				buildings.to_file(f"{gpkg_features_path.format(query=query_formal_name, feature='buildings')}", driver="GPKG")
				print(f"Buildings in {query} have been found and stored at {gpkg_features_path.format(query=query_formal_name, feature='buildings')}")
			except:
				print(f"No building was found in {query}")

			# 获取地点占据区域内设施
			try:
				amenity = ox.features_from_place(query, tags={"amenity": True})
				amenity = amenity.apply(lambda c: c.astype(str) if c.name != "geometry" else c, axis=0)
				amenity.to_file(f"{gpkg_features_path.format(query=query_formal_name, feature='amenity')}", driver="GPKG") 
				print(f"Amenity found in {query}")
			except:
				print(f"No amenity was found in {query}")
			print("\n")