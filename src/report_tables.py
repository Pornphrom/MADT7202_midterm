"""One definition of the displayed Section 6 tables for notebook and PDF."""
def section6_tables(summary):
    primary = summary['primary']
    checks = summary['checks']
    ranks = [['Note', 'Freq. rank', 'BC rank', 'Gap', 'Top-10 rate']]
    for name in ('Lemon', 'Peach'):
        row = next(r for r in primary['rows'] if r['note'] == name)
        ranks.append([name, f'{row["frequency_rank"]:g}',
                      f'{row["betweenness_rank"]:g}', f'{row["rank_gap"]:g}',
                      f'{row["bootstrap_p"]:.1%}'])
    robustness = [['Check', 'Pass', 'Control']]
    for label, result in [
        (f'Raw ({primary["edges"]} edges)',primary),
        (f'NPMI ({checks["npmi"]["edges"]} edges)',checks['npmi']),
        (f'No supplements ({checks["without_supplemented"]["N"]})',checks['without_supplemented']),
        (f'Wider ({checks["wider"]["N"]:,})',checks['wider'])]:
        robustness.append([label, str(len(result['passed'])), result['fallback']])
    return ranks, robustness
