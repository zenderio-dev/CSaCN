import sys
from collections import defaultdict


def has_4cycle(n, edges):
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    # для каждой вершины w считаем пары её соседей (u, v);
    # если какая-то пара (u, v) встретилась у двух разных w - это и есть 4-цикл u-w1-v-w2-u
    seen = {}
    for w in adj:
        neigh = sorted(adj[w])
        for i in range(len(neigh)):
            for j in range(i + 1, len(neigh)):
                pair = (neigh[i], neigh[j])
                if pair in seen and seen[pair] != w:
                    return True
                seen[pair] = w
    return False


def main(path):
    tokens = iter(open(path).read().split())
    read = lambda: int(next(tokens))

    t = read()
    results = []
    for _ in range(t):
        n, m = read(), read()
        edges = [(read(), read()) for _ in range(m)]
        results.append("1" if has_4cycle(n, edges) else "-1")

    print(" ".join(results))
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("Результаты по 17 графам (1 - есть простой цикл длины 4, -1 - нет):\n")
        f.write(" ".join(results) + "\n")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "square_graph_dataset.txt")
