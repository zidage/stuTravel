"""
地图图像生成模块
功能: 

作者: 字禹润

创建日期: 2024-03-30
最后修改日期: 2024-04-03
"""


import geopandas as gpd
import os
import json
import networkx as nx
import osmnx as ox
import pickle
from math import isnan
import route_finder
from shapely.geometry import Point
import route_optimizer


route_color = ["#f94144", "#f3722c", "#f8961e", "#f9c74f",
               "#90be6d", "#43aa8b", "#577590"]

MAP_ONLY = 0
ROUTE_OVERLAY = 1
WALK = 0
BIKE = 1
DISTANCE_FIRST = 0
TIME_FIRST = 1

# 从amn_list中得到某一地点的经纬度以及名字
def get_place(amn_list, place_id):
    place_coor = []
    
    for place in amn_list:
        if (place["id"] == int(place_id)):
            place_coor.append(float(place["longitude"]))
            place_coor.append(float(place["latitude"]))
            place_coor.append(place["name"])
            place_coor.append(place_id)
        
    return place_coor


def new_view_generator(place, map_basket, file_name, 
                       wpt_gdf=None, mode=MAP_ONLY):
    mk = {"radius": 6}
    # print(map_basket["adj_list"])
    # nodes, edges = ox.graph_to_gdfs(map_basket["graph"])

    if (mode == MAP_ONLY):
        m = map_basket["amenity"].explore()
        # m = map_basket["amenity"].explore(tooltip="name")
        print(0)
        m.save(os.environ("DS_FILES") + "\\" + "place_holder.html")
        # print(f"{plan_id} html saved!")
        return
    
    trip_time = 0
    trip_dist = 0

    m = None

    for index, route in enumerate(map_basket["route"], start=0):
        route_edges = ox.routing.route_to_gdf(
            map_basket["graph"], route[0], weight="length")
        
        if m is not None:
            m = route_edges.explore(m=m, style_kwds={
                                    "weight": 6, "opacity": 0.8}, color=route_color[index % len(route_color)])
        else:
            m = route_edges.explore(style_kwds={
                                    "weight": 6, "opacity": 0.8}, color=route_color[index % len(route_color)])
        trip_dist += route[1][0]
        trip_time += route[1][1]
    m = wpt_gdf.explore(m=m, tooltip="name", marker_kwds=mk)

    
    
    print(str(trip_time)+","+str(trip_dist))
    # print("Throuth road" + str(path))
    #if waypoints is not None:
        #for index, w in enumerate(waypoints, start=0):
            #map_basket["amenity"].loc[map_basket["amenity"]["name"] == w[2]].explore(m=m, tooltip="name", marker_kwds=mk,
                                                                                  #color=route_color[index % len(route_color)])

    m.save(os.environ("DS_FILES") + "\\" + f"{plan_id}.html")
    # print(f"{plan_id} html saved!")


# main函数
root_dir = f'{os.environ["MAP_DATA"]}/map_exports'
# output_dir = f'{os.environ["MAP_DATA"]}/map_view_test'


# 用户输入
# 用户输入将由3-5部分组成, 其中参数0, 1, 2分别为模式、地点规范名称、缩放因子
# 参数3, 4则为-b模式下起点及终点的id
user_input = input().split()
mode = user_input[0]
plan_id = user_input[1]
strategy = user_input[2]
transport = user_input[3]
place = user_input[4]


# query的大学名称未找到则程序将暂停
if not os.path.exists(f"{root_dir}/{place}"):
    print("Folder do not exist!")
else:
    with open(f"{root_dir}/{place}/{place}_sr.pickle", "rb") as f:
        map_basket = pickle.load(f)
        map_basket["route"] = []
        if (mode == '-n' or len(user_input) < 6):  # -n模式, 该模式将不显示路径
            new_view_generator(place, map_basket, plan_id)
            # view_generator(map_basket, university, output_dir,
            # None, None, scale_factor=float(user_input[2]))
        elif (mode == '-r' or mode == '-o'):  # -b模式，该模式将显示路径, 并需要client程序输入起点及终点
            with open(f"{root_dir}/{place}/{place}_map.json", "r", encoding='utf-8') as js_file:
                js = json.load(js_file)
                amn_list = js["amenity"]["amenity_list"]
                orig_venue, dest_venue = None, None
                waypoints = {"name": [], "geometry": []}
                wpt = []
                for i in range(5, len(user_input) - 1):
                    orig_venue = get_place(amn_list, user_input[i])
                    dest_venue = get_place(amn_list, user_input[i + 1])
                    waypoints["name"].append(orig_venue[2])
                    waypoints["geometry"].append(Point(orig_venue[0], orig_venue[1]))
                    wpt.append(orig_venue)
                waypoints["name"].append(dest_venue[2])
                waypoints["geometry"].append(Point(dest_venue[0], dest_venue[1]))
                wpt.append(dest_venue)
                if (mode == '-o'):
                    result = route_optimizer.optimize_route(map_basket, wpt, int(strategy), int(transport))
                    if result is None:
                       print("None")
                       exit(0)
                    for i in range(len(result) - 1):
                        print(result[i] + ",", end='')
                    print(result[-1])
                    exit(0)
                wpt_gdf = gpd.GeoDataFrame(waypoints)
                map_basket["route"] = route_finder.route_find_test(place, map_basket, wpt, int(strategy), int(transport))
                new_view_generator(place, map_basket, plan_id, wpt_gdf, ROUTE_OVERLAY)
