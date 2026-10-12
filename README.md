# ScentSelf anchor-note analysis (MADT 7202 mid-term)

Question: which fragrance note should ScentSelf anchor its debut perfume on? Method: fragrance-note co-occurrence network (node = note, edge = two notes in the same perfume, weight = number of perfumes), generic notes (>=20% of perfumes) excluded before ranking, betweenness compared with frequency, and a pre-set decision rule with brand-cluster bootstrap.

## Data access (read this)
Raw Fragrantica data are **not** included. The pages were collected with Selenium (~Jul 2026). Fragrantica's Terms of Service (effective 14 Jan 2026, section 5.3) prohibit automated access without written permission; none was requested. The data were used for coursework only and are not republished. `data/list_209_urls.csv` lists the 209 perfumes analysed so the pages can be inspected manually.

See `docs/tos_evidence.md` for the clauses relied on (add your own dated screenshot there).

## Run
Place the two local workbooks outside the repo and point to them:
```
export SCENT_DATA=/path/combined_scrape_preview_metadata_filled.xlsx
export SCENT_LIST=/path/ScentSelf_Collection_List_200.xlsx
cd notebooks && jupyter nbconvert --to notebook --execute analysis.ipynb
```
`notebooks/analysis.ipynb` is already executed (outputs saved). Bootstrap seed = 7, B = 300.

## Files
- `src/decision_rule.py` — frozen decision rule (frozen 4 Oct 2026; amended 12 Oct 2026, see below)
- `src/netlib.py`, `src/notes_clean.py`, `src/corpus.py`, `src/figure.py` — graph, cleaning, loading, figure
- `results/` — rule output on the 209 list perfumes, the 1,780-perfume robustness set and the earlier 504-perfume exploratory file; figure
- Note: the force-directed layout in the figure can differ slightly between runs; the numbers do not.

## Amendment log
12 Oct 2026: notes with betweenness = 0 were previously ranked alphabetically and could pass the top-10 test spuriously; they now share the bottom rank and cannot count as bridges. No verdict changed.

## Limitations
Notes are declared pyramids on Fragrantica, not formulations; the 209-perfume list covers scent families unevenly; the pruned graph is small (20 nodes, 23 edges at k=6) and sensitive to the cutoff.

## Report source (one-page PDF)

`report/report.html` is the HTML source of the submitted one-page PDF and `report/render.py` renders it with Playwright/Chromium
(`pip install playwright`, then `python render.py <repo-url>`). `report/fig_page.png` is the figure produced by `src/figure.py`
(also in `results/`). The numbers in the report come from `notebooks/analysis.ipynb` and `results/*.txt`.

## Notebook and review status

- [Open the executed analysis notebook](notebooks/analysis.ipynb)
- [Windows run instructions](RUN_WINDOWS.md)
- [Rubric review and remaining corrections](review/MADT7202_Rubric_Review_TH.md)
- [Independent numerical rerun, 12 October 2026](review/numerical_rerun_2026-10-12.txt)

The original numerical analysis is preserved. Both corpus runs were independently reproduced; the original figure was inspected in the supplied report. The review identifies unresolved source-permission and provenance issues, ranking-universe differences, and limits to the robustness claim. Publication does not resolve these issues. Raw workbooks are not distributed. The repository contains the Update3 report source, not a revised final submission.
