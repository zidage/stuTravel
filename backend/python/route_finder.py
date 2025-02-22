import osmnx as ox
from os import environ
from route_optimizer import optimize_route
from datetime import datetime
import heapq


DISTANCE_FIRST = 0
TIME_FIRST = 1
WALK = 0
BIKE = 1


root_dir = f'{environ["MAP_DATA"]}/map_exports_test'


def get_offset(transport):
    current_time = datetime.now()
    current_hour = current_time.hour
    offset = 0

    if 7 <= current_hour <= 9 or 16 <= current_hour <= 19:
        offset = -3 if transport == 'bike' else -1
    return offset 


def route_find(map_basket, orig, dest):
    orig_node = ox.nearest_nodes(map_basket["graph"], orig[0], orig[1])
    dest_node = ox.nearest_nodes(map_basket["graph"], dest[0], dest[1])

    return ox.shortest_path(map_basket["graph"], orig_node, dest_node, weight="length")


def heuristic(node, target, strategy):
    x1, y1 = node
    x2, y2 = target
    return 0 if strategy == TIME_FIRST else abs(x1 - x2) + abs(y1 - y2)


def astar(adjacency_list, node_list, start, end, strategy=DISTANCE_FIRST, transport=WALK):
    wts = {node: (float('inf'), float('inf')) for node in adjacency_list}
    wts[start] = (0, 0) # wts[][0]是距离 wts[][1]是时间
    heap = [(0, 0, 0, start)] # 第一项是heuristic函数返回的值 第二项是当前策略下的权值 第三项是与当前策略对立的另一策略的权值
    previous = {}

    if start == end:
        return (0, 0), [start]

    weight_select = 0 if strategy == DISTANCE_FIRST else strategy + transport

    while heap:
        _, current_g, current_other_g, current_node = heapq.heappop(heap)

        if current_node == end:
            break

        for neighbor, weight in adjacency_list[current_node].items():
            try:
                wt = current_g + weight[weight_select]
                wt_another = 0
                if strategy == DISTANCE_FIRST:
                    wt_another = current_other_g + weight[1 + transport]
                elif strategy == TIME_FIRST:
                    wt_another = current_other_g + weight[0]
                if wt < wts[neighbor][strategy]:
                    if strategy == DISTANCE_FIRST:
                        wts[neighbor] = (wt, wt_another)
                    elif strategy == TIME_FIRST:
                        wts[neighbor] = (wt_another, wt)
                    f = wt + heuristic(node_list[neighbor], node_list[end], strategy)
                    heapq.heappush(heap, (f, wt, wt_another, neighbor))
                    previous[neighbor] = current_node
            except:
                continue
    
    if end not in previous:
        return (0, 0), []
    
    path_node = []
    node = end
    while node != start:
        path_node.insert(0, node)
        node = previous[node]
    path_node.insert(0, start)

    return wts[end], path_node


def route_find_test(place, map_basket, waypoints, strategy=DISTANCE_FIRST, transport=WALK):
    # optimize_route(map_basket, waypoints, strategy, transport)
    
    route = []
    for i in range(len(waypoints) - 1):
        orig_node = ox.nearest_nodes(map_basket["graph"], waypoints[i][0], waypoints[i][1])
        dest_node = ox.nearest_nodes(map_basket["graph"], waypoints[i + 1][0], waypoints[i + 1][1])
        wt, path = astar(map_basket["adj_list"], map_basket["nd_list"], orig_node, dest_node, strategy, transport)
        route.append((path, wt))
    
    return route


    

