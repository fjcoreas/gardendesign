"""
render_redesign.py
Purpose:  Send photo + prompt (+ optional reference images) to the image model and save the edited image.
Used by:  workflows/disenar_y_renderizar_zona.md (step 6)
Inputs:   Normalized photo, prompt text file, optional --ref images (max 3)
Outputs:  .tmp/renders/<photo>__<timestamp>.png and a .json sidecar with model, prompt, refs, size
Env vars: GEMINI_API_KEY, GEMINI_IMAGE_MODEL (OPENAI_API_KEY if --provider openai) (see .env.example)
Cost:     PAID (~$0.03-0.11 per image) - ask before batches of >10
Status:   STUB - logic not implemented yet.
"""
import argparse, json, sys
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
TMP_DIR = Path(".tmp"); TMP_DIR.mkdir(exist_ok=True)


def parse_args():
    p = argparse.ArgumentParser(description="Send photo + prompt (+ optional reference images) to the image model and save the edited image.")
    p.add_argument("--photo", required=True)
    p.add_argument("--prompt", required=True, help="Path to prompt .txt")
    p.add_argument("--ref", action="append", default=[], help="Reference image (repeatable, max 3)")
    p.add_argument("--output", default=str(TMP_DIR / "renders"))
    p.add_argument("--provider", choices=["gemini", "openai"], default="gemini")
    p.add_argument("--resolution", choices=["1K", "2K", "4K"], default="2K")
    p.add_argument("--dry-run", action="store_true", help="No writes, no paid API calls")
    return p.parse_args()


def run(photo, prompt_path, refs, output_dir, provider='gemini', resolution='2K', dry_run=False) -> dict:
    # TODO:
    #  gemini -> google-genai client, model=os.environ["GEMINI_IMAGE_MODEL"], contents=[photo, *refs, prompt],
    #            set aspect ratio = closest supported to the photo, image size = resolution; save first image part.
    #  openai -> images.edit with inverted KEEP mask (fallback, ask user first).
    #  Always write the sidecar JSON. In --dry-run, print the request and do not call the API.
    raise NotImplementedError("Stub. See workflows/disenar_y_renderizar_zona.md for the spec.")


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.photo, a.prompt, a.ref, a.output, a.provider, a.resolution, a.dry_run)}, indent=2, ensure_ascii=False)); return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
