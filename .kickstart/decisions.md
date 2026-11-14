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
