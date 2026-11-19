"""Shape-only VIVE pattern definitions (no logo characters). Shared by the
candidate sheet and the full direction pages."""
import math, random, re
from pathlib import Path
ROOT=Path("/Users/madridj1689/client-work/vive-website")
def pts(name): return re.search(r'points="([^"]*)"',(ROOT/f"assets/shapes/{name}.svg").read_text()).group(1)
O,N,S,W,D="#F27A21","#2B3990","#F4BD6A","#F9F9F9","#1D2766"
SYM=f'''<symbol id="s10" viewBox="0 0 1024 1024"><polygon points="{pts('star-10pt-sun')}"/></symbol>
<symbol id="s10k" viewBox="0 0 1024 1024"><polygon points="{pts('star-10pt-spiky-sun')}"/></symbol>
<symbol id="s4" viewBox="0 0 1024 1024"><polygon points="{pts('star-4pt-sparkle-sun')}"/></symbol>
<symbol id="tac" viewBox="252 40 520 920"><polygon points="{pts('triangle-acute-sun')}"/></symbol>
<symbol id="cham" viewBox="122 122 780 780"><polygon points="{pts('square-chamfer-sun')}"/></symbol>
<symbol id="s5" viewBox="0 0 1024 1024"><polygon points="{pts('star-5pt-bold-sun')}"/></symbol>
<symbol id="tri" viewBox="87.6 57 848.8 735"><polygon points="{pts('triangle-equilateral-sun')}"/></symbol>
<symbol id="dia" viewBox="32 32 960 960"><polygon points="{pts('square-diamond-sun')}"/></symbol>'''

def tri_mosaic(pid,cols,k=1,seed=7):
    # true equilateral tessellation; weighted colors; 10 triangles per row-pair cell across
    s=40; h=s*math.sqrt(3)/2; nx=10; ny=8
    W_,H_=nx*s,ny*h
    rnd=random.Random(seed); out=[]
    for r in range(ny):
        for c in range(2*nx+1):
            x=(c-1)*s/2; up=(c+r)%2==0
            y0,y1=r*h,(r+1)*h
            p=[(x,y1),(x+s/2,y0),(x+s,y1)] if up else [(x,y0),(x+s/2,y1),(x+s,y0)]
            col=rnd.choices([c_ for c_,w in cols],[w for c_,w in cols])[0]
            out.append('<polygon points="'+" ".join(f"{a:.2f},{b:.2f}" for a,b in p)+f'" fill="{col}"/>')
    # wrap: copy column 0 colors onto the overflow column so the seam matches
    return f'<pattern id="{pid}" width="{W_*k:.2f}" height="{H_*k:.2f}" patternUnits="userSpaceOnUse"><g transform="scale({k})">'+"".join(out)+'</g></pattern>'

def tri_mosaic_seamless(pid,cols,k=1,seed=7):
    s=40; h=s*math.sqrt(3)/2; nx=10; ny=8
    rnd=random.Random(seed)
    grid={}
    for r in range(ny):
        for c in range(2*nx):
            grid[(r,c)]=rnd.choices([c_ for c_,w in cols],[w for c_,w in cols])[0]
    out=[]
    for r in range(ny):
        for c in range(-1,2*nx+1):
            x=c*s/2; up=(c+r)%2==0
            y0,y1=r*h,(r+1)*h
            p=[(x,y1),(x+s/2,y0),(x+s,y1)] if up else [(x,y0),(x+s/2,y1),(x+s,y0)]
            out.append('<polygon points="'+" ".join(f"{a:.2f},{b:.2f}" for a,b in p)+f'" fill="{grid[(r,c%(2*nx))]}"/>')
    W_,H_=nx*s,ny*h
    return f'<pattern id="{pid}" width="{W_*k:.2f}" height="{H_*k:.2f}" patternUnits="userSpaceOnUse"><g transform="scale({k})">'+"".join(out)+'</g></pattern>'

def star_lattice(pid,bg,star,spark,k=1):
    return f'''<pattern id="{pid}" width="{84*k}" height="{84*k}" patternUnits="userSpaceOnUse"><g transform="scale({k})">
<rect width="84" height="84" fill="{bg}"/><use href="#s10" x="18" y="18" width="48" height="48" fill="{star}"/>
<use href="#s4" x="-8" y="-8" width="16" height="16" fill="{spark}"/><use href="#s4" x="76" y="-8" width="16" height="16" fill="{spark}"/>
<use href="#s4" x="-8" y="76" width="16" height="16" fill="{spark}"/><use href="#s4" x="76" y="76" width="16" height="16" fill="{spark}"/></g></pattern>'''

def halftone(pid,bg,star,k=1,n=10,pitch=40):
    T=n*pitch; out=[f'<rect width="{T}" height="{T}" fill="{bg}"/>']
    for i in range(n):
        for j in range(n):
            # size swells and fades in a seamless wave across the tile
            v=0.5+0.5*math.cos(2*math.pi*i/n)*math.cos(2*math.pi*j/n)
            sz=6+34*v
            if sz<7: continue
            cx,cy=i*pitch+pitch/2,j*pitch+pitch/2
            out.append(f'<use href="#s10" x="{cx-sz/2:.1f}" y="{cy-sz/2:.1f}" width="{sz:.1f}" height="{sz:.1f}" fill="{star}" transform="rotate({(i*7+j*5)%36} {cx} {cy})"/>')
    return f'<pattern id="{pid}" width="{T*k}" height="{T*k}" patternUnits="userSpaceOnUse"><g transform="scale({k})">'+"".join(out)+'</g></pattern>'

def chamfer_checker(pid,a,b,gem,k=1):
    # chamfered squares touch on a grid; the cut corners open a diamond at every meeting point
    return f'''<pattern id="{pid}" width="{120*k}" height="{120*k}" patternUnits="userSpaceOnUse"><g transform="scale({k})">
<rect width="120" height="120" fill="{gem}"/>
<use href="#cham" x="0" y="0" width="60" height="60" fill="{a}"/><use href="#cham" x="60" y="0" width="60" height="60" fill="{b}"/>
<use href="#cham" x="0" y="60" width="60" height="60" fill="{b}"/><use href="#cham" x="60" y="60" width="60" height="60" fill="{a}"/></g></pattern>'''

def shards(pid,bg,a,b,k=1):
    out=[f'<rect width="150" height="220" fill="{bg}"/>']
    cols=[a,a,b,a,a,a,b,a]
    for r,y in enumerate([10,120]):
        for i in range(5):
            x=i*30+(15 if r else 0)
            flip=(i+r)%2
            c=cols[(i+r*3)%len(cols)]
            tf=f' transform="rotate(180 {x+11} {y+45})"' if flip else ''
            out.append(f'<use href="#tac" x="{x}" y="{y}" width="22" height="90" fill="{c}"{tf}/>')
    return f'<pattern id="{pid}" width="{150*k}" height="{220*k}" patternUnits="userSpaceOnUse" patternTransform="rotate(-14)"><g transform="scale({k})">'+"".join(out)+'</g></pattern>'

def tape(pid,bg,a,b,c,spark,k=1):
    # rows of angled banner segments (slanted ends, slightly tilted tops), staggered like tape
    out=[f'<rect width="480" height="240" fill="{bg}"/>']
    rows=[(14,40,[(0,210,a),(240,470,b)]),(70,28,[(-60,120,c),(150,330,a),(360,420,c)]),(116,44,[(30,250,b),(280,460,c)]),(178,30,[(-90,90,a),(120,300,b),(330,390,a)])]
    for y,h,segs in rows:
        for x0,x1,col in segs:
            for off in (0,480,-480):
                X0,X1=x0+off,x1+off
                if X1<0 or X0>480: continue
                out.append(f'<polygon points="{X0+8},{y} {X1},{y+3} {X1-8},{y+h} {X0},{y+h-3}" fill="{col}"/>')
    for x,y,s in [(225,60,18),(440,104,14),(110,160,16),(320,222,12)]:
        out.append(f'<use href="#s10k" x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" fill="{spark}"/>')
    return f'<pattern id="{pid}" width="{480*k}" height="{240*k}" patternUnits="userSpaceOnUse" patternTransform="rotate(-6)"><g transform="scale({k})">'+"".join(out)+'</g></pattern>'


def confetti_shapes(pid,bg,c1,c2,c3,k=1):
    """Batch 1's Confetti Kit toss rebuilt with shapes only: each V became a star,
    a concentric star badge, or a chamfered square, and each ! became the slim
    acute triangle. Sparkles, diamonds, and banner strips fill the gaps."""
    I=[("s10k",20,22,50,50,c1,-14),("s10",140,14,46,46,c2,10),("tac",216,36,15,42,c3,18),("tri",92,86,34,30,c3,32),
       ("cham",30,118,24,24,c2,20),("conc",160,108,42,42,c3,12),("tac",102,156,15,42,c1,-22),("s10",18,188,38,38,c1,-8),
       ("tri",190,196,40,35,c2,-28),
       ("cham",292,40,34,34,c3,22),("tri",400,20,30,26,c1,-40),("s10",440,96,34,34,c3,0),("tac",332,114,15,42,c2,-30),
       ("dia",470,180,20,20,c1,0),("s10k",372,196,52,52,c1,8),("tri",290,220,26,23,c2,50),
       ("conc",60,300,50,50,c3,14),("tac",22,396,15,42,c2,25),("s10",122,388,46,46,c2,-20),("tri",200,300,34,30,c1,-10),
       ("cham",200,460,26,26,c3,30),("tac",152,284,15,42,c1,6),("tri",40,470,22,19,c1,70),
       ("s10k",300,330,32,32,c1,-6),("cham",382,300,40,40,c2,-8),("tri",470,320,32,28,c3,24),("tac",442,414,15,42,c3,-12),
       ("dia",310,440,22,22,c2,0),("s10",360,440,44,44,c2,12),
       ("s4",92,40,16,16,c3,0),("s4",250,140,14,14,c1,0),("s4",458,250,16,16,c2,0),("s4",120,250,12,12,c3,0),("s4",250,400,16,16,c1,0),("s4",420,480,12,12,c3,0),
       ("strip",230,80,34,10,c2,-18),("strip",60,240,30,9,c3,22),("strip",420,150,30,9,c2,-30),("strip",260,500,34,10,c1,14),("strip",100,500,28,9,c3,-24)]
    out=[f'<rect width="520" height="520" fill="{bg}"/>']
    for kind,x,y,w,h,c,r in I:
        cx,cy=x+w/2,y+h/2; t=f'transform="rotate({r} {cx} {cy})"'
        if kind=="strip":
            out.append(f'<polygon points="{x+3},{y} {x+w},{y+1} {x+w-3},{y+h} {x},{y+h-1}" fill="{c}" {t}/>')
        elif kind=="conc":
            ring=bg if c!=bg else c1
            out.append(f'<g {t}><use href="#s10" x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/><use href="#s10" x="{x+w*.25}" y="{y+h*.25}" width="{w*.5}" height="{h*.5}" fill="{ring}"/></g>')
        else:
            out.append(f'<use href="#{kind}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {t}/>')
    return f'<pattern id="{pid}" width="{520*k}" height="{520*k}" patternUnits="userSpaceOnUse"><g transform="scale({k})">'+"".join(out)+'</g></pattern>'
