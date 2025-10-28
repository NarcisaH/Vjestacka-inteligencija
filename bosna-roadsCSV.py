import csv
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

G = nx.Graph()

# Učitavanje iz CSV fajla
with open("bosna_roads.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        a = row["city1"]
        b = row["city2"]
        dist = float(row["distance_km"])
        G.add_edge(a, b, weight=dist)

print("Broj gradova:", G.number_of_nodes())
print("Broj cesta:", G.number_of_edges())



# Vizualizacija grafa
pos = nx.spring_layout(G, seed=42)  # opcionalno: stabilniji raspored čvorova

plt.figure(figsize=(12, 8))

# Čvorovi i ivice
nx.draw_networkx_nodes(G, pos, node_size=500, node_color="lightblue")
nx.draw_networkx_edges(G, pos)

# Oznake gradova
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

# Težine (distance_km)
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


plt.title("Mreža gradova: Bosna i Hercegovina")
plt.axis("off")
plt.tight_layout()
plt.show()


#MATRICA SUSJEDSTVA#
# Čvorovi u određenom poretku (već postoje iz tvog koda)
nodes = list(G.nodes())

# Matrica susjedstva (1/0 prikaz bez težina)
A = nx.to_numpy_array(G, nodelist=nodes, weight=None)

# Kreiranje DataFrame-a za ljepši prikaz
df = pd.DataFrame(A, index=nodes, columns=nodes)

print("\nMatrica susjedstva (sa nazivima gradova):")
print(df)
print("-------------------------------------------")
print("Matrica težina:")
#MATRICA TEŽINA
W = nx.to_numpy_array(G, nodelist=nodes, weight="weight")
# Kreiranje DataFrame-a za ljepši prikaz
dfw = pd.DataFrame(W, index=nodes, columns=nodes)
print(dfw)
