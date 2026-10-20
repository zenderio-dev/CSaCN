import glob
import os
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt

# собираем общий граф из отдельных эго-сетей Facebook (данные SNAP)
G = nx.Graph()
for edges_file in glob.glob("social-networks/*.edges"):
    ego = int(os.path.basename(edges_file).split(".")[0])
    neighbors = [int(line.split()[0]) for line in open(edges_file.replace(".edges", ".feat"))]
    G.add_edges_from((ego, n) for n in neighbors)  # эго дружит со всеми своими соседями
    G.add_edges_from(tuple(map(int, line.split())) for line in open(edges_file))  # дружба между соседями

nx.write_edgelist(G, "facebook_combined.txt", data=False)

# длина кратчайшего пути между каждой парой вершин (BFS от каждой вершины)
lengths = Counter()
for u, dist in nx.all_pairs_shortest_path_length(G):
    for v, d in dist.items():
        if v > u:  # считаем каждую пару один раз, пропускаем пару (u, u) с d=0
            lengths[d] += 1

total = sum(lengths.values())
distances = sorted(lengths)

cum = 0
median = None
for d in distances:
    cum += lengths[d]
    if cum >= total / 2:
        median = d
        break

mode = max(lengths, key=lengths.get)
mean = sum(d * c for d, c in lengths.items()) / total

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(f"Вершин: {G.number_of_nodes()}, рёбер: {G.number_of_edges()}\n")
    f.write(f"Связных пар вершин: {total}\n\n")
    f.write("длина_пути\tчисло_пар\n")
    for d in distances:
        f.write(f"{d}\t{lengths[d]}\n")
    f.write(f"\nСреднее: {mean:.3f}\nМедиана: {median}\nМода: {mode}\n")

plt.bar(distances, [lengths[d] for d in distances])
plt.xlabel("Длина кратчайшего пути")
plt.ylabel("Число пар вершин")
plt.title("Распределение длин кратчайших путей (Facebook ego-network)")
plt.savefig("histogram.png", dpi=150)

print(f"Среднее: {mean:.3f}, медиана: {median}, мода: {mode}")
