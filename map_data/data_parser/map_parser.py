import geopandas as gpd
import os

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

working_directory = 'map_data/university_map'
university_directories = list_subdirectories(working_directory)
print(len(university_directories))




