# Run Update4 on Windows

From the extracted repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:SCENT_DATA = 'D:/IS/outputs/combined_scrape_preview_metadata_filled/combined_scrape_preview_metadata_filled.xlsx'
Set-Location notebooks
..\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute analysis.ipynb --output analysis.rerun.ipynb --ExecutePreprocessor.timeout=1800
Set-Location ..
.\.venv\Scripts\python.exe report/render.py
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

Use your actual permitted workbook path. No separate SCENT_LIST workbook is needed: `data/list_209_urls.csv` is the selection manifest. Notebook execution writes JSON, CSV and figure files; rendering writes `report/MADT7202_MidTerm_Palaloy_Revised.pdf`. All data remains local. The source-permission issue described in README is unresolved.

Repository: https://github.com/Pornphrom/MADT7202_midterm

Notebook: https://github.com/Pornphrom/MADT7202_midterm/blob/main/notebooks/analysis.ipynb
