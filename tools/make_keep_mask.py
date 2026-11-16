"""
make_keep_mask.py
Purpose:  Build the KEEP mask (white = fixed elements that must not change) for one photo.
Used by:  workflows/disenar_y_renderizar_zona.md (step 4)
Inputs:   Photo + comma-separated list of fixed elements in English (e.g. 'house,wall,sky')
Outputs:  <output>/<photo>_keep.png (L-mode, 255 = keep), <photo>_overlay.jpg for review,
          <photo>_segments.json (labels and boxes returned)
Env vars: GEMINI_API_KEY (optional in the cloud session: the proxy injects it), GEMINI_SEG_MODEL
Cost:     gemini: paid but tiny (<$0.01 per photo) | manual: free | sam3: not implemented
Status:   gemini and manual implemented. sam3 left as a stub (needs a large model download).
"""
import argparse, base64, io, json, os, sys, urllib.error, urllib.request
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from PIL import Image, ImageFilter, ImageOps

load_dotenv()
TMP_DIR = Path(".tmp")
API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

SEG_PROMPT = (
    "Give the segmentation masks for these objects in the photo: {items}. "
    "Return one entry per separate object instance (for example each wall separately). "
    "Output a JSON list where each entry contains the 2D bounding box in the key \"box_2d\", "
    "the segmentation mask in key \"mask\", and the text label in the key \"label\". "
    "Use the label names exactly as given."
)


def parse_args():
    p = argparse.ArgumentParser(description="Build the KEEP mask for one photo.")
    p.add_argument("--photo", required=True)
    p.add_argument("--keep", default="", help="Comma-separated fixed elements, e.g. 'house,brick wall,sky'")
    p.add_argument("--output", default=str(TMP_DIR / "masks"))
    p.add_argument("--method", choices=["gemini", "manual", "sam3"], default="gemini")
    p.add_argument("--planting-band", type=int, default=0,
                   help="Pixels removed from the bottom edge of keep regions so new planting can overlap them")
    p.add_argument("--manual-mask", help="Hand-painted mask to merge in (white = keep)")
    p.add_argument("--remove-mask", help="Hand-painted mask of areas that must be editable (white = editable)")
    p.add_argument("--model", default=None, help="Override GEMINI_SEG_MODEL (default gemini-3.8-flash)")
    p.add_argument("--dry-run", action="store_true", help="No API call, no writes")
    return p.parse_args()


def call_gemini(img: Image.Image, items: list[str], model: str) -> list[dict]:
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=92)
    body = {
        "contents": [{"role": "user", "parts": [
            {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}},
            {"text": SEG_PROMPT.format(items=", ".join(items))}]}],
        "generationConfig": {"temperature": 0.3, "responseMimeType": "application/json"},
    }
    if "2.5" in model:  # Google's segmentation guide recommends no thinking on 2.5 models
        body["generationConfig"]["thinkingConfig"] = {"thinkingBudget": 0}
    req = urllib.request.Request(API.format(model=model), data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json",
                                          "x-goog-api-key": os.environ.get("GEMINI_API_KEY") or "proxy-injected"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')[:600]}") from None
    text = "".join(p.get("text", "") for c in resp.get("candidates", [])
                   for p in c.get("content", {}).get("parts", []))
    text = text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)


def paint_segments(segments: list[dict], size: tuple[int, int]) -> np.ndarray:
    """box_2d is [y0, x0, y1, x1] normalised to 0-1000; mask is a PNG of the box area (probabilities 0-255)."""
    w, h = size
    keep = np.zeros((h, w), np.uint8)
    for s in segments:
        try:
            y0, x0, y1, x1 = s["box_2d"]
        except (KeyError, ValueError):
            continue
        x0, x1 = int(x0 / 1000 * w), int(x1 / 1000 * w)
        y0, y1 = int(y0 / 1000 * h), int(y1 / 1000 * h)
        if x1 <= x0 or y1 <= y0:
            continue
        m = s.get("mask", "")
        if m.startswith("data:image"):
            m = m.split(",", 1)[1]
        try:
            piece = Image.open(io.BytesIO(base64.b64decode(m))).convert("L").resize((x1 - x0, y1 - y0), Image.BILINEAR)
            region = (np.asarray(piece) > 127).astype(np.uint8) * 255
        except Exception:
            region = np.full((y1 - y0, x1 - x0), 255, np.uint8)  # no usable mask: fall back to the box
            s["mask_fallback_box"] = True
        keep[y0:y1, x0:x1] = np.maximum(keep[y0:y1, x0:x1], region)
    return keep


def carve_planting_band(keep: np.ndarray, band: int) -> np.ndarray:
    """Remove `band` px from the bottom of every keep region (wall/house feet) so planting can overlap it."""
    if band <= 0:
        return keep
    k = keep > 0
    shifted = np.zeros_like(k)
    shifted[:-band] = k[band:]  # pixel stays only if the pixel `band` rows below is also keep
    return (k & shifted).astype(np.uint8) * 255


def overlay(img: Image.Image, keep: np.ndarray) -> Image.Image:
    a = np.asarray(img, dtype=np.float32)
    tint = np.array([255, 60, 200], np.float32)
    k = (keep > 0)[..., None]
    return Image.fromarray(np.where(k, a * 0.55 + tint * 0.45, a).astype(np.uint8))


def run(photo, keep_items, output_dir, method="gemini", planting_band=0, manual_mask=None, remove_mask=None,
        model=None, dry_run=False) -> dict:
    img = ImageOps.exif_transpose(Image.open(photo)).convert("RGB")
    items = [s.strip() for s in keep_items.split(",") if s.strip()]
    model = model or os.environ.get("GEMINI_SEG_MODEL") or "gemini-3.8-flash"
    if dry_run:
        return {"photo": str(photo), "size": list(img.size), "method": method, "items": items, "dry_run": True}

    keep = np.zeros((img.height, img.width), np.uint8)
    segments = []
    if method == "gemini":
        if not items:
            raise ValueError("--keep is required for method=gemini")
        segments = call_gemini(img, items, model)
        keep = paint_segments(segments, img.size)
    elif method == "sam3":
        raise NotImplementedError("sam3 needs a large model download; use --method gemini or manual.")

    if manual_mask:
        mm = np.asarray(Image.open(manual_mask).convert("L").resize(img.size, Image.NEAREST)) > 127
        keep = np.maximum(keep, mm.astype(np.uint8) * 255)
    keep = carve_planting_band(keep, planting_band)
    if remove_mask:
        rm = np.asarray(Image.open(remove_mask).convert("L").resize(img.size, Image.NEAREST)) > 127
        keep[rm] = 0
    # Small cleanup: close pinholes in the mask.
    keep = np.asarray(Image.fromarray(keep).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)))

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = Path(photo).stem
    Image.fromarray(keep).save(out / f"{stem}_keep.png")
    overlay(img, keep).save(out / f"{stem}_overlay.jpg", quality=90)
    (out / f"{stem}_segments.json").write_text(json.dumps(
        [{k: v for k, v in s.items() if k != "mask"} for s in segments], indent=2, ensure_ascii=False))
    return {"mask": str(out / f"{stem}_keep.png"), "overlay": str(out / f"{stem}_overlay.jpg"),
            "keep_fraction": round(float((keep > 0).mean()), 3),
            "segments": [s.get("label") for s in segments]}


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.photo, a.keep, a.output, a.method, a.planting_band,
                                                 a.manual_mask, a.remove_mask, a.model, a.dry_run)},
                         indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
