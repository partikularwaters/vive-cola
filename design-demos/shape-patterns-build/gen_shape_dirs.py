import sys; sys.path.insert(0,str(__import__('pathlib').Path(__file__).parent))
from shapes_lib import *
root=ROOT
NAVYQ=[("#2B3990",40),("#33429C",25),("#26338A",25),("#3A49A6",10)]
DIRS={
 1:dict(name="Triangle Mosaic",line="Dense and geometric: equilateral triangles tile edge to edge, so the brand's signature shape becomes a full-coverage surface.",
        use="Six-pack sleeves, vending wraps, booth walls, and full-bleed social posts.",
        main=lambda p,k=1:tri_mosaic_seamless(p,[(O,40),(N,25),(S,20),(D,10),(W,5)],k),
        ways=[("Full brand",lambda p:tri_mosaic_seamless(p,[(O,40),(N,25),(S,20),(D,10),(W,5)],.5)),("Sunset",lambda p:tri_mosaic_seamless(p,[(O,45),(S,35),(W,20)],.5,seed=3)),("Night",lambda p:tri_mosaic_seamless(p,[(N,50),(D,35),(O,15)],.5,seed=5))],
        quiet=lambda p:tri_mosaic_seamless(p,NAVYQ,.9,seed=11), quietbg=N, pack=lambda p:tri_mosaic_seamless(p,[(O,40),(N,25),(S,20),(D,10),(W,5)],.8)),
 2:dict(name="Star Halftone",line="Graphic and moving: 10-point stars swell and shrink in a wave, like a halftone print, so the pattern feels charged even when it stands still.",
        use="Website section backgrounds, can-pack sides, tote bags, and the edges of posters.",
        main=lambda p,k=1:halftone(p,N,O,k),
        ways=[("Orange on navy",lambda p:halftone(p,N,O,.5)),("Navy on sun",lambda p:halftone(p,S,N,.5)),("Cream on orange",lambda p:halftone(p,O,W,.5))],
        quiet=lambda p:halftone(p,N,"#3646A3",.8), quietbg=N, pack=lambda p:halftone(p,N,O,.7)),
 3:dict(name="Angled Tape",line="Loud and handmade: strips of the angled banner shape overlap like tape on a wall, the same cut the site uses for its labels and buttons.",
        use="Event walls, merch prints, sticker sheets, and campaign headers.",
        main=lambda p,k=1:tape(p,W,O,N,S,O,k),
        ways=[("Cream",lambda p:tape(p,W,O,N,S,O,.5)),("Navy",lambda p:tape(p,N,O,S,W,S,.5)),("Sun",lambda p:tape(p,S,O,N,W,N,.5))],
        quiet=lambda p:tape(p,O,"#F48A38","#EE7019","#F58F42","#EE7019",.8), quietbg=O, btn="var(--navy)", pack=lambda p:tape(p,N,O,S,W,S,.7)),
 4:dict(name="Confetti Toss",line="Batch 1's Confetti Kit, rebuilt from shapes only: stars, star badges, chamfered squares, slim triangles, sparkles, and banner strips tossed at the angles of the ad's end card.",
        use="Wrapping paper, sticker sheets, cup sleeves, the Christmas section, and social backgrounds.",
        main=lambda p,k=1:confetti_shapes(p,W,O,S,N,k),
        ways=[("Cream",lambda p:confetti_shapes(p,W,O,S,N,.55)),("Navy",lambda p:confetti_shapes(p,N,O,S,W,.55)),("Orange",lambda p:confetti_shapes(p,O,N,S,W,.55))],
        quiet=lambda p:confetti_shapes(p,N,"#3646A3","#3646A3","#3646A3",.6), quietbg=N, pack=lambda p:confetti_shapes(p,N,O,S,W,.75)),
}
for n,d in DIRS.items():
    defs=SYM+d["main"]("main")+(d["pack"]("hero") if "pack" in d else d["main"]("hero",.75))+"".join(f(f"w{i}") for i,(nm,f) in enumerate(d["ways"]))+d["quiet"]("quiet")
    ways="".join(f'<figure><svg viewBox="0 0 300 200"><rect width="300" height="200" fill="url(#w{i})"/></svg><figcaption>{nm}</figcaption></figure>' for i,(nm,f) in enumerate(d["ways"]))
    html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VIVE shape pattern · Direction {n}: {d["name"]}</title>
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
    <h1><small>Shape pattern direction {n}</small>{d["name"]}</h1>
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
    out=root/f"design-demos/shape-pattern-dir-{n}.html"; out.write_text(html); print(out)
