"""Note-name cleaning for the Fragrantica export.

Level 1 (primary): fix parsing artefacts + spelling + obvious synonyms only.
Level 2 (sensitivity): additionally roll origin/variety variants up to the base
note (e.g. Sicilian Lemon -> Lemon, Damask Rose -> Rose), so the report can
state how much the result depends on note merging.
"""
import re
import pandas as pd

L1_SYNONYMS = {
    "vanille": "Vanilla", "vanila": "Vanilla",
    "ylang ylang": "Ylang-Ylang",
    "lily of the valley": "Lily-of-the-Valley",
    "mandarin": "Mandarin Orange",
    "virginian cedar": "Virginia Cedar",
    "agarwood": "Oud", "oud": "Oud",
    "sandal": "Sandalwood",
}

ORIGIN_WORDS = (
    "sicilian|italian|amalfi|calabrian|egyptian|indian|indonesian|haitian|tahitian|"
    "madagascar|madagascan|bourbon|bulgarian|turkish|moroccan|australian|mysore|atlas|"
    "texas|virginia|virginian|brazilian|african|tunisian|french|spanish|"
    "damask|may|natural|sambac|absolute|extract"
)

L2_EXACT = {
    "cedarwood": "Cedar", "virginia cedar": "Cedar",
    "jasmine sambac": "Jasmine",
    "vanilla bean": "Vanilla",
    "egyptian musk": "Musk", "cashmere musk": "Musk", "natural musk": "Musk", "black musk": "Musk",
    "iris pallida": "Iris", "orris": "Iris", "orris root": "Iris",
    "lily": "Lily-of-the-Valley",
    "indonesian patchouli leaf": "Patchouli",
}


def clean_token(tok: str) -> str:
    t = tok.strip()
    # parsing artefact: "Vanilla. The fragrance features ..." / "... winner of award ..."
    t = re.split(r"\.\s", t)[0].rstrip(".")
    t = t.replace("™", "").replace("®", "")
    t = re.sub(r"\s+", " ", t).strip()
    # parentheticals: keep the base note
    t = re.sub(r"\s*\([^)]*\)", "", t).strip() if t.lower() != "agarwood (oud)" else "Agarwood"
    t = t.replace("`", "'")
    return t


def canon_l1(t: str) -> str:
    key = t.lower()
    return L1_SYNONYMS.get(key, t if t != t.lower() else t.title())


def canon_l2(t: str) -> str:
    t1 = canon_l1(t)
    key = t1.lower()
    if key in L2_EXACT:
        return L2_EXACT[key]
    stripped = re.sub(rf"^(?:{ORIGIN_WORDS})\s+", "", t1, flags=re.I)
    stripped = re.sub(rf"\s+(?:{ORIGIN_WORDS})$", "", stripped, flags=re.I)
    if stripped.lower() != key and stripped:
        stripped = canon_l1(stripped)
        if stripped.lower() in L2_EXACT:
            return L2_EXACT[stripped.lower()]
        return stripped
    return t1


def perfume_note_sets(df: pd.DataFrame, level: int = 1):
    canon = canon_l1 if level == 1 else canon_l2
    out = []
    for s in df["Fragrance Notes (All)"]:
        toks = [canon(clean_token(x)) for x in str(s).split(",") if x.strip()]
        # drop award/marketing text that leaked into the note list
        toks = [t for t in toks if t and not re.search(r"fifi|award|\b(19|20)\d\d\b", t, re.I)]
        out.append(sorted(set(toks)))
    return out


def load(path="data.xlsx"):
    df = pd.read_excel(path, sheet_name="Parsed Data")
    df = df.drop_duplicates(["Brand", "Perfume Name"]).reset_index(drop=True)
    df["family"] = df["Scent Family Primary"].str.split().str[0]
    return df
