import collections, matplotlib, numpy as np, sys
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import decision_rule as dr
from notes_clean import perfume_note_sets
from netlib import *
SURF="#ffffff"; INK="#0b0b0b"
COL={"Floral":"#2a78d6","Oriental":"#eb6834","Woody":"#1baf7a","Other / mixed":"#b9b8b2"}
def draw(sub,out="fig_page.png"):
  sub=sub.reset_index(drop=True); sets=perfume_note_sets(sub,1)
  fam=sub["Scent Family Primary"].str.split().str[0].tolist()
  N,freq,pair=counts(sets); K=6
  valid=[i for i,f in enumerate(fam) if isinstance(f,str)]; base=collections.Counter(fam[i] for i in valid); nv=len(valid)
  nf=collections.defaultdict(collections.Counter)
  for i in valid:
      for n in sets[i]: nf[n][fam[i]]+=1
  def dominant(n,min_in=3,min_lift=1.3):
      tot=sum(nf[n].values()); best=None; bl=0
      for f,c in nf[n].items():
          lift=(c/tot)/(base[f]/nv)
          if c>=min_in and lift>bl: best,bl=f,lift
      return best if bl>=min_lift else "Mixed"
  analysis=dr.analyse(sets,K,5)
  bc,G=analysis['bc'],analysis['graph']
  grp={n:('Bridge' if bc[n]>1e-12 else 'Zero betweenness') for n in G}
  colors={'Bridge':'#2876c7','Zero betweenness':'#b9b8b2'}
  SHORT={"Lily-of-the-Valley":"Lily-of-the-Valley"}
  comps=sorted(nx.connected_components(G),key=len,reverse=True)
  pos={}
  p0=nx.kamada_kawai_layout(G.subgraph(comps[0]),weight=None)
  for n,(x,y) in p0.items(): pos[n]=np.array([x*2.3-0.8,y*1.0])
  slots=[(3.5,0.72),(3.5,0.0),(3.5,-0.72)]
  for c,(cx,cy) in zip(comps[1:],slots):
      sg=sorted(c)
      if len(c)==2: pc={sg[0]:np.array([-0.32,0]),sg[1]:np.array([0.32,0])}
      else: pc={sg[0]:np.array([-0.3,-0.16]),sg[1]:np.array([0.3,-0.16]),sg[2]:np.array([0.0,0.18])}
      for n,v in pc.items(): pos[n]=np.array([cx,cy])+v
  fig,ax=plt.subplots(figsize=(7.0,2.4),dpi=300); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
  mx=max(d["count"] for *_,d in G.edges(data=True))
  for a,b,d in G.edges(data=True):
      ax.plot([pos[a][0],pos[b][0]],[pos[a][1],pos[b][1]],color="#bdbcb5",lw=0.6+2.2*d["count"]/mx,alpha=0.75,zorder=1,solid_capstyle="round")
  for n in G: ax.scatter(*pos[n],s=45+1300*bc[n],c=colors[grp[n]],edgecolors="white",linewidths=1.0,zorder=2)
  ax.set_xlim(-3.5,4.9); ax.set_ylim(-1.2,1.22); ax.axis("off")
  fig.subplots_adjust(left=0.01,right=0.99,top=0.99,bottom=0.11)
  fig.canvas.draw()
  P={n:ax.transData.transform(pos[n])*72/fig.dpi for n in G}
  rad={n:((45+1300*bc[n])**0.5)/2 for n in G}
  FS=10.2; placed=[]
  def rect(n,txt,d):
      w=len(txt)*FS*0.53; h=FS*1.2; r=rad[n]+2.5; dx,dy=d
      cx=P[n][0]+dx*(r+(w/2 if abs(dx)>0.3 else 0)); cy=P[n][1]+dy*(r+h/2)
      return (cx-w/2,cy-h/2,cx+w/2,cy+h/2)
  def ov(a,b): return max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
  DIRS=[(1,0),(-1,0),(0,1),(0,-1),(0.7,0.7),(-0.7,0.7),(0.7,-0.7),(-0.7,-0.7)]
  for n in sorted(G,key=lambda x:-bc[x]):
      txt=SHORT.get(n,n); best=None
      OVR={'Oakmoss':[(0,1)],'Lemon':[(1,0)]}
      for d in OVR.get(n,DIRS):
          R=rect(n,txt,d); sc=0
          for m in G:
              c=(P[m][0]-rad[m],P[m][1]-rad[m],P[m][0]+rad[m],P[m][1]+rad[m]); sc+=ov(R,c)*3
          for q in placed: sc+=ov(R,q)*4
          W,H=fig.get_size_inches()*72
          if R[0]<4 or R[2]>W-4 or R[1]<20 or R[3]>H-2: sc+=1e5
          for u,v in G.edges():
              for t in np.linspace(0,1,14):
                  x=P[u][0]*(1-t)+P[v][0]*t; y=P[u][1]*(1-t)+P[v][1]*t
                  if R[0]<=x<=R[2] and R[1]<=y<=R[3]: sc+=6
          if best is None or sc<best[0]: best=(sc,d,R)
      _,d,R=best; placed.append(R); r=rad[n]+2.5
      ha="left" if d[0]>0.3 else ("right" if d[0]<-0.3 else "center")
      va="center" if abs(d[0])>0.3 else ("bottom" if d[1]>0 else "top")
      ax.annotate(txt,pos[n],xytext=(d[0]*r,d[1]*r),textcoords="offset points",ha=ha,va=va,fontsize=FS,color=INK,zorder=4)
  from matplotlib.lines import Line2D
  h=[Line2D([0],[0],marker="o",color="white",markerfacecolor=c,markersize=7,label=k) for k,c in colors.items()]
  fig.legend(handles=h,loc="lower center",ncol=4,frameon=False,fontsize=10,handletextpad=0.2,columnspacing=1.4,bbox_to_anchor=(0.5,0.0))
  fig.savefig(out,facecolor=SURF)
  print(G.number_of_nodes(),G.number_of_edges())
  plt.close(fig)
