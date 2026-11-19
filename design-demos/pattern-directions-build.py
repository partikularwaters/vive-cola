import re, sys
from pathlib import Path
root=Path("/Users/madridj1689/client-work/vive-website")
STAR=re.search(r'points="([^"]*)"',(root/"assets/shapes/star-10pt-sun.svg").read_text()).group(1)
O,N,S,W,D="#F27A21","#2B3990","#F4BD6A","#F9F9F9","#1D2766"
SYM=f'''<symbol id="bang" viewBox="0 0 120 261"><rect width="120" height="176" rx="5"/><rect y="206" width="120" height="55" rx="5"/></symbol>
<symbol id="v" viewBox="138 0 311 261"><polygon points="138,0 258,0 290,124 325,0 448,0 363,261 222,261"/></symbol>
<symbol id="bangv" viewBox="0 0 449 261"><rect width="120" height="176" rx="5"/><rect y="206" width="120" height="55" rx="5"/><polygon points="138,0 258,0 290,124 325,0 448,0 363,261 222,261"/></symbol>
<symbol id="star" viewBox="0 0 1024 1024"><polygon points="{STAR}"/></symbol>
<symbol id="tri" viewBox="0 0 100 87"><polygon points="50,0 100,87 0,87"/></symbol>'''

def monogram(pid,bg,mono,star,k=1):
    return f'''<pattern id="{pid}" width="{170*k}" height="{130*k}" patternUnits="userSpaceOnUse"><g transform="scale({k})">
<rect width="170" height="130" fill="{bg}"/>
<use href="#bangv" x="14" y="16" width="66" height="38" fill="{mono}"/>
<use href="#bangv" x="99" y="81" width="66" height="38" fill="{mono}"/>
<use href="#star" x="113" y="22" width="22" height="22" fill="{star}"/>
<use href="#star" x="28" y="88" width="22" height="22" fill="{star}"/></g></pattern>'''

def chevron(pid,bg,a,b,c,d,k=1):
    return f'''<pattern id="{pid}" width="{145.4*k}" height="{176*k}" patternUnits="userSpaceOnUse"><g transform="scale({k})">
<rect width="145.4" height="176" fill="{bg}"/>
<use href="#v" x="0" y="2" width="100" height="84" fill="{a}"/>
<use href="#v" x="72.7" y="2" width="100" height="84" fill="{b}" transform="rotate(180 122.7 44)"/>
<use href="#v" x="-72.7" y="2" width="100" height="84" fill="{b}" transform="rotate(180 -22.7 44)"/>
<use href="#v" x="0" y="90" width="100" height="84" fill="{c}"/>
<use href="#v" x="72.7" y="90" width="100" height="84" fill="{d}" transform="rotate(180 122.7 132)"/>
<use href="#v" x="-72.7" y="90" width="100" height="84" fill="{d}" transform="rotate(180 -22.7 132)"/></g></pattern>'''

def confetti(pid,bg,c1,c2,c3,k=1):
    # c1 orange role, c2 sun role, c3 navy role; a 2x2 block of varied placements avoids an obvious tile
    items=[("v",20,22,52,44,c1,-14),("star",140,14,46,46,c2,10),("bang",214,40,16,35,c3,18),("tri",92,86,34,30,c3,32),
           ("sq",30,118,24,24,c2,20),("v",160,110,44,37,c3,12),("bang",100,160,16,35,c1,-22),("star",18,188,38,38,c1,-8),
           ("tri",190,196,40,35,c2,-28),
           ("v",290,40,40,34,c3,22),("tri",400,20,30,26,c1,-40),("star",440,96,34,34,c3,0),("bang",330,120,16,35,c2,-30),
           ("sq",470,180,20,20,c1,-15),("v",370,200,56,47,c1,8),("tri",290,220,26,23,c2,50),
           ("star",60,300,50,50,c3,14),("bang",20,400,16,35,c2,25),("v",120,390,50,42,c2,-20),("tri",200,300,34,30,c1,-10),
           ("sq",200,460,26,26,c3,30),("bang",150,290,16,35,c1,6),("tri",40,470,22,19,c1,70),
           ("star",300,330,30,30,c1,-6),("v",380,300,46,39,c2,-8),("tri",470,320,32,28,c3,24),("bang",440,420,16,35,c3,-12),
           ("sq",310,440,22,22,c2,40),("star",360,440,44,44,c2,12)]
    out=[f'<rect width="520" height="520" fill="{bg}"/>']
    for kind,x,y,w,h,c,r in items:
        cx,cy=x+w/2,y+h/2
        if kind=="sq": out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" transform="rotate({r} {cx} {cy})"/>')
        else: out.append(f'<use href="#{kind}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" transform="rotate({r} {cx} {cy})"/>')
    return f'<pattern id="{pid}" width="{520*k}" height="{520*k}" patternUnits="userSpaceOnUse"><g transform="scale({k})">'+"".join(out)+'</g></pattern>'

DIRS={
 1:dict(slug="monogram-canvas",name="Monogram Canvas",line="Ordered and collectible: the !V monogram repeats like a luggage or scarf print, with the brand's 10-point star as the spacer.",
        use="Merch (scarf, tote, cap lining), packaging sleeves, and quiet page backgrounds.",
        main=lambda p,k=1:monogram(p,N,S,W,k),
        ways=[("Navy / sun",lambda p:monogram(p,N,S,W,.7)),("Orange / navy",lambda p:monogram(p,O,N,W,.7)),("Cream / orange",lambda p:monogram(p,W,O,S,.7))],
        quiet=lambda p:monogram(p,N,"#3646A3","#3646A3",.8), quietbg=N),
 2:dict(slug="charged-chevron",name="Charged Chevron",line="Bold and kinetic: the V and its upside-down twin lock edge to edge, so the logo itself builds the zigzag.",
        use="Can-pack sleeves, event walls, the hero edge of a page, and anywhere the brand needs to shout.",
        main=lambda p,k=1:chevron(p,W,O,S,N,O,k),
        ways=[("Full brand",lambda p:chevron(p,W,O,S,N,O,.6)),("Navy night",lambda p:chevron(p,D,N,"#3646A3",O,N,.6)),("Sun day",lambda p:chevron(p,W,S,O,S,W,.6))],
        quiet=lambda p:chevron(p,O,"#F48A38","#EE7019","#F48A38","#EE7019",.8), quietbg=O, btn="var(--navy)"),
 3:dict(slug="confetti-kit",name="Confetti Kit",line="Loose and festive: every brand shape in one toss, at the same angles as the ad's end card.",
        use="Wrapping paper, sticker sheets, cup sleeves, the Christmas section, and social backgrounds.",
        main=lambda p,k=1:confetti(p,W,O,S,N,k),
        ways=[("Cream",lambda p:confetti(p,W,O,S,N,.55)),("Navy",lambda p:confetti(p,N,O,S,W,.55)),("Orange",lambda p:confetti(p,O,N,S,W,.55))],
        quiet=lambda p:confetti(p,N,"#3646A3","#3646A3","#3646A3",.6), quietbg=N, pack=lambda p:confetti(p,N,O,S,W,.75)),
}
for n,d in DIRS.items():
    defs=SYM+d["main"]("main")+(d["pack"]("hero") if "pack" in d else d["main"]("hero",.75))+"".join(f(f"w{i}") for i,(nm,f) in enumerate(d["ways"]))+d["quiet"]("quiet")
    ways="".join(f'<figure><svg viewBox="0 0 300 200"><rect width="300" height="200" fill="url(#w{i})"/></svg><figcaption>{nm}</figcaption></figure>' for i,(nm,f) in enumerate(d["ways"]))
    html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VIVE pattern · Direction {n}: {d["name"]}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&display=swap">
<style>
  :root {{ --orange:#F27A21; --navy:#2B3990; --sun:#F4BD6A; --white:#F9F9F9; --deep:#1D2766; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; width:1440px; background:#ECEDF3; font-family:Montserrat, sans-serif; color:var(--deep); }}
  .top {{ display:grid; grid-template-columns:760px 1fr; gap:48px; padding:48px; align-items:start; }}
  .swatch svg {{ display:block; width:760px; height:560px; }}
  h1 {{ margin:0; font-size:44px; font-weight:900; line-height:1; text-transform:uppercase; }}
  h1 small {{ display:block; font-size:15px; letter-spacing:.12em; color:var(--orange); margin-bottom:12px; }}
  p {{ font-size:17px; line-height:1.55; font-weight:600; margin:18px 0 0; max-width:30em; }}
  p b {{ font-weight:800; }}
  .ways {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:28px; }}
  .ways figure {{ margin:0; }} .ways svg {{ display:block; width:100%; }}
  .ways figcaption {{ margin-top:8px; font-size:13px; font-weight:800; }}
  .uses {{ display:grid; grid-template-columns:1.25fr 1fr; gap:32px; padding:0 48px 48px; }}
  .uses h2 {{ grid-column:1/-1; margin:0; font-size:15px; font-weight:900; letter-spacing:.12em; text-transform:uppercase; }}
  /* Use 1: a site section with the quiet tone-on-tone pattern behind real content */
  .site {{ position:relative; height:380px; overflow:hidden; background:{d["quietbg"]}; }}
  .site svg {{ position:absolute; inset:0; width:100%; height:100%; }}
  .site .in {{ position:relative; padding:56px 52px; color:var(--white); }}
  .site .label {{ display:inline-block; background:var(--sun); color:var(--navy); font-weight:900; font-size:40px; text-transform:uppercase; padding:6px 30px 6px 18px; transform:rotate(-2deg); clip-path:polygon(0 0,100% 0,calc(100% - 18px) 100%,0 100%); }}
  .site .in p {{ color:var(--white); font-size:18px; max-width:24em; }}
  .site .btn {{ display:inline-block; margin-top:22px; background:{d.get("btn","var(--orange)")}; color:var(--white); font-weight:800; font-size:14px; letter-spacing:.06em; text-transform:uppercase; padding:14px 26px 14px 20px; clip-path:polygon(0 0,100% 0,calc(100% - 12px) 100%,0 100%); }}
  .site .note, .pack .note {{ position:absolute; right:14px; bottom:12px; font-size:12px; font-weight:800; color:var(--white); background:rgba(20,24,63,.82); padding:5px 9px; }}
  /* Use 2: a six-pack sleeve face with the full-strength pattern and the real can renders */
  .pack {{ position:relative; height:380px; overflow:hidden; background:var(--deep); }}
  .pack svg {{ position:absolute; inset:0; width:100%; height:100%; }}
  .pack .band {{ position:absolute; left:0; right:0; top:118px; height:150px; background:var(--white); clip-path:polygon(0 12%,100% 0,100% 88%,0 100%); }}
  .pack .band img {{ position:absolute; left:34px; top:48px; width:190px; }}
  .pack .band span {{ position:absolute; left:36px; top:96px; font-size:13px; font-weight:800; letter-spacing:.1em; text-transform:uppercase; color:var(--navy); }}
  .pack .cans {{ position:absolute; right:30px; top:70px; display:flex; gap:6px; align-items:flex-end; }}
  .pack .cans img {{ width:72px; filter:drop-shadow(0 12px 14px rgba(20,24,63,.4)); }}
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute"><defs>{defs}</defs></svg>
<div class="top">
  <div class="swatch"><svg viewBox="0 0 760 560"><rect width="760" height="560" fill="url(#main)"/></svg></div>
  <div>
    <h1><small>Pattern direction {n}</small>{d["name"]}</h1>
    <p>{d["line"]}</p>
    <p><b>Best for:</b> {d["use"]}</p>
    <div class="ways">{ways}</div>
  </div>
</div>
<div class="uses">
  <h2>In use</h2>
  <div class="site">
    <svg><rect width="100%" height="100%" fill="url(#quiet)"/></svg>
    <div class="in">
      <span class="label">Pick your vibe</span>
      <p>The quiet, tone-on-tone version sits behind headings and copy without fighting them.</p>
      <span class="btn">Grab a VIVE!</span>
    </div>
    <span class="note">Website section background</span>
  </div>
  <div class="pack">
    <svg><rect width="100%" height="100%" fill="url(#hero)"/></svg>
    <div class="band"><img src="../assets/wordmark-vive-navy.png" alt="VIVE"><span>Six-pack</span></div>
    <div class="cans"><img src="../assets/can-glow-web.webp" alt=""><img src="../assets/can-classic-web.webp" alt=""><img src="../assets/can-focus-web.webp" alt=""></div>
    <span class="note">Six-pack sleeve</span>
  </div>
</div>
</body>
</html>'''
    out=root/f"design-demos/pattern-dir-{n}.html"; out.write_text(html); print(out)
