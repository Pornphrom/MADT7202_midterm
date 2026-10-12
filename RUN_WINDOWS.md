# Run the original notebook on Windows

These instructions supplement the original README. The analysis code and saved original notebook are unchanged. Dependencies are not pinned to the author's original environment because it was not supplied. The independent numerical rerun log is in review/.

From the extracted repository root, in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:SCENT_DATA = 'D:/IS/outputs/combined_scrape_preview_metadata_filled/combined_scrape_preview_metadata_filled.xlsx'
$env:SCENT_LIST = 'D:/IS/ScentSelf_Collection_List_200.xlsx'
Set-Location notebooks
..\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute analysis.ipynb --output analysis.rerun.ipynb --ExecutePreprocessor.timeout=1800
```

Use your own actual paths. Both workbooks must be accessible locally and lawfully usable. No raw workbook is included. Execution writes the URL manifest and generated figure inside this repository. Numerical auditing in this review ran all numerical cells, including both 300-replicate bootstrap runs; figure rendering was not rerun. The supplied PDF figure was visually inspected.

## Publishing

Upload the extracted repository contents, not just this zip, to the chosen GitHub repository. The original notebook is `notebooks/analysis.ipynb`. Confirm the notebook renders and the intended reviewer can access it before copying its actual URL into the report. Published repository: https://github.com/Pornphrom/MADT7202_midterm . Notebook: https://github.com/Pornphrom/MADT7202_midterm/blob/main/notebooks/analysis.ipynb .

Read review/MADT7202_Rubric_Review_TH.md before submission. Reproducible numbers do not resolve the source permission, provenance, ranking-universe or interpretation issues described there.
