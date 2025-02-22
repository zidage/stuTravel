"""
地图数据处理模块
功能: 删除数据文件夹中数据不完整的文件夹, 并从特定格式文件中还原networkx和geopandas等库中规定的数据.
然后利用matplotlib中的方法对地图进行可视化还原, 这个模块仅作实验性使用, 日后可能其功能会被拆分.

作者: 字禹润

创建日期: 2024-03-21
最后修改日期: 2024-03-24
"""


from fileinput import filename
import imp
import geopandas as gpd
import os
import shutil
from matplotlib.font_manager import json_dump
import matplotlib.pyplot as plt
import json
import networkx as nx
from numpy import save
import osmnx as ox
from shapely.geometry import Polygon, MultiPolygon, Point
from random import randint
import pickle
import speed_limit


def list_subdirectories(root_dir):
    """
    该函数可以返回文件夹中所有子目录。

    Parameter:
    root_dir (str): 根目录地址

    Returns:
    list: 根目录下所有子目录
    """
    subdirectories = []
    # 遍历root_dir下的所有文件和文件夹
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        # 如果是文件夹，则将其添加到subdirectories列表中
        if os.path.isdir(item_path):
            subdirectories.append(item_path)
            # 递归地调用list_subdirectories函数，继续遍历子文件夹
    return subdirectories


def delete_folders_with_few_files(root_dir, min_files=5):
    """
    该函数可以删除给定根目录下文件个数少于等于min_files个数的子文件夹

    Parameter:
    root_dir (str): 根目录地址
    min_files (int): 文件夹删除阈值

    Returns:
    void
    """
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if len(filenames) < min_files and dirpath != root_dir:  # 排除根文件夹
            for file in filenames:
                os.remove(os.path.join(dirpath, file))  # 删除文件
            os.rmdir(dirpath)  # 删除空文件夹
            print(f"Deleted folder: {dirpath}")


def get_files_in_folder(folder_path):
    """
    该函数可以返回给定目录下所有文件的路径列表

    Parameter:
    folder_path (str): 文件夹如今

    Returns:
    list: 目录下的所有文件的路径组成的列表
    """
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def info_parser(file):
    """
    *_info.json文件的解析函数, 目前只回返回"name"这个key的对应value

    Parameter:
    file (str): 文件路径

    Returns:
    str: 地点中文名
    """
    with open(file, 'r', encoding='utf-8') as f:
        js = json.load(f)
        return js["place"]["name"], js["place"]["address"], js["place"]["description"], js["place"]["img"], js["place"]["rating"]


def regular_parser(file):
    """
    常规地理信息文件的解析函数, 返回一个GeoDataFrame.

    Parameter:
    file (str): 文件路径

    Returns:
    GeoDataFrame: 读取特定地理信息文件后形成的GeoDataFrame
    """
    gdf = gpd.read_file(file)
    return gdf


def graph_parser(file):
    """
    graph类型文件的解析函数, 返回一个graph类型的对象.

    Parameter:
    file (str): 文件路径

    Returns:
    Graph: networkx库中定义的存储图的数据对象, 可能是Graph, DiGraph, MultiGraph, MultiDiGraph中的一种
    """
    return ox.load_graphml(file)


def building_parser(file):
    """
    building类型文件的解析函数, 会对一个地点范围内的建筑进行筛选并返回一个GeoDataFrame. 

    Parameter:
    file (str): 文件路径

    Returns:
    GeoDataFrame: 地点范围内建筑的data set.
    """
    gdf = gpd.read_file(file)
    try:
        gdf = gdf[gdf['name'] != 'nan']
    except:
        return gdf
    return gdf


def area_parser(file):
    """
    Deprecated. 与regular_parser功能相同
    """
    gdf = gpd.read_file(file)
    return gdf


def amenity_parser(file):
    """
    amenity类型文件的解析函数, 会对一个地点范围内的设施进行筛选并返回一个GeoDataFrame. 

    Parameter:
    file (str): 文件路径

    Returns:
    GeoDataFrame: 地点范围内设施的data set.
    """
    try:
        gdf = gpd.read_file(file)
        gdf = gdf[gdf['amenity'] != 'university'].drop_duplicates(
            subset=['name'])  # 将含'university'的数据行删去，并去除名字重复的数据
        # 将仅为数字的数据行删掉（防止垃圾数据）
        gdf = gdf[~gdf['name'].astype(str).str.isdigit()]
        gdf.replace({'nan': '可能感兴趣的地点'}, inplace=True)
        # print(gdf.head())
        return gdf
    except:
        print("Amenity file parsing error")
        return None

osmid_existed = []

def export_data_object(map_basket, amenity_basket, university):
    """
    地图属性集合的导出函数, 可将地图属性导出为json以及序列化一个Python对象存储到硬盘上

    Parameter:
    map_basket (dict): 地图属性集合
    amenity_basket (dict): 设施属性集合
    university (str): 大学名称

    Returns:
    None
    """
    file_name = university.split('\\')[-1]
    save_path = f"{os.environ['MAP_DATA']}/map_exports_test/{file_name}"
    os.makedirs(save_path)
    # gdf = amenity_filter(map_basket["amenity"], map_basket["area"])
    # print(map_basket["amenity"].head(100))
    amenity_basket["amenity_list"] = []
    
    try:
        # 将设施的名字，类型，位置放入amenity_basket的amenity_list列表中
        for idx, row in map_basket["amenity"].iterrows():
            try:
                if not row["osmid"] in osmid_existed:
                    amenity_basket["amenity_list"].append({"id": row['osmid'], "name": row["name"], "type": row["amenity"],
                                                        "latitude": row["geometry"].centroid.y, "longitude": row["geometry"].centroid.x})
                    osmid_existed.append(row["osmid"])
            except:
                print(f"Cannot desolve one amenity in {file_name}")
        for idx, row in map_basket["building"].iterrows():
            try:
                if not row["osmid"] in osmid_existed:
                    amenity_basket["amenity_list"].append({"id": row['osmid'], "name": row["name"], "type": row["amenity"],
                                                        "latitude": row["geometry"].centroid.y, "longitude": row["geometry"].centroid.x})
                    osmid_existed.append(row["osmid"])
            except:
                print(f"Cannot desolve one building in {file_name}")    
    except:
        print(f"No amenity or building in {file_name}")
    # 导出的json文件的字典表示
    export_data = {
        "id": map_basket["id"],
        "name": map_basket["name"],
        "address": map_basket["address"],
        "rating": map_basket["rating"],
        "popularity": map_basket["popularity"],
        "data_path": f"map_data/university_map/{file_name}",
        "description": map_basket["description"],
        "images": map_basket["images"],
        "amenity": amenity_basket
    }
    with open(f"{save_path}/{file_name}_map.json", 'w', encoding='utf-8') as file:
        json.dump(export_data, file, indent=4, ensure_ascii=False)
    with open(f"{save_path}/{file_name}_sr.pickle", 'wb') as file: # sr指serialized
        pickle.dump(map_basket, file)  # 存储为pickle文件，把对象腌成泡菜


def get_graph(map_basket):
    # print("get_graph starts")
    try:
        nodes = ox.graph_to_gdfs(map_basket["graph"], edges=False).fillna("")
        edges = ox.graph_to_gdfs(map_basket["graph"], nodes=False).fillna("")
        # print(edges["highway"])
        # print(nodes.iloc[2].name)
        walk_speed = []
        bike_speed = []
        for idx, rows in edges.iterrows():
            if (type(rows['highway']) == list):
                    rows['highway'] = rows['highway'][0]
            
            walk_speed.append(speed_limit.get_speed(0, rows['highway']))
            bike_speed.append(speed_limit.get_speed(1, rows['highway']))
            
        edges["walk_speed"] = walk_speed
        edges["bike_speed"] = bike_speed

    # print(edges["osmid"].head())

        adjacency_list = {}
        node_list = {}

        graph = ox.graph_from_gdfs(nodes, edges)


        for u, v, key, data in graph.edges(keys=True, data=True):
            #if u is None or v is None:
                #continue

            if u not in adjacency_list:
                adjacency_list[u] = {}
            
            if v not in adjacency_list[u]:
                adjacency_list[u][v] = (data["length"], data["length"] / data["walk_speed"], data["length"] / data["bike_speed"])
                # print(adjacency_list[u][v])
        
        for id, data in graph.nodes(data=True):
            node_list[id] = (data['x'], data['y'])

        # print(node_list)
        # print("get_graph ends")
        return adjacency_list, node_list, walk_speed, bike_speed
    except:
        print("Parse terminate")
        return None, None


# main函数
root_dir = f'{os.environ["MAP_DATA"]}/place_map_test'
delete_folders_with_few_files(root_dir)
place_directories = list_subdirectories(root_dir)

def update_map_data_all():
    for place in place_directories:
        files_path = get_files_in_folder(place)

        map_basket = {"id": None, "name": None, "address": None, "description": None, 
                      "images": None, "rating": None, "popularity": None, 
                      "graph": None, "area": None, "building": None, 
                      "amenity": None, "route": None, "adj_list": None, 
                      "nd_list": None, "walk_speed": None, "bike_speed": None}
        
        amenity_basket = {"affiliation": None, "amenity_list": None}
        for file in files_path:
            parsed_line = file.split('_')  # 把下划线分隔的文件名拆成一个数组
            file_type = parsed_line[-1]  # 得到文件类型
            if file_type == 'info.json':
                map_basket["name"], map_basket["address"], map_basket["description"], map_basket["images"], map_basket["rating"] = info_parser(file)
                map_basket["id"] = hash(map_basket["name"])  # 计算该地点的哈希值
                map_basket["popularity"] = int(
                    map_basket["rating"]) * randint(10, 25)  # 根据地点评分随机生成一个欢迎度
                amenity_basket["affiliation"] = map_basket["id"]
            elif file_type == 'graph.graphml':
                map_basket["graph"] = graph_parser(file)  # 将图解析并存储
                map_basket["adj_list"], map_basket["nd_list"], map_basket["walk_speed"], map_basket["bike_speed"] = get_graph(map_basket)
                #if map_basket["adj_list"] is None or map_basket["nd_list"] is None:
                    #continue
            elif file_type == 'area.gpkg':
                map_basket["area"] = regular_parser(file)  # 将占据区域解析并存储
            elif file_type == 'buildings.gpkg':
                map_basket["building"] = building_parser(file)  # 将建筑解析并存储
            elif file_type == 'amenity.gpkg':
                map_basket["amenity"] = amenity_parser(file)  # 将设施解析并存储

        export_data_object(map_basket, amenity_basket, place)
        print(place + 'export data generated!')



def update_traffic():
    exported_directory = list_subdirectories(f'{os.environ["MAP_DATA"]}\\map_exports_test')
    for place in exported_directory:
        try:
            with open(place + '\\' + place.split('\\')[-1] + '_sr.pickle', 'rb') as f:
                map_basket = pickle.load(f)
            
            try:
                map_basket["adj_list"], map_basket["nd_list"], map_basket["walk_speed"], map_basket["bike_speed"] = get_graph(map_basket)
                with open(place + '\\' + place.split('\\')[-1] + '_sr.pickle', 'wb') as f:
                    pickle.dump(map_basket, f)
                    print("Successfully update traffic in " + place)
            except:
                print("Fail to update traffic in " + place)
        except:
            print("Fail to update traffic in " + place)
        


update_map_data_all()
        