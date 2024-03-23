import geopandas as gpd
import os
import shutil
import matplotlib.pyplot as plt
import json




def list_subdirectories(root_dir):
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
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if len(filenames) <= min_files and dirpath != root_dir:  # 排除根文件夹
            for file in filenames:
                os.remove(os.path.join(dirpath, file))  # 删除文件
            os.rmdir(dirpath)  # 删除空文件夹
            print(f"Deleted folder: {dirpath}")


def get_files_in_folder(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def info_parser(file):
    with open(file, 'r', encoding='gb2312') as f:
        js = json.load(f)
        return js["university"]["name"]


def regular_parser(file):
    return gpd.read_file(file)


def amenity_parser(file):
    return gpd.read_file(file, GEOM_POSSIBLE_NAMES="geometry", KEEP_GEOM_COLUMNS="NO")


def map_view_generator(map_basket, university):
    if not os.path.exists(f'map_data/map_thumbnail'):
        os.makedirs(f'map_data/map_thumbnail')
    fig, ax = plt.subplots(figsize=(12, 8))
    # Plot the footprint
    if map_basket["area"] is not None:
        map_basket["area"].plot(ax=ax, facecolor="black")

    # Plot street edges
    if map_basket["edge"] is not None:
        map_basket["edge"].plot(ax=ax, linewidth=1, edgecolor="dimgray")

    # Plot buildings
    if map_basket["building"] is not None:
        map_basket["building"].plot(ax=ax, facecolor="silver", alpha=0.7)

    if map_basket["water"] is not None:
        map_basket["water"].plot(ax=ax, facecolor="xkcd:sky blue")

    # Plot restaurants
    # restaurants.plot(ax=ax, color="yellow", alpha=0.7, markersize=10)
    plt.tight_layout()
    file_name = university.split('\\')[1]
    plt.show()
    plt.savefig(f'map_data/map_thumbnail/map_thumbnail_{file_name}.png', bbox_inches='tight')
    plt.close()



root_dir = 'map_data/university_map'
delete_folders_with_few_files(root_dir)
university_directories = list_subdirectories(root_dir)

for university in university_directories:
    files_path = get_files_in_folder(university)
    map_basket = {"name": None, "node": None, "edge": None, "area": None, 
                  "building": None, "water": None, "amenity": []}
    for file in files_path:   
        parsed_line = file.split('_')
        file_type = parsed_line[-1]
        if file_type == 'info.json':
            map_basket["name"] = info_parser(file)
        elif file_type == 'nodes.csv':
            map_basket["node"] = regular_parser(file)
        elif file_type == 'edges.csv':
            map_basket["edge"] = regular_parser(file)
        elif file_type == 'area.csv':
            map_basket["area"] = regular_parser(file)
        elif file_type == 'buildings.csv':
            map_basket["building"] = regular_parser(file)
        elif file_type == 'water.csv':
            map_basket["water"] = regular_parser(file)
        # else:
            #map_basket["amenity"].append(amenity_parser(file))
    # print(os.getcwd())
    map_view_generator(map_basket, university)
    print(university + ' thumbnail generated!')
        
            




