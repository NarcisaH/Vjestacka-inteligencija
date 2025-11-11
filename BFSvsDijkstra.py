import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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

# 4) Dijkstra put (najmanja ukupna udaljenost / cijena)
path_dijkstra = nx.dijkstra_path(G, source=start, target=goal, weight='distance_km')
distance = nx.dijkstra_path_length(G, source=start, target=goal, weight='distance_km')
print("Dijkstra ruta:", " → ".join(path_dijkstra))
print("Ukupna udaljenost:", distance, "km")

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

plt.title(f"BFS (plavo) vs Dijkstra (crveno): {start} → {goal}")
plt.show()
