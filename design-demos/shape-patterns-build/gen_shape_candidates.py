import sys; sys.path.insert(0,str(__import__('pathlib').Path(__file__).parent))
from shapes_lib import *
C=[("G","Triangle Mosaic","Equilateral triangles tile edge to edge in the four brand colors, orange leading.",tri_mosaic_seamless("pG",[(O,40),(N,25),(S,20),(D,10),(W,5)])),
   ("H","Star Lattice","10-point stars on a square grid, with 4-point sparkles where four tiles meet.",star_lattice("pH",N,S,W)),
   ("I","Star Halftone","10-point stars swell and shrink in a wave, like a halftone print.",halftone("pI",N,O)),
   ("J","Chamfer Checker","Chamfered squares in a checkerboard; their cut corners open sun diamonds.",chamfer_checker("pJ",O,N,S)),
   ("K","Energy Shards","The deck's acute triangles in tilted rows, pointing up and down.",shards("pK",S,N,O)),
   ("L","Angled Tape","Strips of the angled banner shape, staggered like tape, with spiky stars.",tape("pL",W,O,N,S,O))]
defs=SYM+"".join(c[3] for c in C)
figs="".join(f'<figure><svg viewBox="0 0 400 400"><rect width="400" height="400" fill="url(#p{c[0]})"/></svg><figcaption>{c[0]} · {c[1]}<span>{c[2]}</span></figcaption></figure>' for c in C)
html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VIVE shape pattern candidates</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap">
<style>
  :root {{ --deep:#1D2766; }}
  body {{ margin:0; width:1320px; padding:40px; box-sizing:border-box; background:#ECEDF3; font-family:Montserrat, sans-serif; color:var(--deep); }}
  h1 {{ margin:0 0 6px; font-size:28px; font-weight:900; }}
  p.sub {{ margin:0 0 28px; font-size:15px; font-weight:700; color:#4a5288; }}
  .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:28px; }}
  figure {{ margin:0; }} figure svg {{ display:block; width:100%; aspect-ratio:1; }}
  figcaption {{ margin-top:12px; font-size:16px; font-weight:900; }}
  figcaption span {{ display:block; margin-top:4px; font-size:13px; font-weight:700; color:#4a5288; }}
</style>
</head>
<body>
<h1>VIVE shape pattern candidates</h1>
<p class="sub">Batch 2: six repeats built only from the brand shape library, with no logo characters.</p>
<svg width="0" height="0" style="position:absolute"><defs>{defs}</defs></svg>
<div class="grid">{figs}</div>
</body>
</html>'''
(ROOT/"design-demos/shape-pattern-candidates.html").write_text(html)
