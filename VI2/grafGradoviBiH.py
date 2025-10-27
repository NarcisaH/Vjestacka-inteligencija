import math
import networkx as nx
import matplotlib.pyplot as plt

# -----------------------------
# 1) Gradovi sa njihovim (x, y) koordinatama u "mapi"
# Ovo nisu GPS koordinate – već uprošćene da mapa bude pregledna
# -----------------------------
positions = {
    "Bihać": (1, 6),
    "Cazin": (2, 6.5),
    "Sanski Most": (3, 5.3),
    "Prijedor": (4, 6),
    "Banja Luka": (5, 6),
    "Gradiška": (4.8, 6.8),
    "Doboj": (7, 5.3),
    "Zenica": (8, 4.8),
    "Tuzla": (9, 5.5),
    "Bijeljina": (10, 6),
    "Sarajevo": (10, 3.8),
    "Goražde": (11, 3),
    "Mostar": (9, 2),
    "Čapljina": (8.8, 1.3),
    "Trebinje": (11, 1),
    "Bugojno": (7.5, 3.5),
    "Travnik": (7.8, 4.4),
    "Livno": (5.5, 2),
    "Konjic": (9.3, 2.8),
    "Jajce": (6.7, 4.6),
    "Zvornik": (10, 5),
    "Srebrenik": (9.2, 5.6)
}

# -----------------------------
# 2) Funkcija za računanje udaljenosti
# (Euklidska distanca na našoj “mapi” → km skala ~ 25 km po jedinici)
# -----------------------------
def distance_km(a, b):
    x1, y1 = positions[a]
    x2, y2 = positions[b]
    return round(math.hypot(x1 - x2, y1 - y2) * 25, 2)


# -----------------------------
# 3) Povezanost gradova po stvarnim cestama
# (kraće i glavne cestovne rute)
# -----------------------------
roads = [
    ("Bihać", "Cazin"),
    ("Cazin", "Sanski Most"),
    ("Sanski Most", "Prijedor"),
    ("Prijedor", "Banja Luka"),
    ("Banja Luka", "Doboj"),
    ("Doboj", "Tuzla"),
    ("Tuzla", "Srebrenik"),
    ("Srebrenik", "Zvornik"),
    ("Zvornik", "Bijeljina"),
    ("Zenica", "Sarajevo"),
    ("Sarajevo", "Konjic"),
    ("Konjic", "Mostar"),
    ("Mostar", "Čapljina"),
    ("Čapljina", "Trebinje"),
    ("Jajce", "Bugojno"),
    ("Bugojno", "Mostar"),
    ("Bugojno", "Livno"),
    ("Travnik", "Zenica"),
    ("Doboj", "Tuzla"),
    ("Jajce", "Travnik"),
    ("Zenica", "Doboj"),
    ("Sarajevo", "Goražde")
]


# -----------------------------
# 4) Kreiramo graf sa težinama
# -----------------------------
G = nx.Graph()

for city, coord in positions.items():
    G.add_node(city, pos=coord)

for a, b in roads:
    G.add_edge(a, b, weight=distance_km(a, b))


# -----------------------------
# 5) Vizualizacija
# -----------------------------
plt.figure(figsize=(9, 7))

# Koordinate za prikaz
pos = nx.get_node_attributes(G, 'pos')

# Vizualni prikaz čvorova i ivica
nx.draw(
    G, pos,
    with_labels=True,
    node_size=1000,
    node_color="#8ecae6",
    font_weight="bold",
    font_size=8,
    width=1.8
)

# Prikaz težina (km)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=7
)

plt.title("Graf cestovne povezanosti BiH — stvarni gradovi i udaljenosti")
plt.axis("off")
plt.show()

# -----------------------------
# 6) Brza statistika mreže
# -----------------------------
print("Broj gradova:", G.number_of_nodes())
print("Broj cesta:", G.number_of_edges())
avg_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
print("Prosječan stepen:", round(avg_degree, 2))
