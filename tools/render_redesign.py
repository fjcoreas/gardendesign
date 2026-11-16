"""
render_redesign.py
Purpose:  Send photo + prompt (+ optional reference images) to the Gemini image model and save the edited image.
Used by:  workflows/disenar_y_renderizar_zona.md (step 6)
Inputs:   Photo, prompt text file, optional --ref images (max 3)
Outputs:  <output>/<photo-stem>__<timestamp>.png and a .json sidecar (model, prompt, refs, sizes, usage)
Env vars: GEMINI_API_KEY (optional in the cloud session: the proxy injects the Network secret),
          GEMINI_IMAGE_MODEL (default gemini-nano-banana-2.1)
Cost:     PAID (~$0.03-0.11 per image) - ask the user before batches of more than ~10.
Status:   Implemented for provider=gemini (REST, no SDK). provider=openai is still a stub.
"""
import argparse, base64, io, json, os, sys, time, urllib.error, urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from PIL import Image, ImageOps

load_dotenv()
TMP_DIR = Path(".tmp")
API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
# Aspect ratios the Gemini image models accept.
RATIOS = {"1:1": 1.0, "2:3": 2 / 3, "3:2": 1.5, "3:4": 0.75, "4:3": 4 / 3, "4:5": 0.8, "5:4": 1.25,
          "9:16": 9 / 16, "16:9": 16 / 9, "21:9": 21 / 9}


def parse_args():
    p = argparse.ArgumentParser(description="Render a garden redesign with the image model.")
    p.add_argument("--photo", required=True)
    p.add_argument("--prompt", required=True, help="Path to prompt .txt")
    p.add_argument("--ref", action="append", default=[], help="Reference image (repeatable, max 3)")
    p.add_argument("--output", default=str(TMP_DIR / "renders"))
    p.add_argument("--provider", choices=["gemini", "openai"], default="gemini")
    p.add_argument("--resolution", choices=["1K", "2K", "4K"], default="2K")
    p.add_argument("--model", default=None, help="Override GEMINI_IMAGE_MODEL")
    p.add_argument("--dry-run", action="store_true", help="Print the request summary; no API call")
    return p.parse_args()


def closest_ratio(w: int, h: int) -> tuple[str, float]:
    name = min(RATIOS, key=lambda k: abs(RATIOS[k] - w / h))
    return name, abs(RATIOS[name] - w / h) / (w / h)


def image_part(path) -> dict:
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=95)
    return {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}}


def post(url: str, body: dict, retries: int = 2) -> dict:
    key = os.environ.get("GEMINI_API_KEY") or "proxy-injected"
    data = json.dumps(body).encode()
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers={"Content-Type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:800]
            if e.code in (429, 500, 503) and attempt < retries:
                time.sleep(10 * (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {e.code}: {detail}") from None


def run(photo, prompt_path, refs, output_dir, provider="gemini", resolution="2K", model=None, dry_run=False) -> dict:
    if provider != "gemini":
        raise NotImplementedError("provider=openai is the fallback and is not implemented yet (ask the user first).")
    if len(refs) > 3:
        raise ValueError("Use at most 3 reference images (more tends to confuse the model).")
    model = model or os.environ.get("GEMINI_IMAGE_MODEL") or "gemini-nano-banana-2.1"
    prompt = Path(prompt_path).read_text(encoding="utf-8").strip()
    w, h = ImageOps.exif_transpose(Image.open(photo)).size
    ratio, ratio_err = closest_ratio(w, h)

    summary = {"model": model, "photo": str(photo), "photo_size": [w, h], "aspect_ratio": ratio,
               "aspect_mismatch_pct": round(ratio_err * 100, 1), "resolution": resolution,
               "refs": refs, "prompt_chars": len(prompt)}
    if ratio_err > 0.05:
        summary["warning"] = (f"Photo aspect {w}x{h} is {ratio_err:.0%} away from {ratio}; the composite will stretch "
                              "the render. Prefer a photo closer to a supported ratio (e.g. crop the panorama).")
    if dry_run:
        return {**summary, "dry_run": True}

    parts = [image_part(photo)] + [image_part(r) for r in refs] + [{"text": prompt}]
    gen_cfg = {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": ratio, "imageSize": resolution}}
    body = {"contents": [{"role": "user", "parts": parts}], "generationConfig": gen_cfg}
    url = API.format(model=model)
    try:
        resp = post(url, body)
    except RuntimeError as e:
        if "imageSize" not in str(e):
            raise
        gen_cfg["imageConfig"].pop("imageSize")  # some models reject imageSize; retry without it
        summary["note"] = "Model rejected imageSize; used its default resolution."
        resp = post(url, body)

    img_bytes, text_out = None, []
    for cand in resp.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "inlineData" in part and img_bytes is None:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
            elif "text" in part:
                text_out.append(part["text"])
    if img_bytes is None:
        reason = [c.get("finishReason") for c in resp.get("candidates", [])] or resp.get("promptFeedback")
        raise RuntimeError(f"No image returned. finish/feedback: {reason}. Text: {' '.join(text_out)[:300]}")

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = out_dir / f"{Path(photo).stem}__{stamp}.png"
    img = Image.open(io.BytesIO(img_bytes))
    img.save(out_path)
    sidecar = {**summary, "output": str(out_path), "output_size": list(img.size), "prompt": prompt,
               "model_text": " ".join(text_out)[:1000], "usage": resp.get("usageMetadata"),
               "created": stamp}
    out_path.with_suffix(".json").write_text(json.dumps(sidecar, indent=2, ensure_ascii=False))
    return {k: sidecar[k] for k in ("output", "output_size", "model", "aspect_ratio", "usage")} | \
        ({"warning": summary["warning"]} if "warning" in summary else {})


def main():
    a = parse_args()
    try:
        print(json.dumps({"status": "ok", **run(a.photo, a.prompt, a.ref, a.output, a.provider, a.resolution,
                                                 a.model, a.dry_run)}, indent=2, ensure_ascii=False))
        return 0
    except Exception as e:
        print(json.dumps({"status": "error", "error": type(e).__name__, "message": str(e)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
