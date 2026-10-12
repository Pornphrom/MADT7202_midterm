import itertools, collections, math
import networkx as nx
import numpy as np
from scipy.stats import spearmanr


def counts(sets):
    N = len(sets)
    freq = collections.Counter(n for s in sets for n in s)
    pair = collections.Counter()
    for s in sets:
        for a, b in itertools.combinations(sorted(s), 2):
            pair[(a, b)] += 1
    return N, freq, pair


def npmi(N, freq, pair, a, b):
    w = pair[(a, b)] if (a, b) in pair else pair.get((b, a), 0)
    if w == 0:
        return -1.0
    pab = w / N
    pmi = math.log(pab / ((freq[a] / N) * (freq[b] / N)))
    return pmi / (-math.log(pab))


def generic_notes(N, freq, thr):
    return {n for n, f in freq.items() if f / N >= thr}


def build(N, freq, pair, nodes, k, weight="raw", npmi_thr=0.0):
    """Graph on `nodes`. weight='raw': keep edges raw count >= k, w=count.
    weight='npmi': keep edges with raw count >= k AND npmi > npmi_thr, w=npmi."""
    G = nx.Graph()
    G.add_nodes_from(nodes)
    ns = set(nodes)
    for (a, b), w in pair.items():
        if a in ns and b in ns and w >= k:
            if weight == "raw":
                G.add_edge(a, b, weight=float(w), count=w)
            else:
                v = npmi(N, freq, pair, a, b)
                if v > npmi_thr:
                    G.add_edge(a, b, weight=v, count=w)
    return G


def betweenness(G):
    H = nx.Graph()
    H.add_nodes_from(G.nodes())
    for a, b, d in G.edges(data=True):
        H.add_edge(a, b, dist=1.0 / d["weight"])
    return nx.betweenness_centrality(H, weight="dist", normalized=True)


def rank(d):
    items = sorted(d.items(), key=lambda x: (-x[1], x[0]))
    return {k: i + 1 for i, (k, _) in enumerate(items)}


def sp(a, b, keys):
    keys = list(keys)
    r = spearmanr([a[k] for k in keys], [b[k] for k in keys])
    return r.correlation
