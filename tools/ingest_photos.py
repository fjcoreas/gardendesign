"""
ingest_photos.py
Purpose:  Normalize garden photos (EXIF rotation, sRGB, size) and centre-crop each one to the closest aspect ratio
          the image model accepts, so renders are never stretched. Writes a catalog.
Used by:  workflows/entender_jardin.md (step 1)
Inputs:   Folder of JPG/PNG photos (default inputs/fotos)
Outputs:  .tmp/fotos/<name>.jpg and .tmp/catalogo.json (name, sizes, ratio, crop, zona)
Env vars: none
Cost:     free
Status:   Implemented.
"""
import argparse, json, sys
from pathlib import Path

from PIL import Image, ImageOps

TMP_DIR = Path(".tmp")
RATIOS = {"1:1": 1.0, "2:3": 2 / 3, "3:2": 1.5, "3:4": 0.75, "4:3": 4 / 3, "4:5": 0.8, "5:4": 1.25,
          "9:16": 9 / 16, "16:9": 16 / 9, "21:9": 21 / 9}


def parse_args():
    p = argparse.ArgumentParser(description="Normalize photos and crop them to model-supported aspect ratios.")
    p.add_argument("--input", default="inputs/fotos", help="Folder with original photos")
    p.add_argument("--output", default=str(TMP_DIR / "catalogo.json"), help="Catalog JSON path")
    p.add_argument("--max-side", type=int, default=2048, help="Longest side after resize")
    p.add_argument("--tolerance", type=float, default=0.03, help="Crop only if the ratio is off by more than this")
    p.add_argument("--dry-run", action="store_true", help="No writes")
    return p.parse_args()


def crop_to_ratio(img: Image.Image, target: float) -> tuple[Image.Image, list[int]]:
    w, h = img.size
    if w / h > target:  # too wide: trim the sides
        nw = round(h * target)
        box = [(w - nw) // 2, 0, (w - nw) // 2 + nw, h]
    else:  # too tall: trim top and bottom
        nh = round(w / target)
        box = [0, (h - nh) // 2, w, (h - nh) // 2 + nh]
    return img.crop(box), box


def run(input_path, output_path, max_side=2048, tolerance=0.03, dry_run=False) -> dict:
    src = Path(input_path)
    photos = sorted(p for p in src.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"))
    if not photos:
        raise FileNotFoundError(f"No photos in {src}")
    out_path = Path(output_path)
    old = {e["name"]: e for e in json.loads(out_path.read_text())} if out_path.exists() else {}
    out_dir = TMP_DIR / "fotos"
    catalog = []
    for f in photos:
        img = ImageOps.exif_transpose(Image.open(f)).convert("RGB")  # convert() drops the ICC profile -> sRGB-ish
        w, h = img.size
        ratio = min(RATIOS, key=lambda k: abs(RATIOS[k] - w / h))
        off = abs(RATIOS[ratio] - w / h) / RATIOS[ratio]
        box = None
        if off > tolerance:
            img, box = crop_to_ratio(img, RATIOS[ratio])
        img.thumbnail((max_side, max_side), Image.LANCZOS)
        entry = {"name": f.stem, "source": str(f), "original_size": [w, h], "size": list(img.size),
                 "aspect_ratio": ratio, "cropped_box": box,
                 "kept_pct": 100.0 if box is None else round(100 * (box[2] - box[0]) * (box[3] - box[1]) / (w * h), 1),
                 "panoramic": w / h > 2.2, "path": str(out_dir / f"{f.stem}.jpg"),
                 "zona": old.get(f.stem, {}).get("zona", "")}
        catalog.append(entry)
        if not dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)
            img.save(out_dir / f"{f.stem}.jpg", quality=95)
    if not dry_run:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    return {"catalog": str(out_path), "photos": len(catalog),
            "cropped": [e["name"] for e in catalog if e["cropped_box"]], "dry_run": dry_run}


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.input, a.output, a.max_side, a.tolerance, a.dry_run)},
                         indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
