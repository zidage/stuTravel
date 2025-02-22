from datetime import datetime


current_time = datetime.now()

current_hour = current_time.hour

rush_hour = False

if 7 <= current_hour <= 9:
    rush_hour = True

street_types_dict = {
    'motorway': 70,  # 高速公路，限速70mph
    'motorway_link': 70,
    'trunk': 60,  # 主干道，限速60mph
    'trunk_link': 60,
    'primary': 50,  # 主要道路，限速50mph
    'primary_link': 50,
    'secondary': 40,  # 次要道路，限速40mph
    'secondary_link': 40,
    'tertiary': 35,  # 三级道路，限速35mph
    'tertiary_link': 35,
    'residential': 25,  # 居民区道路，限速25mph
    'service': 20,  # 服务道路，限速20mph
    'unclassified': 30,  # 未分类道路，限速30mph
    'road': 40,  # 一般道路，限速40mph
    'living_street': 20,  # 生活街道，限速20mph
    'pedestrian': 10,  # 步行街，限速10mph
    'track': 15,  # 小路，限速15mph
    'path': 10,  # 小径，限速10mph
    'footway': 5,  # 人行道，限速5mph
    'cycleway': 10,  # 自行车道，限速10mph
    'bridleway': 10,  # 马道，限速10mph
    'steps': 5,  # 台阶，限速5mph
    'corridor': 20,  # 走廊，限速20mph
    'proposed': 30,  # 拟议道路，限速30mph
    'construction': 30,  # 施工中道路，限速30mph
    'bus_guideway': 40,  # 公交车专用道，限速40mph
    'escape': 25,  # 逃生通道，限速25mph
    'raceway': 80,  # 赛车道，限速80mph
    'services': 20,  # 服务区道路，限速20mph
    'rest_area': 20,  # 休息区道路，限速20mph
    'abandoned': 20,  # 废弃道路，限速20mph
    'planned': 30,  # 计划中道路，限速30mph
}

def get_speed(transport, street_type):
    # 对字典中的值进行加上偏移量
    
    if transport == 0:
        # 当在早晚高峰时段路越宽越拥挤，但对行人影响较小
        # 行人默认速度为1.3m/s
        try:
            return 1.3 + (-0.007 if rush_hour else 0.005) * street_types_dict[street_type]
        except:
            return 1.3 + (-0.007 if rush_hour else 0.005) * street_types_dict['residential']
    else:
        # 当在早晚高峰时段路越宽越拥挤，但对自行车影响较大
        # 自行车默认速度为3m/s
        try:
            return 3 + (-0.01 if rush_hour else 0.02) * street_types_dict[street_type]
        except:
            return 3 + (-0.01 if rush_hour else 0.02) * street_types_dict['residential']
    