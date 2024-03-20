import json
import requests

# 定义查询语句
query = """
[out:json];
(
  node(around:{radius},{latitude},{longitude})["name"="university"];
  way(around:{radius},{latitude},{longitude})["name"="university"];
  relation(around:{radius},{latitude},{longitude})["name"="university"];
);
out body;
>;
out skel qt;
"""

# 替换查询语句中的占位符
query = query.format(radius=30000, latitude=39.9071, longitude=116.3910)

# 发送查询请求并获取响应
response = requests.get("http://overpass-api.de/api/interpreter", params={"data": query})
data = response.json()

output_file_path = "output_data.json"
with open(output_file_path, "w+", encoding='utf-8') as output_file:
    json.dump(data, output_file, indent=4, ensure_ascii=False)
