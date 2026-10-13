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
sys.path.insert(0,str(ROOT/'src'))
from report_tables import section6_tables
S=json.loads((ROOT/'results/update4_summary.json').read_text(encoding='utf-8'))
P=S['primary']; C=S['checks']
RANK_TABLE,CHECK_TABLE=section6_tables(S)
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
    c.setTitle('MADT7202 Midterm - Palaloy')
    c.setAuthor('Palaloy')
    y=H-M
    y=para(c,'Which note should ScentSelf use as its first test anchor?',M,y,style=TITLE)
    y=para(c,f'Palaloy | MADT7202 | <link href="{URL}" color="#125687">Code, notebook &amp; results: Pornphrom/MADT7202_midterm</link>',M,y)
    y=heading(c,'1  The decision',M,y)
    y=para(c,'Palaloy, ScentSelf founder, will select a test anchor. A stable bridge that outranks prevalence can support differentiation; otherwise use only a provisional control, with no positioning claim.',M,y)
    y=heading(c,'2  Why a network',M,y)
    y=para(c,'Frequency ignores paths; ordinary feature clustering groups similar notes but does not measure their role on paths between groups. Weighted betweenness measures that bridging role; prevalence ranks provide the comparison.',M,y)
    left=heading(c,'3  Data',M,y,COL);right=heading(c,'4  Graph construction',M+COL+GAP,y,COL)
    left=table(c,[
        ['<b>Sources</b>','Fragrantica (Selenium); Parfumo fills notes for <b>11 of 209 perfumes</b>. Parsed offline.'],
        ['<b>Period</b>','30 Aug-12 Oct 2026.'],
        ['<b>Volume</b>',f'<b>{P["N"]}</b> perfumes, {P["notes"]} notes; wider set: <b>1,780</b>. URL manifest in repo.'],
        ['<b>Access</b>','Fragrantica: no written permission; <link href="https://www.fragrantica.com/terms-of-service.phtml" color="#125687">ToS 5.3</link> restricts automation. Parfumo: <link href="https://www.parfumo.com/legal-notice" color="#125687">private/non-commercial copies</link> allowed; project permission unconfirmed.'],
        ['<b>Sampling</b>','Purposive list; Floral 61 vs Leather 4. Not a market sample; supplements are not triangulation.'],
    ],M,left,COL)
    right=table(c,[
        ['<b>Nodes / edges</b>','Note / same-perfume co-occurrence. No seed notes: curated-list corpus.'],
        ['<b>Weight</b>','Count favours repeated pairings; distance = 1/count. NPMI &gt;0.1 checks prevalence.'],
        ['<b>Pruning</b>','Before ranking: exclude generic/high-prevalence &gt;=20% (10 notes); keep frequency &gt;=5 (89), edges &gt;=6; remove isolates.'],
        ['<b>Choice</b>',f'k=6: nearest density 0.12 among k=3..10; <b>{P["nodes"]} nodes / {P["edges"]} edges</b>. k=8 leaves 3 nodes / 2 edges.'],
        ['<b>Rule</b>','Post-result amendment (13 Oct; README): same-node average ranks; gap &gt;=5, positive top-10 in &gt;=80% of 300 brand resamples and at k=3,6,8.'],
    ],M+COL+GAP,right,COL)
    y=min(left,right)-1
    y=heading(c,'5  The network',M,y)
    image_h=WIDTH*2.4/7.0
    c.drawImage(str(ROOT/'results/fig_page.png'),M,y-image_h,width=WIDTH,height=image_h,mask='auto')
    y-=image_h
    y=para(c,'Node size = betweenness; colour = associated scent family; line width = pair count.',M,y)
    left=heading(c,'6  Findings',M,y,COL);right=heading(c,'7  Recommended action (proposed)',M+COL+GAP,y,COL)
    left=table(c,[['<b>Note</b>','<b>Freq.<br/>rank</b>','<b>BC<br/>rank</b>','<b>Gap</b>','<b>Top-10<br/>rate</b>']]+RANK_TABLE[1:],M,left,COL,[52,43,38,35,COL-168],True)
    left=para(c,f'<b>1.</b> Peach has a {Q["rank_gap"]:g}-rank advantage but only {Q["bootstrap_p"]:.1%} stability. Lemon is stable ({L["bootstrap_p"]:.1%}) with little rank advantage. Neither qualifies.',M,left,COL)
    # Compact robustness evidence on-page; full per-node results remain in notebook.
    left=table(c,[['<b>Check</b>','<b>Pass</b>','<b>Control</b>']]+CHECK_TABLE[1:],M,left,COL,[COL-115,32,83],True)
    left=para(c,'<b>2.</b> Zero anchors pass all criteria in each check; the wider catalogue changes the control. Keep Lemon specific to the curated list.',M,left,COL)
    right=para(c,'<b>13 Oct - Palaloy:</b> select Lemon as provisional control; make no differentiation claim.',M+COL+GAP,right,COL)
    right=para(c,'<b>By 23 Oct:</b> brief and cost matched-base Lemon vs Lemon + Peach prototypes; confirm tester availability.',M+COL+GAP,right,COL)
    right=para(c,'<b>By 30 Oct, if ready:</b> blinded, order-balanced pilot with 20 testers; advance Peach only if at least 15 prefer it, otherwise retain control. Section 8 gates testing.',M+COL+GAP,right,COL)
    right=heading(c,'8  What would change my mind',M+COL+GAP,right,COL)
    right=para(c,'Declared-note links do not prove liking. Permission is unresolved for both sites: obtain it or rerun permitted data before testing, with no assumed turnaround. A changed control in that rerun or a failed pilot reverses the recommendation.',M+COL+GAP,right,COL)
    bottom=min(left,right)
    if bottom<M:
        raise ValueError(f'Content crosses {M}pt margin: bottom={bottom:.1f}. Revise content, not font size.')
    c.save()
    print(f'PDF saved: {path}; lowest content y={bottom:.1f} pt; margin={M} pt')
    return {'bottom_y':bottom,'margin_pt':M,'pages':1,'font_min_pt':10}

if __name__=='__main__':
    render(sys.argv[1] if len(sys.argv)>1 else ROOT/'report/MADT7202_MidTerm_Palaloy_Revised.pdf')
