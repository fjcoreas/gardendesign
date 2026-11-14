"""
make_before_after.py
Purpose:  Build a self-contained HTML page with before/after sliders for a zone.
Used by:  workflows/disenar_y_renderizar_zona.md (step 9), workflows/armar_plan_final.md
Inputs:   pairs.json ([{before, after, label}])
Outputs:  comparar.html next to pairs.json (images referenced relatively)
Env vars: none (see .env.example)
Cost:     free
Status:   STUB - logic not implemented yet.
"""
import argparse, json, sys
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
TMP_DIR = Path(".tmp"); TMP_DIR.mkdir(exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description="Build a self-contained HTML page with before/after sliders for a zone.")
    p.add_argument("--pairs", required=True, help="Path to pairs.json")
    p.add_argument("--output", required=True, help="HTML output path")
    p.add_argument("--title", default="Antes y después")
    p.add_argument("--dry-run", action="store_true", help="No writes, no paid API calls")
    return p.parse_args()


def run(pairs_path, output_path, title='Antes y después', dry_run=False) -> dict:
    # TODO: read pairs -> render HTML with one CSS/JS slider per pair (no external deps), Spanish labels.
    raise NotImplementedError("Stub. See workflows/disenar_y_renderizar_zona.md for the spec.")


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.pairs, a.output, a.title, a.dry_run)}, indent=2, ensure_ascii=False)); return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
