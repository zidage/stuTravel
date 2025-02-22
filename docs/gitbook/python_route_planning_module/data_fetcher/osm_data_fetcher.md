# osm\_data\_fetcher

该文件夹下有两个 Python 文件，分别为：

* `university_location_fetch_amap.py`
* `university_location_fetch_osm.py`

### `university_location_fetch_amap.py`

该程序将从

```python
map_data/provinces.json
```

中获取省份信息，该省份信息来源：[https://github.com/modood/Administrative-divisions-of-China](https://github.com/modood/Administrative-divisions-of-China)

随后，利用高德Web基础服务API，查询该省份下所有高校的名称以及对应高德经纬度信息。目前该子程序由于涉及坐标转换等诸多难点，已被废弃。

### `university_location_fetch_osm.py`

该子程序目前主要的地图数据获取方式。程序将通过谷歌API获取地点的格式化文本信息并存储为`.json`文件。然后用`OSMnx`查询目标地点的相关GIS数据，并保存为`.gpkg`文件。

### `google_api_url`

该变量为`Google Place API`的请求`URL`，

