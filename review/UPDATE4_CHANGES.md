# Update4 - changes and remaining requirements

Revised on 13 October 2026 in response to the author's request.

## Corrected

1. Both ranks now use the same surviving graph nodes. Average ties remove arbitrary alphabetical advantages. Peach's primary gap is 6.5 (frequency rank 12.5 minus betweenness rank 6), rather than the old gap 10. The earlier review's gap 7 used the old alphabetical tie rule; 6.5 is the final revised method.
2. Bootstrap draws complete brand clusters with replacement. It no longer truncates the final brand. Main Lemon stability is 262/300 = 87.3%; Peach is 76/300 = 25.3%. Sample sizes vary by design. All four analyses were recomputed, not relabelled from Update3.
3. Fragrantica plus Parfumo field supplementation is disclosed (11/209 and 36/1,780). The full rule was rerun after removing the 11 supplemented primary records (N=198); none qualifies.
4. Full NPMI sensitivity now includes bootstrap and decision outcomes, not only membership of the original bridges. The NPMI graph has 20 nodes/22 edges and changes ranks; Lemon's stability is 77.0% in that check, below the 80% criterion, though it remains the most stable provisional control. No differentiating note qualifies.
5. The wider corpus has 80 nodes/529 edges at k=10; its fallback is Orange Blossom. Lemon has 16.0% stability there. The shared conclusion is no qualifying differentiating anchor, not a universal Lemon recommendation.
6. Collection dates are 30 August-12 October 2026, explicitly confirmed by the author. The prior approximate July date and unknown-start wording are superseded.
7. The one-page report has actual result tables, a readable graph, proposed dated actions, a pilot decision threshold and a working repo link. New figure colours distinguish positive from zero betweenness and make no scent-family inference.
8. The notebook reads the committed 209-URL manifest directly. It records the input hash and software versions. Current JSON, CSV, notebook outputs and report are aligned. Obsolete results are clearly archived.

## Unresolved; do not claim these are fixed

- Written permission for the scraped Fragrantica corpus has not been established. Parfumo permission is also unverified. The assignment's permitted-source condition remains unmet. Obtain suitable permission or replace the dataset and rerun; do not relabel it as permitted.
- The author described ScentSelf as an individual IS rather than a team project. Compliance with the separate-industry condition still depends on the actual class team project; its industry was not supplied.
- The selected list is purposive, source families are uneven, and declared notes are not consumer preferences or a formula. The density search and thresholds are exploratory heuristics, revised after seeing results. No preregistration is claimed.
- Exact count k is held fixed in bootstrap despite variable record counts; prevalence exclusions and the frequency floor are recomputed. Stability remains conditional on this construction. The wider set overlaps the main set.
- The proposed tester plan is not yet performed. Its dates and sample size are a suggested schedule, contingent on source permission/reanalysis, participant availability and prototype readiness. No external task or calendar event was created.

## Checks performed

- Executed and validated the revised notebook, including 300 resamples for each of four analyses.
- Four focused tests cover average ties, common ranking population, zero-centrality exclusion, intact resampled clusters, and a degenerate NPMI pair.
- Re-rendered the graph and visually reviewed the one-page PDF. PDF text is at least 10 pt with 45 pt margins (1.5875 cm).
