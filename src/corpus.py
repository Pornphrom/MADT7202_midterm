"""Corpus loading. Raw data are NOT in this repository (see README: Fragrantica ToS)."""
import pandas as pd

def load_corpus(data_xlsx, list_xlsx, scope="list"):
    """scope: 'list' = the 209 ScentSelf-list perfumes; 'all' = every Fragrantica row with notes."""
    sp = pd.read_excel(list_xlsx, sheet_name="Scraped Preview")
    d = pd.read_excel(data_xlsx, sheet_name="Combined Data")
    d = d[d["Source Type"] == "Fragrantica"].drop_duplicates("Fragrantica URL")
    d = d[d["Fragrance Notes (All)"].notna()].reset_index(drop=True)
    in_list = set(sp.loc[sp["Collection List Match"] == "อยู่ในลิสต์ 200", "Fragrantica URL"])
    flag = d["Fragrantica URL"].isin(in_list)
    return d[flag].reset_index(drop=True) if scope == "list" else d
