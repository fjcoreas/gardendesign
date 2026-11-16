# Decisions log

| Date | Decision | Why |
|---|---|---|
| 2026-11-14 | Claude = designer (analysis, interview, design, prompts, QA). Separate image model = renderer. | Claude can't generate or edit images. |
| 2026-11-14 | Primary renderer: Gemini image model (Nano Banana 2.1) via API, not the app. Fallback: OpenAI GPT Image edit with mask. | Research report; user already has Google access. Mistral has no image model. |
| 2026-11-14 | Protect fixed elements by compositing original pixels back over a "keep" mask. | No model guarantees untouched regions. |
| 2026-11-14 | Generate each variant fresh from the original photo; avoid long chains of edits. | Repeated edits accumulate drift. |
| 2026-11-14 | Garden photos are committed to the repo (`inputs/fotos/`). | User asked to store them in the repo. |
| 2026-11-14 | Client-facing outputs in Spanish. | Clients are the user's parents in El Salvador. |
| 2026-11-14 | Budget presented in three tiers (básico / medio / completo). | Money budget unknown. |
| 2026-11-14 | Project docs and client outputs in Spanish; code and image prompts in English. | User switched to Spanish; image models follow English prompts better. |
| 2026-11-14 | Mask method left OPEN: try SAM 3 (local) or Gemini segmentation, fall back to a hand-painted mask. | No method tested yet. |
| 2026-11-16 | Gemini key stored as an environment Network secret (host generativelanguage.googleapis.com, header x-goog-api-key). Tools send a placeholder key; the proxy injects the real one. | Key never touches files or code. `Authorization` header does not work for this API. |
| 2026-11-16 | Model: `gemini-nano-banana-2.1`; in-Google fallback `gemini-3-pro-image`. | Both confirmed available via the API's model list. |
