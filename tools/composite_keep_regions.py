"""
composite_keep_regions.py
Purpose:  Paste original pixels back over the KEEP mask so fixed elements are guaranteed unchanged.
Used by:  workflows/disenar_y_renderizar_zona.md (step 7)
Inputs:   Original normalized photo, render, KEEP mask (255 = keep original)
Outputs:  <output>/<original-stem>__<render-stem>.png and an entry appended to <output>/pairs.json
Env vars: none
Cost:     free
Status:   Implemented.
"""
import argparse, json, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps


def parse_args():
    p = argparse.ArgumentParser(description="Paste original pixels back over the KEEP mask.")
    p.add_argument("--original", required=True)
    p.add_argument("--render", required=True)
    p.add_argument("--mask", required=True, help="KEEP mask, 255 = keep original")
    p.add_argument("--output", required=True, help="Output folder, e.g. outputs/renders/cesped")
    p.add_argument("--feather", type=int, default=9, help="Gaussian blur radius for the seam (5-15 px)")
    p.add_argument("--erode", type=int, default=2, help="Shrink keep mask before feathering (px)")
    p.add_argument("--color-match", action="store_true",
                   help="Match the render's colour to the original in LAB, measured inside the KEEP area")
    p.add_argument("--label", default="", help="Caption for the before/after page")
    p.add_argument("--dry-run", action="store_true", help="No writes")
    return p.parse_args()


def load_rgb(path) -> Image.Image:
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def color_match_lab(render: Image.Image, original: Image.Image, keep: np.ndarray) -> Image.Image:
    """Shift the render's LAB mean/std to the original's, using only KEEP pixels as the reference.

    Both images show the same fixed elements there, so any difference is model colour drift
    (e.g. the pink cast reported for Gemini at 2K/4K)."""
    sel = keep > 0.5
    if sel.sum() < 1000:  # too little shared area to measure drift reliably
        return render
    r = np.asarray(render.convert("LAB"), dtype=np.float32)
    o = np.asarray(original.convert("LAB"), dtype=np.float32)
    out = r.copy()
    for c in range(3):
        rm, rs = r[..., c][sel].mean(), r[..., c][sel].std() + 1e-6
        om, os_ = o[..., c][sel].mean(), o[..., c][sel].std() + 1e-6
        out[..., c] = (r[..., c] - rm) * (os_ / rs) + om
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "LAB").convert("RGB")


def build_alpha(mask_path, size, erode: int, feather: int) -> np.ndarray:
    m = Image.open(mask_path).convert("L").resize(size, Image.NEAREST)
    if erode > 0:
        m = m.filter(ImageFilter.MinFilter(erode * 2 + 1))
    if feather > 0:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    return np.asarray(m, dtype=np.float32)[..., None] / 255.0


def run(original, render, mask, output_dir, feather=9, erode=2, color_match=False, label="", dry_run=False) -> dict:
    orig = load_rgb(original)
    rend = load_rgb(render)
    resized = rend.size != orig.size
    if resized:
        rend = rend.resize(orig.size, Image.LANCZOS)

    hard_keep = np.asarray(Image.open(mask).convert("L").resize(orig.size, Image.NEAREST), dtype=np.float32) / 255.0
    if color_match:
        rend = color_match_lab(rend, orig, hard_keep)

    alpha = build_alpha(mask, orig.size, erode, feather)
    o = np.asarray(orig, dtype=np.float32)
    r = np.asarray(rend, dtype=np.float32)
    out = Image.fromarray(np.clip(o * alpha + r * (1 - alpha), 0, 255).astype(np.uint8), "RGB")

    # How much the model changed the fixed area before we restored it (mean abs diff, 0-255).
    drift = float(np.abs(o - r)[hard_keep > 0.5].mean()) if (hard_keep > 0.5).any() else 0.0

    out_dir = Path(output_dir)
    out_path = out_dir / f"{Path(original).stem}__{Path(render).stem}.png"
    result = {"output": str(out_path), "size": list(orig.size), "render_was_resized": resized,
              "keep_fraction": round(float(hard_keep.mean()), 3),
              "fixed_area_drift_before_restore": round(drift, 2), "color_match": color_match}
    if dry_run:
        return {**result, "dry_run": True}

    out_dir.mkdir(parents=True, exist_ok=True)
    out.save(out_path)

    # Keep an untouched copy of the "before" next to the result so the HTML page is self-contained.
    before_path = out_dir / f"{Path(original).stem}__original.jpg"
    if not before_path.exists():
        orig.save(before_path, quality=92)

    pairs_path = out_dir / "pairs.json"
    pairs = json.loads(pairs_path.read_text()) if pairs_path.exists() else []
    pairs = [p for p in pairs if p.get("after") != out_path.name]
    pairs.append({"before": before_path.name, "after": out_path.name, "label": label or Path(render).stem})
    pairs_path.write_text(json.dumps(pairs, indent=2, ensure_ascii=False))
    return {**result, "pairs": str(pairs_path)}


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.original, a.render, a.mask, a.output, a.feather, a.erode,
                                                 a.color_match, a.label, a.dry_run)}, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
