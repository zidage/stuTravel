import pandas as pd

# 加载 CSV 文件
df = pd.read_csv("data_fetcher\qs_ranking\qs_data.csv")

# 筛选符合条件的数据
top_30_WRD = df[~df['location code'].str.startswith('CN')]['institution'].head(30)
top_100_CN = df[df['location code'].str.startswith('CN')]['institution']

top_30_WRD.to_json("map_data/catagory/world_university.json", orient="records", force_ascii=False, indent=4)
top_100_CN.to_json("map_data/catagory/china_university.json", orient="records", force_ascii=False, indent=4)

