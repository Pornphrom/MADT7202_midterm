"""Update4 exploratory rule, revised 13 October 2026 after review.

Both ranks use the same graph nodes. Average ranks resolve ties; zero
betweenness never qualifies. Resample whole brands, without truncation.
This revision is not a preregistered or independently confirmed analysis.
"""
import collections
import random
import networkx as nx
from notes_clean import perfume_note_sets
from netlib import counts, generic_notes, build, betweenness, rank, sp

GENERIC_THR = 0.20
TOP_N = 10
STABLE_P = 0.80
MIN_GAP = 5
MAX_ANCHORS = 3
TARGET_DENSITY = 0.12
K_CANDIDATES = tuple(range(3, 11))
BOOT_B = 300
BOOT_SEED = 7
EPS = 1e-12

def analyse(sets, k, minf=None, weight='raw', generic_thr=GENERIC_THR):
    N, freq, pair = counts(sets)
    if not N:
        raise ValueError('Empty corpus')
    minf = max(5, round(0.02 * N)) if minf is None else minf
    high = generic_notes(N, freq, generic_thr)
    eligible = sorted(n for n, f in freq.items() if f >= minf and n not in high)
    G = build(N, freq, pair, eligible, k, weight, npmi_thr=0.1)
    G.remove_nodes_from(list(nx.isolates(G)))
    bc = betweenness(G)
    br = rank({n: round(v, 12) for n, v in bc.items()})
    fr = rank({n: freq[n] for n in G})
    bridges = {n for n in G if bc[n] > EPS and br[n] <= TOP_N}
    rho = sp(bc, {n: freq[n] for n in G}, sorted(G)) if len(G) > 1 and len(set(bc.values())) > 1 else None
    return dict(N=N, minf=minf, k=k, graph=G, bc=bc, br=br, fr=fr,
                freq=freq, excluded=sorted(high), eligible_count=len(eligible),
                distinct_notes=len(freq), bridges=bridges, rho=rho)

def choose_k(sets):
    candidates = []
    for k in K_CANDIDATES:
        a = analyse(sets, k)
        if a['graph'].number_of_edges():
            candidates.append((abs(nx.density(a['graph']) - TARGET_DENSITY), k))
    if not candidates:
        raise ValueError('No edges at any candidate cutoff')
    return min(candidates)[1]

def sample_brand_indices(groups, rng):
    """Sample B whole clusters for B unique brands; preserve multiplicity."""
    brands = sorted(groups)
    selected = [rng.choice(brands) for _ in brands]
    return [i for brand in selected for i in groups[brand]], selected

def apply_rule(df, level=1, boot_b=BOOT_B, weight='raw', k=None):
    df = df.sort_values('Fragrantica URL', kind='stable').reset_index(drop=True)
    sets = perfume_note_sets(df, level)
    k = choose_k(sets) if k is None else k
    a = analyse(sets, k, weight=weight)
    sweep = sorted(set([max(2, k-3), k, k+2]))
    sweeps = {cut: analyse(sets, cut, weight=weight) for cut in sweep}
    groups = collections.defaultdict(list)
    for i, brand in enumerate(df['Brand'].fillna('[unknown brand]').astype(str)):
        groups[brand].append(i)
    rng = random.Random(BOOT_SEED)
    hits = collections.Counter()
    sample_sizes = []
    for _ in range(boot_b):
        indices, _ = sample_brand_indices(groups, rng)
        sample_sizes.append(len(indices))
        b = analyse([sets[i] for i in indices], k, weight=weight)
        hits.update(b['bridges'])
    rows = []
    for n in sorted(a['graph'], key=lambda n: (a['br'][n], n)):
        p = hits[n] / boot_b
        gap = a['fr'][n] - a['br'][n]
        bridge = n in a['bridges']
        stable = p >= STABLE_P and all(n in b['bridges'] for b in sweeps.values())
        rows.append(dict(note=n, frequency=a['freq'][n], frequency_rank=a['fr'][n],
                         betweenness=a['bc'][n], betweenness_rank=a['br'][n],
                         rank_gap=gap, bootstrap_hits=hits[n], bootstrap_runs=boot_b,
                         bootstrap_p=p, bridge=bridge, stable=stable,
                         sweep_all=all(n in b['bridges'] for b in sweeps.values()),
                         passed=bridge and stable and gap >= MIN_GAP))
    passed = [r['note'] for r in rows if r['passed']][:MAX_ANCHORS]
    choices = [r for r in rows if r['bridge']]
    fallback = min(choices, key=lambda r: (-r['bootstrap_p'], r['betweenness_rank'], r['note']))['note'] if choices else None
    return dict(N=len(df), notes=a['distinct_notes'], eligible_notes=a['eligible_count'],
                excluded_notes=a['excluded'], weight=weight, min_frequency=a['minf'],
                k=k, nodes=len(a['graph']), edges=a['graph'].number_of_edges(),
                density=nx.density(a['graph']), spearman=a['rho'],
                components=sorted(map(len, nx.connected_components(a['graph'])), reverse=True),
                positive_bridges=sum(v > EPS for v in a['bc'].values()),
                rows=rows, passed=passed, fallback=fallback,
                bootstrap=dict(method='whole-brand cluster bootstrap', runs=boot_b,
                               seed=BOOT_SEED, brands=len(groups),
                               sample_size_min=min(sample_sizes), sample_size_max=max(sample_sizes)),
                sweep=[dict(k=cut, nodes=len(b['graph']), edges=b['graph'].number_of_edges(),
                            top_positive_bridges=sorted(b['bridges']),
                            gap_candidates=[n for n in sorted(b['bridges']) if b['fr'][n]-b['br'][n] >= MIN_GAP])
                       for cut, b in sweeps.items()])
