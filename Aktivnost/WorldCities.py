'''
AKTIVNOST - ZADATAK
VJ2 - Vještačka inteligencija


Učitati worldcities.csv
Korisniku omogućiti izbor: države iz liste, minimalnog i maksimalnog broja slova u nazivu grada (3–10) i
minimalne populacije (100.000–10.000.000)

Filtrirati gradove prema kriterijima
Kreirati graf: čvor = grad (atributi: naziv, populacija, lat/lon)

svaka ivica spaja grad i 3 najbliža grada:   težina ivice = zračna udaljenost (km)

Spremiti ivice u filtered_graph_data.csv
Vizualno prikazati graf (čvorovi s imenima, ivice s km)

'''


import pandas as pd
import networkx as nx
import math
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1) Učitavanje CSV fajla
# ----------------------------------------------------------
df = pd.read_csv("worldcities.csv")

# Kontinenti koji postoje u datasetu
countries = sorted(df["country"].dropna().unique().tolist())

print("Dostupni kontinenti:")
for i, c in enumerate(countries, start=1):
    print(f"{i}. {c}")

# ----------------------------------------------------------
# 2) Unos korisnika: izbor države
# ----------------------------------------------------------
choice = int(input("\nIzaberite državu (1-{}): ".format(len(countries))))
selected_country = countries[choice - 1]

# ----------------------------------------------------------
# 3) Unos broja slova u nazivu grada
# ----------------------------------------------------------
min_letters = int(input("Minimalan broj slova (3-10): "))
max_letters = int(input("Maksimalan broj slova (3-10): "))

# ----------------------------------------------------------
# 4) Unos populacije
# ----------------------------------------------------------
min_pop = int(input("Minimalan broj stanovnika (100000-10000000): "))

# ----------------------------------------------------------
# 5) Filtriranje podataka
# ----------------------------------------------------------
filtered = df[
    (df["country"] == selected_country) &
    (df["population"] >= min_pop) &
    (df["city"].str.len() >= min_letters) &
    (df["city"].str.len() <= max_letters)
]

# Ako je malo gradova – upozorenje
if len(filtered) < 2:
    raise ValueError("Premalo gradova nakon filtriranja. Izaberite druge parametre!")

print("\nBroj gradova nakon filtriranja:", len(filtered))
# print(filtered[["city", "population"]].head()) #head pokazuje prvih 5
print(filtered[["city", "population"]])


# ----------------------------------------------------------
# 6) Izračunavanje udaljenosti između gradova
# Haversine formula za geografsku distancu u km
# ----------------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # radijus Zemlje (km)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat/2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return R * c


# ----------------------------------------------------------
# 7) Kreiranje grafa iz filtriranih podataka
# ----------------------------------------------------------
G = nx.Graph()

for _, row in filtered.iterrows():
    G.add_node(row["city"], population=row["population"],
               lat=row["lat"], lng=row["lng"])

# spajamo svaki grad sa 3 najbliža susjeda
cities = list(filtered.itertuples(index=False))

for a in cities:
    distances = []
    for b in cities:
        if a.city != b.city:
            dist = haversine(a.lat, a.lng, b.lat, b.lng)
            distances.append((b.city, dist))

    for neighbor, dist in sorted(distances, key=lambda x: x[1])[:3]:
        G.add_edge(a.city, neighbor, distance_km=round(dist, 1))


# ----------------------------------------------------------
# 8) Spremanje u novi CSV
# ----------------------------------------------------------
edges_list = [
    (u, v, data["distance_km"])
    for u, v, data in G.edges(data=True)
]

new_df = pd.DataFrame(edges_list, columns=["city1", "city2", "distance_km"])
new_df.to_csv("filtered_graph_data.csv", index=False)

print("\n✅ Novi CSV fajl kreiran: filtered_graph_data.csv")
print("✅ Graf kreiran sa", G.number_of_nodes(), "gradova i", G.number_of_edges(), "veza.")


# ----------------------------------------------------------
# 7) Vizualizacija grafa (PRIKAZ)
# ----------------------------------------------------------
plt.figure(figsize=(10, 6))

# pozicija = GPS lokacije → realan položaj na mapi
pos = {city: (data["lng"], data["lat"]) for city, data in G.nodes(data=True)}

nx.draw(
    G, pos,
    with_labels=True,
    node_size=900,
    node_color="#4db6ac",
    font_size=8,
    font_weight="bold"
)

# Dodaj oznake udaljenosti na ivice
edge_labels = {(u, v): f"{data['distance_km']} km" for u, v, data in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

plt.title("Graf filtriranih gradova i njihove zračne udaljenosti")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()