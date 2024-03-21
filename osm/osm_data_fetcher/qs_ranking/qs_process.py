import pandas as pd

# 加载 CSV 文件
df = pd.read_csv("osm\osm_data_fetcher\qs_ranking\\qs_data.csv")

# 筛选符合条件的数据
top_100_CN = df[(df['location code'] == 'CN')]['institution'].head(100)

top_100_CN.to_json("china_university.json", orient="records", force_ascii=False)

