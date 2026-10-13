# MADT7202 Midterm - ScentSelf anchor-note analysis (Update4)

Which note should founder Palaloy use as the first ScentSelf test anchor?

- [One-page report (PDF)](report/MADT7202_MidTerm_Palaloy_Update4.pdf)
- [Executed notebook](notebooks/analysis.ipynb)
- [Computed results and sensitivity checks](results/update4_summary.json)
- [What changed and what remains unresolved](review/UPDATE4_CHANGES.md)
- [Windows instructions](RUN_WINDOWS.md)

## Current finding

No note meets every criterion in the primary corpus, the wider corpus, the NPMI check, or the corpus excluding supplemented records. On the main 209-perfume graph, Lemon is an experimental control only: stability 87.3%, rank gap 0.5. Peach has gap 6.5 but stability 25.3%. The wider corpus changes the fallback to Orange Blossom; the Lemon recommendation is not market-wide.

## Data and permission status

The author confirmed collection with Selenium from **30 August to 12 October 2026**. The primary workbook combines Fragrantica with Parfumo note supplements in 11/209 primary records (36/1,780 wider records). This is supplementation, not independent triangulation. Exact input and manifest SHA256 hashes are saved in the results JSON. Collection dates are author-reported, not independently timestamp-verified.

**Source permission remains unresolved.** Fragrantica ToS section 5.3 restricts unapproved automated access; written permission was not established. Parfumo supplement permission was not established either. Coursework use and not redistributing raw data do not grant permission. The assignment's permitted-source requirement is not yet satisfied. Resolve permission or replace the data and rerun before treating this as a compliant final submission. No new scraping is performed by this repository.

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

Update4 (13 October 2026) corrects the ranking population, tie handling and bootstrap procedure after review. It does not claim preregistration. Historical Update3 outputs and the earlier review are under `archive/update3/`; the full Update3 source is in Git history. Read `review/UPDATE4_CHANGES.md` for limitations that remain.
