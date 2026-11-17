"""
composite_keep_regions.py
Purpose:  Paste original pixels back over the KEEP mask so fixed elements are guaranteed unchanged.
Used by:  workflows/disenar_y_renderizar_zona.md (step 7)
Inputs:   Original normalized photo, render, KEEP mask (255 = keep original)
Outputs:  <output>/<original-stem>__<render-stem>.png and an entry appended to <output>/pairs.json
Env vars: none
Cost:     free
Status:   Implemented. Optional step since 2026-11-16 (see workflow learnings): use --measure-only first.
"""
import argparse, json, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps


def parse_args():
    p = argparse.ArgumentParser(description="Paste original pixels back over the KEEP mask.")
    p.add_argument("--original", required=True)
    p.add_argument("--render", required=True)
    p.add_argument("--mask", required=True,
                   help="KEEP mask (255 = keep original), or 'auto' to keep everything except the region where the render "
                        "differs from the original (for small additions to an already-approved image)")
    p.add_argument("--diff-threshold", type=int, default=30, help="With --mask auto: per-pixel difference counted as a change")
    p.add_argument("--output", required=True, help="Output folder, e.g. outputs/renders/cesped")
    p.add_argument("--feather", type=int, default=9, help="Gaussian blur radius for the seam (5-15 px)")
    p.add_argument("--erode", type=int, default=2, help="Shrink keep mask before feathering (px)")
    p.add_argument("--color-match", action="store_true",
                   help="Match the render's colour to the original in LAB, measured inside the KEEP area")
    p.add_argument("--label", default="", help="Caption for the before/after page")
    p.add_argument("--measure-only", action="store_true",
                   help="Only measure camera drift (scale/rotation/shift) between original and render; no output")
    p.add_argument("--dry-run", action="store_true", help="No writes")
    return p.parse_args()


def load_rgb(path) -> Image.Image:
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def color_match_lab(render: Image.Image, original: Image.Image, keep: np.ndarray) -> Image.Image:
    """Shift the render's LAB mean/std to the original's, using only KEEP pixels as the reference.

    Both images show the same fixed elements there, so any difference is model colour drift
    (e.g. the pink cast reported for Gemini at 2K/4K). Uses OpenCV's float LAB (L 0-100, a/b signed);
    PIL's 8-bit LAB wraps the signed a/b channels and produced garish colours."""
    import cv2
    sel = keep > 0.5
    if sel.sum() < 1000:  # too little shared area to measure drift reliably
        return render
    r = cv2.cvtColor(np.asarray(render, dtype=np.float32) / 255.0, cv2.COLOR_RGB2LAB)
    o = cv2.cvtColor(np.asarray(original, dtype=np.float32) / 255.0, cv2.COLOR_RGB2LAB)
    out = r.copy()
    for c in range(3):
        rm, rs = r[..., c][sel].mean(), r[..., c][sel].std() + 1e-6
        om, os_ = o[..., c][sel].mean(), o[..., c][sel].std() + 1e-6
        out[..., c] = (r[..., c] - rm) * (os_ / rs) + om
    rgb = cv2.cvtColor(out, cv2.COLOR_LAB2RGB)
    return Image.fromarray(np.clip(rgb * 255.0, 0, 255).astype(np.uint8), "RGB")


def estimate_alignment(original: Image.Image, render: Image.Image, keep: np.ndarray):
    """Similarity transform (scale + rotation + shift) mapping ORIGINAL -> RENDER, fitted on keep pixels.

    Returns (2x3 matrix, info dict) or (None, info) if there are too few reliable matches."""
    import cv2
    go = cv2.cvtColor(np.asarray(original), cv2.COLOR_RGB2GRAY)
    gr = cv2.cvtColor(np.asarray(render), cv2.COLOR_RGB2GRAY)
    m = ((keep > 0.5) * 255).astype(np.uint8)
    sift = cv2.SIFT_create(5000)
    ko, do = sift.detectAndCompute(go, m)
    kr, dr = sift.detectAndCompute(gr, None)
    if do is None or dr is None or len(ko) < 10 or len(kr) < 10:
        return None, {"matches": 0}
    good = [a for a, b in cv2.BFMatcher().knnMatch(do, dr, k=2) if a.distance < 0.75 * b.distance]
    if len(good) < 12:
        return None, {"matches": len(good)}
    src = np.float32([ko[g.queryIdx].pt for g in good])
    dst = np.float32([kr[g.trainIdx].pt for g in good])
    A, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    n = int(inl.sum()) if inl is not None else 0
    if A is None or n < 10:
        return None, {"matches": len(good), "inliers": n}
    scale = float(np.hypot(A[0, 0], A[1, 0]))
    rot = float(np.degrees(np.arctan2(A[1, 0], A[0, 0])))
    return A, {"matches": len(good), "inliers": n, "scale": round(scale, 4), "rotation_deg": round(rot, 2),
               "shift_px": [round(float(A[0, 2]), 1), round(float(A[1, 2]), 1)]}


def auto_keep_mask(original: Image.Image, render: Image.Image, threshold: int = 30, grow: int = 25) -> Image.Image:
    """KEEP mask = everything except the area the model actually changed.

    Meant for a small addition to an approved image (original = approved image, render = same image + addition):
    pixel differences above `threshold` are grouped, small noise blobs dropped, and the changed area grown by `grow` px
    so its shadow and edges come from the render."""
    import cv2
    # Compare blurred images: the model re-draws fine textures (grass, leaves) everywhere, which a per-pixel diff
    # reads as change; blurring keeps only real shape/colour changes such as a new object.
    o = cv2.GaussianBlur(np.asarray(original, np.float32), (0, 0), 10)
    r = cv2.GaussianBlur(np.asarray(render, np.float32), (0, 0), 10)
    d = np.abs(o - r).max(axis=2)
    changed = (d > threshold).astype(np.uint8)
    changed = cv2.morphologyEx(changed, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(changed)
    min_area = 0.002 * changed.size
    keep_changed = np.zeros_like(changed)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            keep_changed[lab == i] = 1
    keep_changed = cv2.dilate(keep_changed, np.ones((grow * 2 + 1, grow * 2 + 1), np.uint8))
    return Image.fromarray(((1 - keep_changed) * 255).astype(np.uint8))


def build_alpha(mask_path, size, erode: int, feather: int) -> np.ndarray:
    m = mask_path if isinstance(mask_path, Image.Image) else Image.open(mask_path)
    m = m.convert("L").resize(size, Image.NEAREST)
    if erode > 0:
        m = m.filter(ImageFilter.MinFilter(erode * 2 + 1))
    if feather > 0:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    return np.asarray(m, dtype=np.float32)[..., None] / 255.0


def run(original, render, mask, output_dir, feather=9, erode=2, color_match=False, label="", dry_run=False,
        measure_only=False, diff_threshold=30) -> dict:
    orig = load_rgb(original)
    rend = load_rgb(render)
    resized = rend.size != orig.size
    if resized:
        rend = rend.resize(orig.size, Image.LANCZOS)
    if mask == "auto":
        mask = auto_keep_mask(orig, rend, diff_threshold)
    if measure_only:
        keep = np.asarray((mask if isinstance(mask, Image.Image) else Image.open(mask)).convert("L")
                          .resize(orig.size, Image.NEAREST), dtype=np.float32) / 255.0
        A, info = estimate_alignment(orig, rend, keep)
        drift = None if A is None else round(max(abs(info["scale"] - 1) * 100,
                                                 100 * float(np.hypot(*info["shift_px"])) / max(orig.size)), 1)
        return {"alignment": info, "drift_pct": drift,
                "composite_advised": drift is not None and drift <= 2.0,
                "note": "drift_pct = max(scale change, shift as % of longest side). Above ~2% compositing "
                        "creates double edges; deliver the render after visual QA instead."}

    mask_img = mask if isinstance(mask, Image.Image) else Image.open(mask)
    hard_keep = np.asarray(mask_img.convert("L").resize(orig.size, Image.NEAREST), dtype=np.float32) / 255.0
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
                                                 a.color_match, a.label, a.dry_run, a.measure_only,
                                                 a.diff_threshold)}, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
