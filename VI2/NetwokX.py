import networkx as nx #!pip install networkx
import matplotlib.pyplot as plt

# Definišemo graf kao rječnik gdje je ključ grad,
# a vrijednost drugi rječnik: susjedni grad -> udaljenost
weighted_graph = {
    "Sarajevo": {"Zenica": 70, "Mostar": 120},
    "Zenica": {"Sarajevo": 70, "Tuzla": 90},
    "Mostar": {"Sarajevo": 120},
    "Tuzla": {"Zenica": 90}
}

# Kreiramo NetworkX graf
G = nx.Graph()

# Dodajemo ivice i udaljenosti u G
for city, neighbors in weighted_graph.items():
    for neighbor, cost in neighbors.items():
        # Dodajemo vezu između dva grada
        # cost se pohranjuje kao težina ivice
        G.add_edge(city, neighbor, weight=cost)

# Layout određuje raspored čvorova na ekranu
pos = nx.spring_layout(G)

# Crtamo čvorove i veze
nx.draw(G, pos, with_labels=True, node_size=2000, font_weight='bold')

# Dodajemo težine ivica na prikaz
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Prikazujemo grafički prozor
plt.show()
