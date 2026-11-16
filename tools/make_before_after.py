"""
make_before_after.py
Purpose:  Build a self-contained HTML page with before/after sliders for a zone.
Used by:  workflows/disenar_y_renderizar_zona.md (step 9), workflows/armar_plan_final.md
Inputs:   pairs.json ([{before, after, label}]), image paths relative to pairs.json
Outputs:  Self-contained HTML page (images embedded; --link-images to reference files instead)
Env vars: none
Cost:     free
Status:   Implemented.
"""
import argparse, base64, html, io, json, os, sys
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Build a before/after slider page.")
    p.add_argument("--pairs", required=True, help="Path to pairs.json")
    p.add_argument("--output", required=True, help="HTML output path")
    p.add_argument("--title", default="Antes y después")
    p.add_argument("--link-images", action="store_true",
                   help="Reference image files instead of embedding them (default embeds, so the page works anywhere)")
    p.add_argument("--max-side", type=int, default=1600, help="Longest side of embedded images")
    p.add_argument("--dry-run", action="store_true", help="No writes")
    return p.parse_args()


PAGE = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body {{ margin:0; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background:#f6f3ec; color:#2f3a2f; }}
  header {{ padding:24px 20px 8px; max-width:1200px; margin:auto; }}
  h1 {{ font-size:1.6rem; margin:0 0 4px; }}
  p.hint {{ margin:0; color:#5d6b5d; }}
  figure {{ max-width:1200px; margin:20px auto 36px; padding:0 20px; }}
  .ba {{ position:relative; overflow:hidden; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,.15); user-select:none; touch-action:none; }}
  .ba img {{ display:block; width:100%; height:auto; }}
  .ba .after {{ position:absolute; inset:0; clip-path: inset(0 0 0 50%); }}
  .ba .after img {{ height:100%; object-fit:cover; }}
  .ba .bar {{ position:absolute; top:0; bottom:0; left:50%; width:3px; background:#fff; box-shadow:0 0 4px rgba(0,0,0,.5); pointer-events:none; }}
  .ba .knob {{ position:absolute; top:50%; left:50%; width:38px; height:38px; margin:-19px 0 0 -19px; border-radius:50%;
               background:#fff; box-shadow:0 1px 6px rgba(0,0,0,.4); pointer-events:none; display:flex; align-items:center;
               justify-content:center; font-size:15px; color:#2f3a2f; }}
  .tag {{ position:absolute; top:10px; padding:3px 9px; border-radius:4px; background:rgba(0,0,0,.55); color:#fff; font-size:.85rem; pointer-events:none; }}
  .tag.l {{ left:10px; }} .tag.r {{ right:10px; }}
  figcaption {{ margin-top:8px; font-size:1rem; }}
  .controls {{ display:flex; gap:10px; align-items:center; margin-top:12px; }}
  .controls button {{ flex:0 0 auto; font-size:1rem; padding:10px 16px; border-radius:8px; border:1px solid #9fb09f;
                      background:#fff; color:#2f3a2f; }}
  .controls button.on {{ background:#3f6b3f; color:#fff; border-color:#3f6b3f; }}
  .controls input[type=range] {{ flex:1 1 auto; height:44px; accent-color:#3f6b3f; }}
</style></head><body>
<header><h1>{title}</h1><p class="hint">Mueve la barra de abajo (o arrastra sobre la foto) para comparar el jardín actual con la propuesta. También puedes tocar «Antes» o «Después».</p></header>
{figures}
<script>
document.querySelectorAll('figure').forEach(function (fig) {{
  var el = fig.querySelector('.ba'), after = el.querySelector('.after'), bar = el.querySelector('.bar'),
      knob = el.querySelector('.knob'), range = fig.querySelector('input[type=range]'),
      btns = fig.querySelectorAll('button'), dragging = false;
  // "p" = how much of the BEFORE photo is visible from the left (0 = all after, 100 = all before).
  function show(p) {{
    p = Math.min(100, Math.max(0, p));
    after.style.clipPath = 'inset(0 0 0 ' + p + '%)';
    after.style.webkitClipPath = 'inset(0 0 0 ' + p + '%)';
    bar.style.left = p + '%'; knob.style.left = p + '%';
    range.value = 100 - p;
    btns.forEach(function (b) {{ b.classList.toggle('on', (b.dataset.v === '0' && p === 100) || (b.dataset.v === '100' && p === 0)); }});
  }}
  range.addEventListener('input', function () {{ show(100 - Number(range.value)); }});
  btns.forEach(function (b) {{ b.addEventListener('click', function () {{ show(b.dataset.v === '0' ? 100 : 0); }}); }});
  function fromX(x) {{ var r = el.getBoundingClientRect(); show((x - r.left) / r.width * 100); }}
  el.addEventListener('pointerdown', function (e) {{ dragging = true; try {{ el.setPointerCapture(e.pointerId); }} catch (_) {{}} fromX(e.clientX); }});
  el.addEventListener('pointermove', function (e) {{ if (dragging) fromX(e.clientX); }});
  el.addEventListener('pointerup', function () {{ dragging = false; }});
  el.addEventListener('pointercancel', function () {{ dragging = false; }});
  el.addEventListener('touchmove', function (e) {{ if (e.touches[0]) {{ fromX(e.touches[0].clientX); e.preventDefault(); }} }}, {{ passive: false }});
  show(50);
}});
</script>
</body></html>
"""

FIGURE = """<figure>
  <div class="ba">
    <img src="{before}" alt="Antes">
    <div class="after"><img src="{after}" alt="Después"></div>
    <div class="bar"></div><div class="knob">&#8596;</div>
    <span class="tag l">Antes</span><span class="tag r">Después</span>
  </div>
  <div class="controls">
    <button type="button" data-v="0">Antes</button>
    <input type="range" min="0" max="100" value="50" aria-label="Comparar antes y después">
    <button type="button" data-v="100">Después</button>
  </div>
  <figcaption>{label}</figcaption>
</figure>"""


def embed(path: Path, max_side: int) -> str:
    from PIL import Image, ImageOps
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    img.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def run(pairs_path, output_path, title="Antes y después", link_images=False, max_side=1600, dry_run=False) -> dict:
    pairs_file = Path(pairs_path)
    pairs = json.loads(pairs_file.read_text())
    if not pairs:
        raise ValueError(f"{pairs_path} has no pairs")
    out = Path(output_path)
    figures = []
    for p in pairs:
        paths = {}
        for k in ("before", "after"):
            img = (pairs_file.parent / p[k]).resolve()
            if not img.exists():
                raise FileNotFoundError(f"Missing image: {img}")
            paths[k] = (html.escape(os.path.relpath(img, out.parent.resolve())) if link_images
                        else embed(img, max_side))
        figures.append(FIGURE.format(label=html.escape(p.get("label", "")), **paths))
    page = PAGE.format(title=html.escape(title), figures="\n".join(figures))
    if dry_run:
        return {"output": str(out), "pairs": len(pairs), "dry_run": True}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return {"output": str(out), "pairs": len(pairs)}


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.pairs, a.output, a.title, a.link_images, a.max_side, a.dry_run)}, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
