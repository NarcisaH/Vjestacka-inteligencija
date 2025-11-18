# ----------------------------------------------------------
# VJEŽBA 5 – OD GRAFA KA ML KLASIFIKACIJI
# ----------------------------------------------------------
'''
Klasifikacija gradova na osnovu grafa. Korištenjem datoteke worldcities.csv, potrebno je uraditi sljedeće:
 - Učitati sve gradove jedne države po izboru.
 - Nasumično odabrati 10 gradova i formirati podgraf, gdje su čvorovi gradovi,
 a ivice se formiraju povezivanjem svakog grada sa 2 njemu najbliža grada (račun zračne udaljenosti pomoću Haversine formule).
 - Za svaki grad (čvor) izračunati feature-e:
    - degree
    - prosječna udaljenost do susjeda
    - clustering koeficijent
    - centralnost (degree centrality)

 - Formirati ML dataset od prethodnih feature-a i dodati kolonu label, gdje:
    - 1 → grad je visoko povezan (degree ≥ prosječan degree)
    - 0 → ostali
 - Podijeliti dataset na trening i test (70% : 30%).
 - Trenirati i evaluirati dva modela:
    - Decision Tree classifier
    - Naive Bayes classifier
 - Ispisati accuracy i classification report  te feature importance i confusion matrix za oba modela i uporediti rezultate.
 - Vizualizovati stablo odlučivanja.
'''

#-----------------------------------------------RJEŠENJE-----------------------------------------------#
import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from math import radians, sin, cos, sqrt, asin
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sns


# ----------------------------------------------------------
# 1) Učitavanje CSV fajla (city, lat, lng)
# Učitavanje CSV datoteke i filtriranje države
# -------------------------------------------------
df = pd.read_csv("worldcities.csv")

print("Primjeri dostupnih država:")
print(", ".join(sorted(df["country"].unique())[:20]))

country = input("\nUnesite naziv države (npr. Croatia, Poland, Italy): ")
filtered = df[df["country"] == country][["city", "lat", "lng", "population"]].dropna()

if len(filtered) < 20:
    raise ValueError("Država ima premalo gradova. Izaberite veću.")

# 2) Haversine distanca
# ----------------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# ----------------------------------------------------------
# 3) Kreiranje grafa – povezivanje svakog grada sa 2 najbliža
# Odabir 10 gradova za podgraf
# -------------------------------------------------
cities = random.sample(list(filtered.itertuples(index=False)), 20)
print("\nIzabrani gradovi:", [c.city for c in cities])
# nasumični izbor 10 gradova → svako dobije drugačiji graf

G = nx.Graph()

# Dodaj čvorove
for c in cities:
    G.add_node(c.city, lat=c.lat, lng=c.lng, population=c.population)

# Poveži svaki grad sa 2 najbliža grada
for a in cities:
    distances = []
    for b in cities:
        if a.city != b.city:
            d = haversine(a.lat, a.lng, b.lat, b.lng)
            distances.append((b.city, d))
    for neighbor, dist in sorted(distances, key=lambda x: x[1])[:2]:
        G.add_edge(a.city, neighbor, distance_km=round(dist, 1))

# ----------------------------------------------------------
# 4) Feature engineering za svaki grad
# ----------------------------------------------------------
feature_rows = []

centrality_dict = nx.degree_centrality(G) # normaliziran broj veza: degree / (N-1)
clustering_dict = nx.clustering(G)

for city in G.nodes():
    degree = G.degree(city)
    neighbor_distances = [G[city][nbr]["distance_km"] for nbr in G.neighbors(city)]
    avg_distance = np.mean(neighbor_distances)
    centrality = centrality_dict[city]
    clustering = clustering_dict[city]

    feature_rows.append([
        city,
        degree,
        avg_distance,
        clustering,
        centrality
    ])

df_feat = pd.DataFrame(
    feature_rows,
    columns=["city", "degree", "avg_distance", "clustering", "centrality"]
)

print("\nFEATURE TABLE:\n", df_feat)

# ----------------------------------------------------------
# 5) Kreiranje labela (0/1)
# kriterij: degree >= prosjek degree-a
# ----------------------------------------------------------
threshold = df_feat["degree"].mean()
df_feat["label"] = (df_feat["degree"] >= threshold).astype(int)

# ----------------------------------------------------------
# 6) Priprema podataka za ML modele
# ----------------------------------------------------------
X = df_feat[["degree", "avg_distance", "clustering", "centrality"]]
y = df_feat["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# ----------------------------------------------------------
# 7) Decision Tree model
# ----------------------------------------------------------
dt_model = DecisionTreeClassifier(max_depth=4)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)

print("\n--- DECISION TREE ---")
print("Accuracy:", accuracy_score(y_test, dt_pred))
print(classification_report(y_test, dt_pred))

# Feature importance
print("\n--- FEATURE IMPORTANCE (Decision Tree) ---")
for feat, val in zip(X.columns, dt_model.feature_importances_):
    print(f"{feat}: {val:.3f}")

# Confusion matrix
print("\n--- CONFUSION MATRIX (Decision Tree) ---")
print(confusion_matrix(y_test, dt_pred))

# ----------------------------------------------------------
# 8) Naive Bayes model
# ----------------------------------------------------------
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)
nb_pred = nb_model.predict(X_test)

print("\n--- NAIVE BAYES ---")
print("Accuracy:", accuracy_score(y_test, nb_pred))
print(classification_report(y_test, nb_pred))

# Confusion matrix
print("\n--- CONFUSION MATRIX (Naive Bayes) ---")
print(confusion_matrix(y_test, nb_pred))


# ---- Confusion Matrix with labels ---- #
cm_dt = confusion_matrix(y_test, dt_pred)
plt.figure(figsize=(4,3))
sns.heatmap(cm_dt, annot=True, cmap="Blues", fmt="d",
            xticklabels=["low (0)","high (1)"],
            yticklabels=["low (0)","high (1)"])
plt.title("Decision Tree – Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# ---- For Naive Bayes ---- #
cm_nb = confusion_matrix(y_test, nb_pred)
plt.figure(figsize=(4,3))
sns.heatmap(cm_nb, annot=True, cmap="Purples", fmt="d",
            xticklabels=["low (0)","high (1)"],
            yticklabels=["low (0)","high (1)"])
plt.title("Naive Bayes – Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# ----------------------------------------------------------
# 9) Vizualizacija stabla
# ----------------------------------------------------------
plt.figure(figsize=(14, 6))
plot_tree(dt_model, filled=True, feature_names=X.columns, class_names=["low", "high"])
plt.title("Decision Tree – europe_capitals")
plt.show()

