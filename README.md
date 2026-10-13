# MADT7202 Midterm - ScentSelf anchor-note analysis

Which note should founder Palaloy use as the first ScentSelf test anchor?

- [One-page report (PDF)](report/MADT7202_MidTerm_Palaloy_Update4.pdf)
- [Executed notebook](notebooks/analysis.ipynb)
- [Computed results and sensitivity checks](results/update4_summary.json)
- [Method amendment](#method-amendment---13-october-2026)
- [Collection-date evidence](docs/collection_dates.md)
- [Windows instructions](RUN_WINDOWS.md)

## Current finding

No note meets every criterion in the primary corpus, the wider corpus, the NPMI check, or the corpus excluding supplemented records. On the main 209-perfume graph, Lemon is an experimental control only: stability 87.3%, rank gap 0.5. Peach has gap 6.5 but stability 25.3%. The wider corpus changes the fallback to Orange Blossom; the Lemon recommendation is not market-wide.

## Data and permission status

The author confirmed collection with Selenium from **30 August to 12 October 2026**. The primary workbook combines Fragrantica with Parfumo note supplements in 11/209 primary records (36/1,780 wider records). This is supplementation, not independent triangulation. Exact input and manifest SHA256 hashes are saved in the results JSON. Collection dates are author-reported, not independently timestamp-verified.

**Source permission remains unresolved.** Fragrantica ToS section 5.3 restricts unapproved automated access; written permission was not established. Parfumo ToS were not reviewed in this analysis, and supplement permission was not established either. Coursework use and not redistributing raw data do not grant permission. The assignment's permitted-source requirement is not yet satisfied. Resolve permission or replace the data and rerun before treating this as a compliant final submission. No new scraping is performed by this repository.

Raw workbooks, scraped page contents and credentials are not included. To rerun, use a locally accessible workbook you are entitled to use. The versioned URL manifest selects the 209 records without requiring the separate collection-list workbook.

## Reproduce

Install `requirements.txt` in a fresh environment and set `SCENT_DATA` to the local combined workbook. `requirements-tested.txt` records the numerical and rendering package versions used for this revision (Python version is in the results JSON).

```bash
python -m pip install -r requirements.txt
export SCENT_DATA=/absolute/path/combined_scrape_preview_metadata_filled.xlsx
cd notebooks
jupyter nbconvert --to notebook --execute analysis.ipynb --output analysis.rerun.ipynb --ExecutePreprocessor.timeout=1800
cd ..
python report/render.py
python -m unittest discover -s tests
```

Run the notebook from the repository root or `notebooks/`. It writes current JSON and metrics CSVs and creates the figure. `report/render.py` renders the PDF from those computed results. No Playwright or browser is required. The report link points to this repository.

## Method

Undirected note co-occurrence within a whole perfume; raw shared-perfume count as edge strength; shortest-path distance 1/strength. Exclude notes in >=20% of records as high-prevalence controls, then require frequency >=max(5, round(0.02*N)). Remove isolates after edge pruning. The cutoff is nearest to density 0.12 among k=3..10, a heuristic inherited from exploratory work. The wider corpus does not reach the target within that range.

Both prevalence and betweenness ranks use the surviving graph nodes. Ties use average rank; betweenness is rounded to 12 decimals for ranking. Zero betweenness is never a bridge. Qualification requires positive top-10 betweenness, rank gap >=5, top-10 in >=80% of 300 whole-brand bootstrap resamples (seed 7), and positive top-10 status across the cutoff sweep. An absent node counts as failure. Bootstrap samples draw as many brands as the original unique-brand count, with replacement and full cluster multiplicity; sample size varies. The frequency floor is recalculated for each sample; the absolute edge cutoff stays fixed. This is an exploratory heuristic, not a statistical test of centrality beyond popularity.

NPMI uses the primary raw cutoff and NPMI >0.1, with distance 1/NPMI, and reruns the full rule. Removing supplemented records is a sensitivity check, not reconstruction of their original note fields. The wider corpus overlaps the primary corpus, so it is not independent confirmation.

The pilot dates, 20 testers and 15-of-20 advance threshold in the report are a **proposed future plan**, conditional on resolving data permission/reanalysis. They are not measured results or a claimed completed study.

## Revision history

Update4 (13 October 2026) corrects the ranking population, tie handling and bootstrap procedure after review. It does not claim preregistration. Historical numerical Update3 outputs are under `archive/update3/`; the original source and prior review history remain in Git. Current results and amendments are documented here.

## Method amendment - 13 October 2026

This amendment was made **after examining the earlier results**. It replaces the earlier README/docstring claim of a frozen rule; the amended results are exploratory and must not be represented as preregistered confirmation. No numerical method changed during the subsequent report-editing pass on the same date.

| Item | Earlier method (Update3) | Amended method | Reason |
|---|---|---|---|
| Ranking population | Frequency ranks across 89 eligible notes; betweenness ranks on 20 retained graph nodes | Both ranks on the same 20 retained nodes in the primary graph | Make rank differences comparable |
| Ties | Alphabetical ordering for equal positive values/counts | Average ranks; round betweenness to 12 decimals for ties | Remove arbitrary alphabetical advantages |
| Bootstrap | Draw brand blocks until N rows, then truncate the final block | Draw B entire brands with replacement for B observed brands; preserve all repeated rows | Preserve whole clusters; sample size can vary |
| Interpretation | Stability could be read as universal support for Lemon | Main-catalogue control only; wider corpus selects Orange Blossom | Separate the shared no-pass verdict from a sample-specific control |

Peach changes from frequency rank 16 / betweenness rank 6 / gap 10 to **12.5 / 6 / 6.5**. Its resampled top-10 rate is **76/300 = 25.3%**, so it still fails the stability criterion. Lemon's frequency rank is 1.5 and betweenness rank is 1, with **262/300 = 87.3%** stability. No note passes the whole rule. These revised rates are newly computed, not rounded versions of old outputs.

The notebook's **Section 6** regenerates both tables printed in PDF Section 6. Notebook and renderer call the same `src/report_tables.py` function. The displayed tables are also saved as `results/section6_ranks.csv` and `results/section6_checks.csv`.

## Decision and feasible proposed schedule

Palaloy selects Lemon as a provisional control on 13 October, without a differentiation claim. By 23 October, prepare a costed brief for matched-base Lemon and Lemon + Peach prototypes and confirm tester availability. Target 30 October for a blinded, order-balanced 20-person pilot only if prototypes, participants and the source-permission/permitted-data rerun prerequisite are ready. Advance Peach only if at least 15 prefer it; otherwise retain control. The permission process has no assumed one-day turnaround. These are proposed actions, not completed work or calendar bookings.

## Project independence

The author stated that ScentSelf is an individual IS, not a team project. The team capstone industry has not yet been provided, so the separate-industry requirement is not asserted as verified. Being an individual IS alone does not establish a different domain.
