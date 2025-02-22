import osmnx as ox
import networkx as nx
import heapq



DISTANCE_FIRST = 0
TIME_FIRST = 1
WALK = 0
BIKE = 1


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


def optimize_route(map_basket, waypoints, strategy, transport):
    tsp_graph = []
    wpt = []

    adj_list = map_basket["adj_list"]
    nd_list = map_basket["nd_list"]

    for i in range(len(waypoints) - 1):
        wpt_a = waypoints[i]
        for j in range(i + 1, len(waypoints)):
            wpt_b = waypoints[j]
            orig_node = ox.nearest_nodes(map_basket["graph"], wpt_a[0], wpt_a[1])
            dest_node = ox.nearest_nodes(map_basket["graph"], wpt_b[0], wpt_b[1])
            wt, path = astar(adj_list, nd_list, orig_node, dest_node, strategy, transport)
            if wt == 0:
                return None
            tsp_graph.append((wpt_a[-1], wpt_b[-1], wt[strategy], path))
        wpt.append(int(wpt_a[-1]))
    wpt.append(int(waypoints[-1][-1]))
    
    G = nx.Graph()

    for u, v, w, _ in tsp_graph:
        G.add_edge(u, v, weight=w)
    
    try:
        optimized_wpt, _ = christofides_tsp(G)
        return optimized_wpt
    except:
        return None
    # print(tsp_graph)
    # print()


def christofides_tsp(G):
    # Step 1: Compute the Minimum Spanning Tree (MST)
    mst = nx.minimum_spanning_tree(G, weight='weight')

    # Step 2: Find vertices with odd degree in the MST
    odd_degree_nodes = [v for v, degree in mst.degree() if degree % 2 == 1]

    # Step 3: Find the Minimum Weight Matching on odd degree nodes
    subgraph = G.subgraph(odd_degree_nodes)
    min_weight_matching = nx.algorithms.matching.min_weight_matching(subgraph, weight='weight')

    # Step 4: Combine MST and Minimum Weight Matching to form an Eulerian circuit
    multi_graph = nx.MultiGraph(mst)
    multi_graph.add_edges_from(min_weight_matching)

    # Step 5: Find an Eulerian circuit in the multi-graph
    eulerian_circuit = list(nx.eulerian_circuit(multi_graph))

    # Step 6: Convert Eulerian circuit to Hamiltonian circuit by skipping visited nodes
    visited = set()
    path = []
    for u, v in eulerian_circuit:
        if u not in visited:
            path.append(u)
            visited.add(u)
    path.append(path[0])  # Return to start

    # Calculate total distance of the path
    total_distance = sum(G[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))

    return path, total_distance