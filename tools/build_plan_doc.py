"""
build_plan_doc.py
Purpose:  Convert the Markdown garden plan into a styled HTML (and optional PDF) document with images.
Used by:  workflows/armar_plan_final.md (step 3)
Inputs:   outputs/plan_jardin.md (with relative image links)
Outputs:  outputs/plan_jardin.html (and .pdf with --pdf)
Env vars: none (see .env.example)
Cost:     free
Status:   STUB - logic not implemented yet.
"""
import argparse, json, sys
from pathlib import Path
from dotenv import load_dotenv
import markdown

load_dotenv()
TMP_DIR = Path(".tmp"); TMP_DIR.mkdir(exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description="Convert the Markdown garden plan into a styled HTML (and optional PDF) document with images.")
    p.add_argument("--input", default="outputs/plan_jardin.md")
    p.add_argument("--output", default="outputs/plan_jardin.html")
    p.add_argument("--pdf", action="store_true", help="Also print to PDF via the pre-installed Chromium/Playwright")
    p.add_argument("--dry-run", action="store_true", help="No writes, no paid API calls")
    return p.parse_args()


def run(input_path, output_path, pdf=False, dry_run=False) -> dict:
    # TODO: markdown -> HTML with tables extension, simple warm garden CSS, images max-width 100%
    #       -> if --pdf: playwright chromium page.pdf().
    raise NotImplementedError("Stub. See workflows/armar_plan_final.md for the spec.")


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.input, a.output, a.pdf, a.dry_run)}, indent=2, ensure_ascii=False)); return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
