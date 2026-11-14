"""
make_keep_mask.py
Purpose:  Build the KEEP mask (white = fixed elements that must not change) for one photo.
Used by:  workflows/disenar_y_renderizar_zona.md (step 4)
Inputs:   Normalized photo + comma-separated list of fixed elements in English (e.g. 'house,wall,tree,sky')
Outputs:  .tmp/masks/<photo>_keep.png (L-mode, 255 = keep) and <photo>_overlay.jpg for human review
Env vars: GEMINI_API_KEY (only if --method gemini) (see .env.example)
Cost:     free (sam3/manual) | paid (gemini)
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
    p = argparse.ArgumentParser(description="Build the KEEP mask (white = fixed elements that must not change) for one photo.")
    p.add_argument("--photo", required=True)
    p.add_argument("--keep", required=True, help="Comma-separated fixed elements, e.g. 'house,wall,avocado tree,sky'")
    p.add_argument("--output", default=str(TMP_DIR / "masks"))
    p.add_argument("--method", choices=["sam3", "gemini", "manual"], default="sam3",
                   help="OPEN: which method works best is still to be tested")
    p.add_argument("--planting-band", type=int, default=40,
                   help="Pixels carved out of the mask at the foot of walls/house so new planting can overlap them")
    p.add_argument("--manual-mask", help="Path to a hand-painted mask (method=manual)")
    p.add_argument("--dry-run", action="store_true", help="No writes, no paid API calls")
    return p.parse_args()


def run(photo, keep, output_dir, method='sam3', planting_band=40, manual_mask=None, dry_run=False) -> dict:
    # TODO:
    #  sam3   -> transformers SAM 3 text-prompted segmentation, one prompt per element, union of masks
    #  gemini -> ask Gemini for segmentation masks of the named elements (verify API support first)
    #  manual -> load --manual-mask, binarize
    #  then: carve planting band at the bottom edge of wall/house regions, light dilation,
    #  save keep.png + overlay (keep areas tinted) for review.
    raise NotImplementedError("Stub. See workflows/disenar_y_renderizar_zona.md for the spec.")


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.photo, a.keep, a.output, a.method, a.planting_band, a.manual_mask, a.dry_run)}, indent=2, ensure_ascii=False)); return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
