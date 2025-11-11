import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, asin

# 1) Učitavanje grafa iz CSV fajla
# CSV treba imati kolone: city1, city2, distance_km
df = pd.read_csv("europe_capitals.csv")

# Kreiramo usmjereni ili ne-usmjereni graf (u ovom slučaju ne-usmjereni)
G = nx.Graph()

for _, row in df.iterrows():
    G.add_edge(row["city1"], row["city2"], distance_km=row["distance_km"])

print(f"Broj čvorova u grafu: {len(G.nodes())}")
print(f"Broj veza: {len(G.edges())}")

# 2) Unos od korisnika
start = input("Unesite početni grad: ")
goal = input("Unesite ciljni grad: ")

if start not in G.nodes() or goal not in G.nodes():
    raise ValueError("Grad nije u grafu!")

# 3) BFS put (najmanje čvorova u putanji)
path_bfs = nx.shortest_path(G, source=start, target=goal)
print("BFS ruta (najmanje koraka):", " → ".join(path_bfs))

#
# Preuzimanje koordinata za svaki grad (ako postoje u CSV-u)
coords = {}

for _, row in df.iterrows():
    if "lat" in df.columns and "lng" in df.columns:
        coords[row["city1"]] = (row.get("lat", None), row.get("lng", None))
        coords[row["city2"]] = (row.get("lat", None), row.get("lng", None))
#
#

#Funkcija za zračnu udaljenost
def haversine(a, b):
    if a not in coords or b not in coords:
        return 999999  # ako nema koordinata, heuristika postaje neupotrebljiva
    lat1, lon1 = coords[a]
    lat2, lon2 = coords[b]
    R = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    val = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2 * R * asin(sqrt(val))
#
#################################
#BEST-FIRST
#################################
import heapq

def best_first(graph, start, goal):
    visited = set()
    pq = []
    heapq.heappush(pq, (haversine(start, goal), start, [start]))

    while pq:
        _, node, path = heapq.heappop(pq)

        if node == goal:
            return path

        if node in visited:
            continue

        visited.add(node)

        for neighbor in graph.neighbors(node):
            new_path = path + [neighbor]
            heapq.heappush(pq, (haversine(neighbor, goal), neighbor, new_path))

    return None

#



# 4) Dijkstra put (najmanja ukupna udaljenost / cijena)
path_dijkstra = nx.dijkstra_path(G, source=start, target=goal, weight='distance_km')
distance = nx.dijkstra_path_length(G, source=start, target=goal, weight='distance_km')
print("Dijkstra ruta:", " → ".join(path_dijkstra))
print("Ukupna udaljenost:", distance, "km")

####POZIV BEST-FIRST####
path_best = best_first(G, start, goal)
print("Best-First ruta (heuristika):", " → ".join(path_best) if path_best else "Nema rute")

# 5) Vizualizacija
plt.figure(figsize=(10,6))

# Pozicija čvorova može biti slučajna: bolje je odvojiti ih prostorno
pos = nx.spring_layout(G, seed=42)

# Prikažemo osnovni graf
nx.draw(G, pos, with_labels=True, node_color="#b3d9ff", node_size=1000, font_size=9)

# Obojimo BFS put (plavo)
bfs_edges = list(zip(path_bfs, path_bfs[1:]))
nx.draw_networkx_edges(G, pos, edgelist=bfs_edges, width=3, edge_color="blue")

# Obojimo Dijkstra put (crveno)
dijkstra_edges = list(zip(path_dijkstra, path_dijkstra[1:]))
nx.draw_networkx_edges(G, pos, edgelist=dijkstra_edges, width=3, edge_color="red")

# Best-First put (zeleno)
if path_best:
    best_edges = list(zip(path_best, path_best[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=best_edges, width=3, edge_color="green")


plt.title(f"BFS (plavo) vs Dijkstra (crveno): {start} → {goal}")
plt.show()
