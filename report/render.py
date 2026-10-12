import sys, pathlib
from playwright.sync_api import sync_playwright
repo = sys.argv[1] if len(sys.argv)>1 else "[add repo/notebook link before submitting]"
html = pathlib.Path("report.html").read_text().replace("@@REPO@@", repo)
pathlib.Path("_tmp.html").write_text(html)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto("file://"+str(pathlib.Path("_tmp.html").resolve()))
    pg.pdf(path="MADT7202_MidTerm_Palaloy.pdf",print_background=True,prefer_css_page_size=True)
    b.close()
