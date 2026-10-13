"""Render the one-page report from computed Update4 JSON.

Run: python report/render_update4.py [output.pdf]
Requires reportlab and results/fig_page.png. No raw data is read here.
"""
from pathlib import Path
import sys, json, html
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

ROOT=Path(__file__).resolve().parents[1]
S=json.loads((ROOT/'results/update4_summary.json').read_text(encoding='utf-8'))
P=S['primary']; C=S['checks']
def row(result,note): return next(r for r in result['rows'] if r['note']==note)
L=row(P,'Lemon'); Q=row(P,'Peach'); WL=row(C['wider'],'Lemon')
URL='https://github.com/Pornphrom/MADT7202_midterm'
W,H=A4; M=45; WIDTH=W-2*M; GAP=12; COL=(WIDTH-GAP)/2
INK=colors.HexColor('#172538'); BLUE=colors.HexColor('#125687'); LINE=colors.HexColor('#cad5df')
BODY=ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=11.4,textColor=INK)
CELL=ParagraphStyle('cell',parent=BODY,leading=11.1)
TITLE=ParagraphStyle('title',parent=BODY,fontName='Helvetica-Bold',fontSize=13.1,leading=15.2)
HEAD=ParagraphStyle('head',parent=BODY,fontName='Helvetica-Bold',fontSize=10.2,leading=12.2,textColor=BLUE)

def para(c,text,x,y,width=WIDTH,style=BODY,gap=2):
    p=Paragraph(text,style); _,height=p.wrap(width,1000)
    p.drawOn(c,x,y-height)
    return y-height-gap
def heading(c,text,x,y,width=WIDTH):
    y=para(c,text,x,y,width,HEAD,1)
    c.setStrokeColor(LINE);c.setLineWidth(.45);c.line(x,y,x+width,y)
    return y-3
def table(c,rows,x,y,width,widths=None,header=False):
    rows=[[Paragraph(str(v),CELL) for v in r] for r in rows]
    t=Table(rows,colWidths=widths or [55,width-55],hAlign='LEFT')
    commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,LINE),
              ('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
              ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]
    commands.append(('BACKGROUND',(0,0),(-1,0) if header else (0,-1),colors.HexColor('#edf3f8')))
    t.setStyle(TableStyle(commands));_,height=t.wrap(width,1000);t.drawOn(c,x,y-height)
    return y-height-3

def render(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(path),pagesize=A4)
    c.setTitle('MADT7202 Midterm - Palaloy - Update4')
    c.setAuthor('Palaloy')
    y=H-M
    y=para(c,'Which note should ScentSelf use as its first test anchor?',M,y,style=TITLE)
    y=para(c,f'Palaloy | MADT7202 | Update4 | <link href="{URL}" color="#125687">Code, notebook &amp; results: Pornphrom/MADT7202_midterm</link>',M,y)
    y=heading(c,'1  The decision',M,y)
    y=para(c,'Palaloy, ScentSelf founder, will select a test anchor. A stable bridge that outranks prevalence can support differentiation; otherwise use only a provisional control, with no positioning claim.',M,y)
    y=heading(c,'2  Why a network',M,y)
    y=para(c,'Counts show common notes; weighted shortest paths show which notes connect note groups. Comparing betweenness and prevalence ranks distinguishes these roles.',M,y)
    left=heading(c,'3  Data',M,y,COL);right=heading(c,'4  Graph construction',M+COL+GAP,y,COL)
    left=table(c,[
        ['<b>Sources</b>','Fragrantica; Parfumo note supplements in <b>11/209</b>. Selenium; offline note parsing.'],
        ['<b>Period</b>','30 Aug-12 Oct 2026 (author-confirmed).'],
        ['<b>Volume</b>',f'<b>{P["N"]}</b> perfumes, {P["notes"]} notes; wider set: <b>1,780</b>. URL manifest in repo.'],
        ['<b>Access</b>','Permission not established. Fragrantica <link href="https://www.fragrantica.com/terms-of-service.phtml" color="#125687">ToS 5.3</link> restricts unapproved automation. Raw data not shared; source requirement unresolved.'],
        ['<b>Sampling</b>','Purposive list; Floral 61 vs Leather 4. Not a market sample; supplements are not triangulation.'],
    ],M,left,COL)
    right=table(c,[
        ['<b>Nodes / edges</b>','Cleaned notes / notes listed in the same perfume. No seed-note filter.'],
        ['<b>Weight</b>','Count favours repeated pairings; distance = 1/count. NPMI &gt;0.1 checks prevalence.'],
        ['<b>Pruning</b>','Exclude prevalence &gt;=20% (10 notes); retain frequency &gt;=5 (89 notes). Drop edges &lt;6 and isolates.'],
        ['<b>Choice</b>',f'k=6: nearest density 0.12 among k=3..10; <b>{P["nodes"]} nodes / {P["edges"]} edges</b>. k=8 leaves 3 nodes / 2 edges.'],
        ['<b>Rule</b>','Average ranks on same nodes; gap &gt;=5, positive top-10, &gt;=80% of 300 whole-brand resamples; top-10 at k=3,6,8.'],
    ],M+COL+GAP,right,COL)
    y=min(left,right)-1
    y=heading(c,'5  The network',M,y)
    image_h=WIDTH*2.4/7.0
    c.drawImage(str(ROOT/'results/fig_page.png'),M,y-image_h,width=WIDTH,height=image_h,mask='auto')
    y-=image_h
    y=para(c,'Node size = betweenness; blue = positive betweenness; line width = pair count.',M,y)
    left=heading(c,'6  Findings',M,y,COL);right=heading(c,'7  Recommended action (proposed)',M+COL+GAP,y,COL)
    left=table(c,[
        ['<b>Note</b>','<b>Freq.<br/>rank</b>','<b>BC<br/>rank</b>','<b>Gap</b>','<b>Top-10<br/>rate</b>'],
        ['Lemon',f'{L["frequency_rank"]:g}',f'{L["betweenness_rank"]:g}',f'{L["rank_gap"]:g}',f'{L["bootstrap_p"]:.1%}'],
        ['Peach',f'{Q["frequency_rank"]:g}',f'{Q["betweenness_rank"]:g}',f'{Q["rank_gap"]:g}',f'{Q["bootstrap_p"]:.1%}'],
    ],M,left,COL,[52,43,38,35,COL-168],True)
    left=para(c,f'<b>1.</b> Peach has a {Q["rank_gap"]:g}-rank advantage but only {Q["bootstrap_p"]:.1%} stability. Lemon is stable ({L["bootstrap_p"]:.1%}) with little rank advantage. Neither qualifies.',M,left,COL)
    # Compact robustness evidence on-page; full per-node results remain in notebook.
    left=table(c,[
        ['<b>Check</b>','<b>Pass</b>','<b>Control</b>'],
        [f'Raw ({P["edges"]} edges)',len(P['passed']),P['fallback']],
        [f'NPMI ({C["npmi"]["edges"]} edges)',len(C['npmi']['passed']),C['npmi']['fallback']],
        ['No supplements (198)',len(C['without_supplemented']['passed']),C['without_supplemented']['fallback']],
        ['Wider (1,780)',len(C['wider']['passed']),C['wider']['fallback']],
    ],M,left,COL,[COL-115,32,83],True)
    left=para(c,'<b>2.</b> Zero anchors pass all criteria in each check; the wider catalogue changes the control. Keep Lemon specific to the curated list.',M,left,COL)
    right=para(c,'<b>13 Oct - Palaloy:</b> resolve source permission or select permitted replacement data and rerun before committing to the test.',M+COL+GAP,right,COL)
    right=para(c,'<b>14 Oct, if cleared:</b> brief matched-base prototypes: Lemon control vs Lemon + Peach; hold concentration constant.',M+COL+GAP,right,COL)
    right=para(c,'<b>15 Oct, if ready:</b> run a blinded, order-balanced pilot with 20 testers. Advance Peach only if at least 15 prefer it; otherwise retain the control. Postpone if prerequisites fail.',M+COL+GAP,right,COL)
    right=heading(c,'8  What would change my mind',M+COL+GAP,right,COL)
    right=para(c,'Declared-note co-occurrence is not liking or a recipe. The graph changes with cutoff and catalogue. A permitted, broader sample that changes the control, or failure in the blinded pilot, would change the recommendation.',M+COL+GAP,right,COL)
    bottom=min(left,right)
    if bottom<M:
        raise ValueError(f'Content crosses {M}pt margin: bottom={bottom:.1f}. Revise content, not font size.')
    c.save()
    print(f'PDF saved: {path}; lowest content y={bottom:.1f} pt; margin={M} pt')
    return {'bottom_y':bottom,'margin_pt':M,'pages':1,'font_min_pt':10}

if __name__=='__main__':
    render(sys.argv[1] if len(sys.argv)>1 else ROOT/'report/MADT7202_MidTerm_Palaloy_Update4.pdf')
