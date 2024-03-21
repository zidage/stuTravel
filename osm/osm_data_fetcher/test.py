import json
import requests
import time
import osmnx as ox
import matplotlib.pyplot as plt
import os


query = "University of Electronic Science and Technology of China"


graph = ox.graph_from_place(query)
nodes, edges = ox.graph_to_gdfs(graph)
area = ox.geocode_to_gdf(query)
area.to_csv()
buildings = ox.features_from_place(query, {"building": True})
# restaurants = ox.features_from_place(query, {"amenity": "restaurant"})
fig, ax = plt.subplots(figsize=(12, 8))
# Plot the footprint
area.plot(ax=ax, facecolor="black")

# Plot street edges
edges.plot(ax=ax, linewidth=1, edgecolor="dimgray")

# Plot buildings
buildings.plot(ax=ax, facecolor="silver", alpha=0.7)

# Plot restaurants
# restaurants.plot(ax=ax, color="yellow", alpha=0.7, markersize=10)
plt.tight_layout()
plt.show()

