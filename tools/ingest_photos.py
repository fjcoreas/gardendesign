"""
ingest_photos.py
Purpose:  Normalize garden photos (EXIF rotation, sRGB, max size) and write a catalog by zone.
Used by:  workflows/entender_jardin.md (step 1)
Inputs:   Folder of JPG/PNG photos (default inputs/fotos)
Outputs:  .tmp/fotos/<name>.png and .tmp/catalogo.json (name, size, panoramic flag, zona='' to be filled by agent)
Env vars: none (see .env.example)
Cost:     free
Status:   STUB - logic not implemented yet.
"""
import argparse, json, sys
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageOps

load_dotenv()
TMP_DIR = Path(".tmp"); TMP_DIR.mkdir(exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description="Normalize garden photos (EXIF rotation, sRGB, max size) and write a catalog by zone.")
    p.add_argument("--input", default="inputs/fotos", help="Folder with original photos")
    p.add_argument("--output", default=str(TMP_DIR / "catalogo.json"), help="Catalog JSON path")
    p.add_argument("--max-side", type=int, default=2048, help="Longest side after resize")
    p.add_argument("--dry-run", action="store_true", help="No writes, no paid API calls")
    return p.parse_args()


def run(input_path, output_path, max_side=2048, dry_run=False) -> dict:
    # TODO: for each photo: ImageOps.exif_transpose -> convert to sRGB (drop P3 ICC) -> resize to max_side
    #       -> save PNG in .tmp/fotos/ -> record {name, original_size, size, aspect, panoramic: aspect>2.2, zona: ""}
    #       -> keep existing 'zona' values if catalog already exists.
    raise NotImplementedError("Stub. See workflows/entender_jardin.md for the spec.")


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.input, a.output, a.max_side, a.dry_run)}, indent=2, ensure_ascii=False)); return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
