"""
composite_keep_regions.py
Purpose:  Paste original pixels back over the KEEP mask so fixed elements are guaranteed unchanged.
Used by:  workflows/disenar_y_renderizar_zona.md (step 7)
Inputs:   Original normalized photo, render, KEEP mask
Outputs:  outputs/renders/<zona>/<photo>__<variant>.png and an entry appended to pairs.json
Env vars: none (see .env.example)
Cost:     free
Status:   STUB - logic not implemented yet.
"""
import argparse, json, sys
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
from PIL import Image, ImageFilter

load_dotenv()
TMP_DIR = Path(".tmp"); TMP_DIR.mkdir(exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description="Paste original pixels back over the KEEP mask so fixed elements are guaranteed unchanged.")
    p.add_argument("--original", required=True)
    p.add_argument("--render", required=True)
    p.add_argument("--mask", required=True, help="KEEP mask, 255 = keep original")
    p.add_argument("--output", required=True, help="Output folder, e.g. outputs/renders/cesped")
    p.add_argument("--feather", type=int, default=9, help="Gaussian blur radius for the seam (5-15 px)")
    p.add_argument("--erode", type=int, default=2, help="Shrink keep mask before feathering")
    p.add_argument("--color-match", action="store_true", help="Match render to original in LAB inside KEEP area")
    p.add_argument("--dry-run", action="store_true", help="No writes, no paid API calls")
    return p.parse_args()


def run(original, render, mask, output_dir, feather=9, erode=2, color_match=False, dry_run=False) -> dict:
    # TODO: resize render to original size -> optional LAB mean/std colour match using KEEP pixels
    #       -> erode + feather mask -> out = original*m + render*(1-m) -> save PNG
    #       -> append {before, after, label} to <output>/pairs.json
    raise NotImplementedError("Stub. See workflows/disenar_y_renderizar_zona.md for the spec.")


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.original, a.render, a.mask, a.output, a.feather, a.erode, a.color_match, a.dry_run)}, indent=2, ensure_ascii=False)); return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
