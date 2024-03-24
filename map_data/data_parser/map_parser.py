"""
地图数据处理模块
功能: 删除数据文件夹中数据不完整的文件夹, 并从特定格式文件中还原networkx和geopandas等库中规定的数据.
然后利用matplotlib中的方法对地图进行可视化还原, 这个模块仅作实验性使用, 日后可能其功能会被拆分.

作者: 字禹润

创建日期: 2024-03-21
最后修改日期: 2024-03-24
"""


import geopandas as gpd
import os
import shutil
import matplotlib.pyplot as plt
import json
import networkx as nx
import osmnx as ox
from shapely.geometry import Polygon, MultiPolygon, Point
from random import randint



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


def delete_folders_with_few_files(root_dir, min_files=2):
    """
    该函数可以删除给定根目录下文件个数少于等于min_files个数的子文件夹

    Parameter:
    root_dir (str): 根目录地址
    min_files (int): 文件夹删除阈值

    Returns:
    void
    """
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if len(filenames) <= min_files and dirpath != root_dir:  # 排除根文件夹
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
    with open(file, 'r', encoding='gb2312') as f:
        js = json.load(f)
        return js["university"]["name"]


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
        gdf = gdf[gdf['amenity'] != 'university'].drop_duplicates(subset=['name']) # 将含'university'的数据行删去，并去除名字重复的数据
        gdf = gdf[gdf['name'] != 'nan'] # 将含'nan'的数据行删去
        # print(gdf.head())
        return gdf
    except:
        print("Amenity file parsing error")
        return None


def amenity_filter(amenity_gdf, area_gdf):
    """
    amenity类型文件的进一步筛选函数, 目前已废弃. 
    """
    try:
        # 定义函数处理每个几何对象
        def filter_geometry(row):
            geom = row['geometry']
            if isinstance(geom, Point) or isinstance(geom, Polygon):
                return any(geom.within(polygon) for polygon in area_gdf['geometry'])
            elif isinstance(geom, MultiPolygon):
                for poly in geom.geoms:
                    if any(poly.within(polygon) for polygon in area_gdf['geometry']):
                        return True
                return False

        # 对每个 'amenity_gdf' 中的几何值进行空间查询，并保留在 'area_gdf' 中的数据
        filtered_gdf = amenity_gdf[amenity_gdf.apply(filter_geometry, axis=1)]
        return filtered_gdf
    except Exception as e:
        print("filter error: ", e)
        return amenity_gdf


def map_view_generator(map_basket, university):
    """
    根据各类数据集合对各种数据进行可视化的函数

    Parameter:
    map_basket (dict): 特定地点的数据集合
    university (str): 文件命名所用字符串的组成部分

    Returns:
    void
    """

    # 创建thumbnail文件夹，目前该函数仅用于生成缩略图
    if not os.path.exists(f'map_data/map_thumbnail'):
        os.makedirs(f'map_data/map_thumbnail')

    if map_basket["graph"] is not None: # 先对存储有road network的graph数据进行可视化，具体参数详见osmnx及matplotlib文档
        fig, ax = ox.plot_graph(
            map_basket["graph"],
            show=False,
            close=False,
            bgcolor="#141414",
            edge_color="lightgrey",
            edge_linewidth=1,
            node_size=0,
        )

        # 显示路名
        for _, edge in ox.graph_to_gdfs(map_basket["graph"], nodes=False).fillna("").iterrows():
            random_number = randint(1, 100) # 由于每条边都有命名，所以将随机显示，避免文字过密
            if (random_number % 3 == 0):
                text = edge["name"]
                c = edge["geometry"].centroid
                ax.annotate(text, (c.x, c.y), c="white", fontname='Microsoft YaHei', fontsize=3)

        # 显示地点占据区域
        if map_basket["area"] is not None:
            map_basket["area"].plot(ax=ax, facecolor='dimgrey', linewidth=0.6, edgecolor='black', alpha=0.5)
            offset = 0.001 # offset参数，单位为"°"，用于控制缩放范围
            bbox = map_basket["area"].total_bounds # 区域占据的bbox大小，用于限定显示范围
            ax.set_xlim(bbox[0]-offset, bbox[2]+offset)
            ax.set_ylim(bbox[1]-offset, bbox[3]+offset)

        # 显示建筑
        if map_basket["building"] is not None:
            map_basket["building"].plot(ax=ax, facecolor='lightgrey')

        #显示设施
        if map_basket["amenity"] is not None:
            filtered_gdf = amenity_filter(map_basket["amenity"], map_basket["area"])
            # 显示设施名，并用红点标注
            for idx, row in filtered_gdf.iterrows():
                centroid = row.geometry.centroid
                ax.text(centroid.x, centroid.y, row['name'], fontsize=4, fontname='Microsoft YaHei', color='white')
                ax.scatter(centroid.x, centroid.y, color='red', s=10)

        # 缩略图存储文件名
        file_name = university.split('\\')[1]
        # 存储文件
        plt.savefig(f'map_data/map_thumbnail/map_thumbnail_{file_name}.png', bbox_inches='tight', dpi=300)
        plt.close()


# main函数
root_dir = 'map_data/university_map'
delete_folders_with_few_files(root_dir)
university_directories = list_subdirectories(root_dir)

for university in university_directories:
    files_path = get_files_in_folder(university)
    map_basket = {"name": None, "graph": None, "area": None, 
                  "building": None, "amenity": None}
    for file in files_path:   
        parsed_line = file.split('_')
        file_type = parsed_line[-1]
        if file_type == 'info.json':
            map_basket["name"] = info_parser(file)
        elif file_type == 'graph.graphml':
            map_basket["graph"] = graph_parser(file)
        elif file_type == 'area.gpkg':
            map_basket["area"] = regular_parser(file)
        elif file_type == 'buildings.gpkg':
            map_basket["building"] = regular_parser(file)
        elif file_type == 'amenity.gpkg':
            map_basket["amenity"] = amenity_parser(file)

    map_view_generator(map_basket, university)
    print(university + ' thumbnail generated!')
        
            




