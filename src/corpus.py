"""Read the local workbook and versioned manifest; no network collection."""
from pathlib import Path
import pandas as pd

def load_corpus(data_xlsx, manifest_csv=None, scope='list', exclude_supplemented=False):
    manifest_csv = manifest_csv or Path(__file__).resolve().parents[1] / 'data/list_209_urls.csv'
    if scope not in ('list', 'all'):
        raise ValueError('scope must be list or all')
    d = pd.read_excel(data_xlsx, sheet_name='Combined Data')
    d = d[d['Source Type'].eq('Fragrantica')].copy()
    if d['Fragrantica URL'].isna().any():
        raise ValueError('Missing record URL')
    d = d.drop_duplicates('Fragrantica URL')
    valid = ~d['Fragrance Notes (All)'].fillna('').astype(str).str.strip().str.lower().isin(['','n/a','na','none','nan','-'])
    d = d[valid].copy()
    if scope == 'list':
        manifest = pd.read_csv(manifest_csv)
        urls = manifest['Fragrantica URL']
        if urls.isna().any() or urls.duplicated().any() or len(urls) != 209:
            raise ValueError('Expected a unique 209-URL manifest')
        missing = set(urls) - set(d['Fragrantica URL'])
        if missing:
            raise ValueError(f'{len(missing)} manifest records missing or without notes')
        d = d[d['Fragrantica URL'].isin(urls)]
    if exclude_supplemented:
        d = d[d['Supplemental Notes Source'].fillna('').astype(str).str.strip().eq('')]
    return d.sort_values('Fragrantica URL', kind='stable').reset_index(drop=True)
