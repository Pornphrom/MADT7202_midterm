"""FROZEN decision rule for the ScentSelf anchor-note question.

Frozen on 2026-10-04 (amended 2026-10-12, see analyse(): zero-betweenness notes are not bridges), BEFORE the remaining collection-list items were scraped.
Calibrated on the exploratory 504-perfume Step 2 Preview file (so the numbers
below were chosen after seeing that file; the confirmatory run on the completed
collection list must use them unchanged).

A note is a "differentiating anchor" only if ALL of the following hold
(note must be non-generic: appears in < GENERIC_THR of perfumes):
  1. BRIDGE      betweenness rank <= TOP_N at the primary k
  2. STABLE      in top-TOP_N in >= STABLE_P of brand-cluster bootstrap
                 resamples AND in top-TOP_N at every k in the sweep
  3. ADDED VALUE (frequency rank - betweenness rank) >= MIN_GAP at the primary k
At most MAX_ANCHORS notes are returned (ordered by betweenness).
If none qualifies -> FALLBACK: anchor on the most stable bridge note
(highest bootstrap P(top-TOP_N)) and report that its position comes from
popularity, not differentiation.

k selection (fixed rule, not tuned to rankings): among k in K_CANDIDATES choose
the one whose graph edge density is closest to TARGET_DENSITY (0.12 = the
density at the primary k=8 on the exploratory file). Sweep = (k-3, k, k+2).
min node frequency scales with corpus size: max(5, round(0.02 * N)).
"""
import collections, random, sys
from notes_clean import load, perfume_note_sets
from netlib import counts, generic_notes, build, betweenness, rank
import networkx as nx

GENERIC_THR = 0.20
TOP_N = 10
STABLE_P = 0.80
MIN_GAP = 5
MAX_ANCHORS = 3
TARGET_DENSITY = 0.12
K_CANDIDATES = (3, 4, 5, 6, 7, 8, 9, 10)
BOOT_B = 300
BOOT_SEED = 7


def analyse(sets, k, minf):
    N, freq, pair = counts(sets)
    gen = generic_notes(N, freq, GENERIC_THR)
    elig = [n for n, f in freq.items() if f >= minf and n not in gen]
    G = build(N, freq, pair, elig, k, "raw")
    G = G.subgraph([n for n in G if G.degree(n) > 0]).copy()
    if G.number_of_edges() == 0:
        return None
    bc = betweenness(G)
    fr = rank({n: freq[n] for n in elig})
    # AMENDMENT 2026-10-12: notes with betweenness == 0 are not bridges. Rank only
    # notes with bc > 0; zero-betweenness notes share the bottom rank (previously
    # they were ordered alphabetically and could pass the 'top-10' test spuriously).
    pos = rank({n: v for n, v in bc.items() if v > 1e-12})
    bottom = len(G) + 1
    br = {n: pos.get(n, bottom) for n in bc}
    return bc, br, fr, G, freq, gen


def choose_k(sets, minf):
    best = None
    for k in K_CANDIDATES:
        r = analyse(sets, k, minf)
        if r is None:
            continue
        G = r[3]
        d = nx.density(G)
        score = abs(d - TARGET_DENSITY)
        if best is None or score < best[0]:
            best = (score, k, d, G.number_of_nodes(), G.number_of_edges())
    return best


def apply_rule(df, level=1, verbose=True):
    sets = perfume_note_sets(df.reset_index(drop=True), level)
    brands = df["Brand"].tolist()
    N = len(sets)
    minf = max(5, round(0.02 * N))
    _, k, dens, nn, ne = choose_k(sets, minf)
    sweep = [max(2, k - 3), k, k + 2]
    bc, br, fr, G, freq, gen = analyse(sets, k, minf)
    if verbose:
        print(f"N={N} minf={minf} primary k={k} (density {dens:.3f}) nodes={nn} edges={ne} sweep={sweep}")
        print("generic:", sorted(gen))
    sweep_top = {}
    for kk in sweep:
        r = analyse(sets, kk, minf)
        sweep_top[kk] = {n for n, rk in r[1].items() if rk <= TOP_N} if r else set()
    by = collections.defaultdict(list)
    for i, b in enumerate(brands):
        by[b].append(i)
    bl = list(by)
    rng = random.Random(BOOT_SEED)
    hit = collections.Counter()
    for _ in range(BOOT_B):
        idx = []
        while len(idx) < N:
            idx += by[rng.choice(bl)]
        idx = idx[:N]
        r = analyse([sets[i] for i in idx], k, minf)
        if r is None:
            continue
        for n, rk in r[1].items():
            if rk <= TOP_N:
                hit[n] += 1
    rows = []
    for n, rk in sorted(br.items(), key=lambda x: x[1])[: 2 * TOP_N]:
        p = hit[n] / BOOT_B
        gap = fr[n] - rk
        c1 = rk <= TOP_N
        c2 = p >= STABLE_P and all(n in sweep_top[kk] for kk in sweep)
        c3 = gap >= MIN_GAP
        rows.append((n, rk, fr[n], gap, p, c1, c2, c3))
    passed = [r[0] for r in rows if r[5] and r[6] and r[7]][:MAX_ANCHORS]
    if verbose:
        print(f"{'note':22s} bc_rk fr_rk gap  P(top{TOP_N}) bridge stable value")
        for n, rk, f, g, p, c1, c2, c3 in rows:
            print(f"{n:22s} {rk:5d} {f:5d} {g:+4d}  {p:6.2f}   {c1!s:6} {c2!s:6} {c3!s}")
        if passed:
            print("ANCHORS:", passed)
        else:
            top = max(hit.items(), key=lambda x: x[1])
            print(f"NO ANCHOR QUALIFIES -> FALLBACK most stable bridge: {top[0]} (P={top[1]/BOOT_B:.2f})")
    return passed


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data.xlsx"
    apply_rule(load(path))
