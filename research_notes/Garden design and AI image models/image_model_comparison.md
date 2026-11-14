# AI image-editing models for photo-faithful garden redesign (as of 14 Nov 2026)

> **How these notes were researched, and how much to trust them.** Research date: 2026-11-14. Direct page fetches failed because these hosts aren't in this session's allowed network: **ai.google.dev and arena.ai** (so the remaining primary pages were not tried). All findings below come from web-search results: search snippets plus the search tool's own summaries of the pages, which name the cited URLs. **Many cited pages are third-party blogs or API resellers, not vendor pages.** Prices and limits should be checked against the official pages (ai.google.dev/gemini-api/docs/pricing, developers.openai.com, bfl.ai/pricing, BytePlus) before building. To fetch those pages, ai.google.dev and arena.ai must be added to the session's network settings. Dates are given where the search results showed them. Items marked **[>6 mo, possibly outdated]** date from before about May 2026.

## Q1. Candidate comparison: masks, preservation, photorealism, multi-image consistency, resolution, API, price

### Takeaway
As of Nov 2026, the field has moved well past the models named in the brief. Google's current editing model is **Nano Banana 2.1**. OpenAI's are **GPT Image 2.5/2.6** ("Sunburst"/"Flare"). BFL now ships **FLUX.2 and FLUX 3 Image**. Alibaba has **Qwen-Image 2.1 (open) and 3.0 (API)**, and ByteDance has **Seedream 5.0/5.5**. The older candidates are gone or obsolete: Gemini 2.5 Flash Image retired 2 Oct 2026, and Imagen editing on Vertex is shut down. No instruction-based model guarantees pixel-identical unedited regions. True binary-mask inpainting is offered only by OpenAI's edit endpoint, FLUX.1 Fill (Pro/dev), and open models via ComfyUI (Qwen-Image inpaint ControlNet, SD/SDXL). Gemini and FLUX 3 use "mask painted on the image" or prompt-described regions instead.

### Comparison table

| Model (vendor) | Mask / inpainting? | Preservation of unedited areas (known issues) | Multi-image reference input | Max resolution | API / SDK | Price per image (standard) | Date of key info |
|---|---|---|---|---|---|---|---|
| **Nano Banana 2.1** (`gemini-nano-banana-2.1`, Google) | No separate mask file. You paint the mask onto the input image and describe the change in the prompt. Release notes reportedly single out mask editing for improvement | Vendor and blog claims of clean edges (marketing). One blog test: when asked to change only the background, it also changed clothing, while GPT Image 2.6 changed nothing else. Earlier Gemini image models had forum reports of a pink/magenta cast at 2K/4K and downscaled or stretched output | Up to 14 reference images (most sources). One tool caps at 10; one source says unconfirmed | 4K (1K/2K/4K tiers) | Gemini API (google-genai SDK), Vertex AI, fal, Replicate | ~$0.0336 (1K), $0.0504 (2K), $0.113 (4K). Batch is about 50% | Listed as current general model, Oct 21 2026 |
| **Nano Banana 2 Lite** (`gemini-3.1-flash-lite-image`) | Same approach as Nano Banana 2.1 | No specific data | Not found | 1K only | Gemini API | $0.0336 (1K) | Nov 2026 aggregators |
| **Nano Banana Pro** (`gemini-3-pro-image`) | Instruction-based. Same painted-mask approach | Forum report: magenta tint and detail loss at 4K on Vertex. Pink cast on edits at 2K/4K (via Replicate and Vertex) | Yes (count not confirmed in these results) | 4K | Gemini API, Vertex | $0.134 (1K/2K), $0.24 (4K) | Pricing Nov 2026. Model launched about Nov 2025 **[>6 mo]** |
| **Nano Banana 2** (`gemini-3.1-flash-image`) | Instruction-based | Same pink-cast report | Yes | 4K | Gemini API | $0.067 / $0.101 / $0.151 (1K/2K/4K). One source says deprecated, no shutdown date | Nov 2026 |
| **Gemini 2.5 Flash Image** (original "Nano Banana") | Instruction-based. Developers say it accepts no explicit mask | Forum: returned 832x1248 from a 3808x5712 input (downscaling). Photoshop users: stretched, not pixel-accurate | Yes | ~1K | (retired) | ~$0.039 | **Retired 2 Oct 2026. Do not use** |
| **Imagen 3 editing** (`imagen-3.0-capability-001/002`, Vertex) | Was true mask inpainting | n/a | n/a | n/a | **Discontinued** (release notes: 24 Mar 2026; reports of Vertex removal 30 Jun and Gemini API removal 17 Aug 2026). No mask-based Gemini replacement | n/a | Mar–Oct 2026 |
| **GPT Image 2.5 / 2.6 Sunburst & Flare** (OpenAI) | **Yes, a true binary mask**: B/W PNG, white = editable. Must match the input size; OpenAI reportedly requires an alpha channel. 2.6 adds "markup-guided edits" (sources conflict on whether these replace masks) | Docs: gpt-image-2 always processes inputs at high fidelity (`input_fidelity` can't be set). One blog test: background-only edit changed nothing else. Its outputs are still regenerated, not composited. No measured pixel-diff data found | Yes. Extra input images cost ~$0.0085 each (fal measurement) | Any size meeting the constraints. fal lists max ~8.29 MP, longest side 4000 px | OpenAI Images API (`images.edit`), official SDKs, also on fal | Token-billed: $8/M image-input, $30/M image-output tokens. Measured ~$0.04–0.06 per 1K edit | Rates checked 5 Nov 2026 by a reseller |
| **FLUX 3 Image** (BFL) | **No mask field.** You target regions with bounding boxes written into the prompt, through a unified endpoint. Marketed as "edit one thing, keep the rest", with staged multi-step editing | Vendor claim only | 1–10 reference images | Up to 4K | BFL API, fal, Replicate | ~$0.048 at 1K on fal. One source says $0.024 on Replicate (conflict) | Image launch around Oct 2026 (dates conflict) |
| **FLUX.2 [pro]/[max]** (BFL) | Instruction and reference editing. No dedicated mask endpoint found | No data found | Yes (multi-reference) | per-MP pricing | BFL API, Replicate, fal | Pro: $0.03 first MP + $0.015 per extra MP. Max: $0.07 + $0.03. Image-to-image about $0.045 (Pro) / $0.10 (Max) at 1 MP | BFL pricing page possibly stale **[>6 mo]** |
| **FLUX.1 Kontext pro/max/dev** | Instruction-based | Photoshop users: "pixel-accurate", unlike Nano Banana | Limited | ~1 MP | BFL, fal, Replicate | ~$0.04 (pro) / $0.08 (max) | **[>6 mo]**. BFL now recommends FLUX.2 for new work |
| **FLUX.1 Fill [pro] / [dev]** (BFL) | **Yes, true mask inpainting** (`/v1/flux-pro-1.0-fill`, base64 mask). Still BFL's dedicated mask tool | Only the masked region is generated | No | ~1–2 MP | BFL API, AI SDK, fal | $0.05 (BFL Pro). fal dev Fill with LoRAs $0.037 | **[>6 mo]** model, still listed |
| **Qwen-Image 2.1 / 2.1-Turbo** (Alibaba, open weights) | Unified generation and editing. Mask inpainting through ComfyUI inpaint model patches / InstantX inpainting ControlNet | No data found | Yes (edit references) | n/a | Hugging Face, ModelScope, fal | fal: Qwen Image Edit ~$0.021, Edit 2511 ~$0.037 (or $0.02/MP) | Released 20 Sep / 9 Oct 2026. License disputed (Qwen Research License, non-commercial, per one review) |
| **Qwen-Image-Edit-2511** (open, Apache 2.0) | Edit model. Depth, canny and inpaint control in ComfyUI | No data | Yes | n/a | HF, fal, ComfyUI | ~$0.037 on fal | Dec 2025 **[>6 mo]** |
| **Qwen-Image 3.0 / 3.0 Pro** | API only, no weights | No data | n/a | n/a | Alibaba Cloud API | not found | 2026 |
| **Seedream 5.0 Pro / 5.5** (ByteDance) | Instruction-based editing. 5.5 marketed as "100 rounds of editing", transparency, layers | Seedream 5.0 Pro topped Artificial Analysis' identity-preserving-edits category (about Sep 2026) | Yes. The first reference is free, then $0.003 per extra reference | 5.0 Pro has a price break above 2.36 MP | BytePlus ModelArk API, aggregators | 5.0 Pro: $0.045 (≤2.36 MP), $0.09 above. 5.0 Lite $0.035. 5.5 packs from $0.02 | Nov 11 2026 (5.5) |
| **SeedEdit 3.0** | Instruction edit | — | — | — | BytePlus | ~$0.03 | **[>6 mo]** |
| **SD / SDXL / SD3 + ControlNet** (ComfyUI) | **Yes, full mask inpainting** plus depth, segmentation and canny ControlNet | Only the masked area changes, and VAE seams can be composited out | Via IP-Adapter (not researched) | depends on model | Self-host or ComfyUI cloud | GPU time | No 2026-specific source found. FLUX/Qwen ComfyUI workflows have largely replaced it |
| **Adobe Firefly Generative Fill (Firefly Services API)** | Yes (mask-based fill) | No data | n/a | n/a | Enterprise API ("Operations" metering). One source says enterprise contracts start around $1,000/mo | No public per-image price (one blog says ~$0.02, unverified) | 2026 blogs |
| **Ideogram 4.x** | "Precise Edit" / edit with references | No data | Yes (references) | n/a | Ideogram API | Generation $0.03–0.10. Ideogram 4.5 High with references/Precise Edit $0.22 | 2026 blogs |
| **Recraft V4.1** | Inpaint exists. No price found | No data | n/a | n/a | Recraft API | Generation ~$0.035–0.04 (raster) | 2026 blogs |
| **Microsoft MAI-Image-2.6/2.7-Preview** (not in brief) | Not researched | Ranks #4 on both Arena and AA edit boards | — | — | Microsoft | — | Nov 2026 |
| **Mistral** | **No Mistral-built image model.** Le Chat's editing uses BFL's Kontext | — | — | — | No Mistral image API found | — | See Q6 |

### Cited Findings
**Google Gemini / Nano Banana**
- Nano Banana 2.1 (`gemini-nano-banana-2.1`) costs about $0.0336 (1K), $0.0504 (2K) and $0.113 (4K). It was listed as the current general model as of Oct 21 2026. Nano Banana 2 Lite (`gemini-3.1-flash-lite-image`) is $0.0336 at 1K only. Nano Banana Pro (`gemini-3-pro-image`) is $0.134 at 1K/2K and $0.24 at 4K. Nano Banana 2 (`gemini-3.1-flash-image`) is $0.067/$0.101/$0.151. Original Nano Banana (`gemini-2.5-flash-image`) was about $0.039 and retires 2 Oct 2026 — [benchlm.ai](https://benchlm.ai/media-pricing/nano-banana); [developersdigest.tech](https://www.developersdigest.tech/models/image-generation/google-gemini-api); [renderahouse.com](https://www.renderahouse.com/blog/nano-banana-pricing)
- Every Nano Banana model has a Batch tier at half the standard rate (e.g. Nano Banana 2.1 batch $0.0168 per 1K image). Billing is per output token: $120, $60 and $30 per 1M image-output tokens for Pro, Nano Banana 2 and 2 Lite — [blog.laozhang.ai](https://blog.laozhang.ai/en/posts/nano-banana-api-pricing-free-vs-pro); [benchlm.ai](https://benchlm.ai/media-pricing/nano-banana)
- Sources conflict on pricing: picassoia lists Nano Banana 2 at $0.034 for 1K, which looks like the batch rate. curlscape (about 124 days old) has older figures — [blog.picassoia.com](https://blog.picassoia.com/gemini-image-api-pricing-rate-limits-resolution-and-python); [curlscape.com](https://curlscape.com/blog/google-gemini-api-pricing-guide-2026)
- Nano Banana 2.1: there is no separate mask file. The mask is painted onto the input image and the prompt says what that area should become. Up to 14 reference images. 1K/2K/4K output — [fal.ai/nano-banana-2.1](https://fal.ai/nano-banana-2.1); [fal.ai learn guide](https://fal.ai/learn/tools/how-to-use-nano-banana-2-1); [felo.ai](https://felo.ai/blog/nano-banana-2-1-on-felo/). Fuser caps references at 10 — [fuser.studio](https://fuser.studio/articles/nano-banana-prompt-guide). Kie.ai says the reference limit is unconfirmed — [kie.ai](https://kie.ai/blog/what-is-nano-banana-2-1)
- A developer write-up advises masking or compositing with the original photo when content must stay pixel-exact, because reference-based generation cannot guarantee it — [dev.to](https://dev.to/drew_grant_7c81ce9e84426a/nano-banana-21-treat-image-edits-like-testable-specs-3do1)
- Side-by-side test: asked to change only the background, Nano Banana 2.1 also swapped shorts for jeans, while GPT Image 2.6 changed nothing else. The source advises naming every element that must stay — single blog test, via [Picsart blog](https://picsart.com/blog/gpt-image-2-6-sunburst-vs-nano-banana-2-1) / [linkmodel.ai](https://www.linkmodel.ai/blog/gpt-image-2-6-vs-nano-banana-2-1) (the search summary did not say which of the comparison pages it came from)
- Known issues (community reports, no official Google acknowledgment found):
  - A pink color cast on edited images from Nano Banana Pro and Nano Banana 2, at 2K/4K, reproducible on Replicate and Vertex AI — [discuss.ai.google.dev](https://discuss.ai.google.dev/t/edited-images-return-with-a-slight-pink-color-cast-after-migration-from-preview-to-image/176315)
  - A magenta tint and distortion with Gemini 3 Pro at 4K on Vertex — [discuss.ai.google.dev](https://discuss.ai.google.dev/t/regresion-de-calidad-persistente-deformacion-y-tinte-magenta-en-gemini-3-pro-4k-vertex-ai/183342)
  - Tiled background artifacts at 4K — [discuss.ai.google.dev](https://discuss.ai.google.dev/t/4k-image-generation-produces-repeating-tiled-background-artifacts-after-migration-from-preview-to-image/175782)
  - Gemini 2.5 Flash Image returned 832x1248 from a 3808x5712 input — [discuss.ai.google.dev](https://discuss.ai.google.dev/t/gemini-2-5-flash-image-only-downloads-low-resolution-images/101868)
  - Photoshop Generative Fill with Nano Banana gives stretched, non-pixel-accurate results, while Flux Kontext Pro was pixel-accurate — [community.adobe.com](https://community.adobe.com/t5/bug-photoshop-beta/generative-fill-with-gemini-2.5-(nano-banana)-is-giving-stretched-results/idi-p/15534785); [community.adobe.com](https://community.adobe.com/t5/photoshop-beta-bugs/nano-banana-bug-generating-smaller-results/idi-p/15531196)
  - Converting Display P3 (iPhone) photos to sRGB before upload avoids some color shifts — [docs.apiyi.com](https://docs.apiyi.com/en/faq/banana-pro-edit-red-cast) (third-party)
- Imagen editing: Vertex AI release notes list `imagen-3.0-capability-001/-002` as discontinued on 24 Mar 2026, with `gemini-2.5-flash-image` as the replacement — [Vertex AI release notes](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/release-notes). A developer forum thread says no mask-based editing replacement exists — [discuss.google.dev](https://discuss.google.dev/t/imagen-3-0-capability-001-retiring-june-30-no-mask-based-editing-replacement-exists/343602). A GitHub PR says the model was removed from Vertex on 30 Jun and from the Gemini API on 17 Aug, and saw 404s on 29 Oct 2026 — [github.com/Tehnolabs/pixelforge-mcp PR #22](https://github.com/Tehnolabs/pixelforge-mcp/pull/22); [chatforest.com](https://chatforest.com/builders-log/google-imagen-deprecated-june-2026-gemini-image-migration-builder-guide/); [ud.hk](https://www.ud.hk/en/blogs/insight/article/image-model-after-imagen-2026-08-17). Exact dates conflict between sources

**OpenAI**
- The official guide says that for gpt-image-2 you should omit `input_fidelity`, because the model always processes image inputs at high fidelity. It also says gpt-image-2 accepts any size that meets its constraints — [developers.openai.com image-generation guide](https://developers.openai.com/api/docs/guides/image-generation); [images.edit reference](https://developers.openai.com/api/reference/ruby/resources/images/methods/edit)
- Mask: a black-and-white PNG where white marks the editable area, matching the input dimensions. Pixel limits: 655,340 to 8,294,400 total, longest side 4000 px (fal listing) — [fal.ai gpt-image-2 edit](https://fal.ai/models/openai/gpt-image-2/edit). The image and mask must share format and size, and the mask needs an alpha channel. Mask size limit: 4 MB vs 50 MB (sources conflict) — [adpicto.com](https://www.adpicto.com/en/blog/gpt-image-2-image-editing-workflow)
- GPT Image 2.6 Sunburst/Flare token rates: $5 per M text input, $8 per M image input, $30 per M image output, checked against OpenAI on 5 Nov 2026. Same rates as 2.5 — [kie.ai](https://kie.ai/blog/gpt-image-2-6-pricing); [mockingbirdhouse.com](https://www.mockingbirdhouse.com/guides/gpt-image-2-6-pricing)
- Measured costs: a one-image edit was about $0.060 (Mockingbird). Medium-quality 1K on fal was about $0.041. Each extra input image (including a mask) adds about $0.0085. Medium quality costs 2–3x more than in 2.5 — [dev.to (fal measurement)](https://dev.to/lygerone/gpt-image-26-pricing-what-one-edit-really-costs-on-fal-measured-5aan); [mockingbirdhouse.com](https://www.mockingbirdhouse.com/guides/gpt-image-2-6-pricing)
- Markup-guided edits in 2.6: one source says they use the same token rates. Another says a markup overlay is a separate $2.00 input that replaces binary masks and can't be combined with them — [eesel.ai](https://www.eesel.ai/blog/chatgpt-images-2-6) vs [kie.ai](https://kie.ai/blog/gpt-image-2-6-pricing) (unresolved conflict)

**Black Forest Labs**
- FLUX.2 pricing per megapixel: Pro $0.03 for the first MP plus $0.015 for each extra MP. Max $0.07 plus $0.03. The page may be stale — [bfl.ai/pricing](https://bfl.ai/pricing). Image-to-image at 1 MP: $0.045 (Pro) and $0.10 (Max) — [getclaudeskills.com BFL guide](https://www.getclaudeskills.com/skills/bfl-api-integration-guide-calesthio)
- FLUX.1 Kontext Pro is about $0.04 and Max about $0.08. BFL now recommends FLUX.2 for new editing work — [magichour.ai](https://magichour.ai/blog/what-is-flux1-kontext)
- FLUX.1 Fill: the dedicated mask endpoint is `/v1/flux-pro-1.0-fill` at $0.05 and takes a base64 mask — [getclaudeskills.com](https://www.getclaudeskills.com/skills/bfl-api-integration-guide-calesthio). The AI SDK shows `prompt.mask` with `flux-pro-1.0-fill` — [ai-sdk.dev](https://ai-sdk.dev/providers/ai-sdk-providers/black-forest-labs)
- The Flux.3 series was announced on 23 Jul 2026 — [Wikipedia: Flux](https://en.wikipedia.org/wiki/Flux_(text-to-image_model)). FLUX 3 Image: no mask field; you target regions with bounding boxes in the prompt; 1–10 reference images; up to 4K; open-weights Image Klein is 5.6B; FLUX 3 Dev has no date — [eachlabs.ai](https://www.eachlabs.ai/blog/flux-3-image-explained); [layer3labs.io](https://www.layer3labs.io/guides/flux-3-image-explained); [dataist.ai](https://dataist.ai/news/black-forest-labs-releases-flux-3-image-with-staged-editing/); [aifrontierpost.com](https://aifrontierpost.com/articles/flux-3-image-black-forest-labs-launch/). Image launch coverage is dated around 2 Oct 2026; one source said the release date was unconfirmed as of 8 Oct
- FLUX.3 at 1K: $0.048 on fal vs $0.024 on Replicate (conflict) — [teamday.ai](https://www.teamday.ai/blog/ai-image-video-api-providers-comparison-2026); [teamday.ai fal pricing](https://www.teamday.ai/blog/fal-ai-pricing-2026)

**Qwen**
- Qwen-Image-2.1 was released 20 Sep 2026. It unifies generation and editing: a 7B DiT with a Qwen3-VL 8B encoder and native RGBA. 2.1-Turbo (8 steps) followed on 9 Oct 2026 — [eesel.ai review](https://www.eesel.ai/blog/qwen-image-2-1-review); [x.com/Alibaba_Qwen](https://x.com/Alibaba_Qwen/status/2101659302792679789); [artrealmai.com](https://artrealmai.com/article/qwen-image-2-1-turbo-8-step-open-weights)
- License: one review says Qwen-Image-2.1 is non-commercial only (Qwen Research License) — [cellcog.ai](https://cellcog.ai/blog/qwen-image-2-1/). Qwen-Image-Edit (Aug 2025) and Edit-2511 (Dec 2025) were Apache 2.0. Qwen-Image 3.0/3.0 Pro are API-only — [invideo.io](https://invideo.io/blog/qwen-image-ai-generator/); [picassoia](https://blog.picassoia.com/qwen-image-3-0-open-source-weights-api-and-local-setup)
- ComfyUI's official Qwen-Image docs list canny, depth and inpaint model patches. Comfy Hub has a Qwen-Image InstantX inpainting ControlNet workflow (mask in LoadImage) — [docs.comfy.org](https://docs.comfy.org/tutorials/image/qwen/qwen-image); [comfy.org hub](https://comfy.org/hub/workflows/qwen-image-instantx-inpainting-controlnet-15538e51d812/)

**ByteDance**
- Seedream 5.0 Pro: $0.045 per output up to 2.36 MP and $0.09 above. The first reference image is free, then $0.003 each. 5.0 Lite costs from $0.035. Seedream 5.5 first-purchase packs start at $0.02 per image (as of 11 Nov 2026). One source gives 5.0 Pro as $0.075 (conflict) — [therundown.ai](https://www.therundown.ai/tools/seedream-5-0-pro); [myclaw.ai](https://myclaw.ai/blog/seedream-5-5-review); [cellcog.ai](https://cellcog.ai/blog/seedream-5-5/); [tech-insider.org](https://tech-insider.org/how-to-use-seedream-5-0-pro-lite-2026/)
- SeedEdit 3.0 is about $0.03 — [ai-best-search.com](https://ai-best-search.com/en/products/seedream) **[>6 mo]**

**Other vendors**
- Adobe Firefly API: no public per-image price. Metered in "Operations" under enterprise contracts; one estimate puts the minimum around $1,000/mo — [sudomock.com](https://sudomock.com/blog/adobe-firefly-api-pricing-2026); [toolcolumn.com](https://www.toolcolumn.com/tools/adobe-firefly)
- Ideogram: 4.0 API generation costs $0.03/$0.06/$0.10. Ideogram 4.5 High with references/Precise Edit costs $0.22. Recraft V4.1 raster generation costs $0.035, with no inpaint price found — [eesel.ai](https://www.eesel.ai/blog/chatgpt-images-2-5-alternatives); [datanorth.ai](https://datanorth.ai/blog/top-10-best-ai-image-generation-tools-2026)

### Inferences
- **Photorealism on outdoor and architectural scenes:** no source benchmarked garden or landscape scenes specifically. Arena "single-image edit" rankings (Q5) are the best available proxy. They favor GPT Image 2.5/2.6, then MAI, then Nano Banana 2.1 (reported 1427 vs 1476 for 2.6 Sunburst).
- **Only true masked inpainting confines changes by construction:** OpenAI edit with a mask, FLUX Fill, and ComfyUI Qwen/SD inpaint. Even OpenAI regenerates the full frame, so compositing the original pixels back is still needed for "pixel-identical" walls and sky. Gemini and FLUX 3 are instruction or painted-mask models and will drift without compositing.
- **Design consistency across several photos:** multi-reference input is the only mechanism found. Nano Banana 2.1 takes up to 14 images, FLUX 3 up to 10, and Seedream and GPT Image also take references. A practical approach is to pass the first approved redesigned view as a reference image when editing the other angles, along with a written design spec from Claude.
- The brief's named models are outdated:
  - "Gemini 2.5 Flash Image" is retired.
  - gpt-image-1 has been succeeded by gpt-image-2/2.5/2.6.
  - FLUX.1 Kontext has been succeeded by FLUX.2/FLUX 3.
  - Qwen-Image-Edit has been succeeded by Qwen-Image 2.1/3.0.
  - Seedream 4 has been succeeded by 5.x.

### Gaps
- No published benchmark measures pixel-level preservation (PSNR/SSIM outside the edit region) or color drift for any 2026 model. The color and resolution evidence is anecdotal forum posts.
- Official Google docs for Nano Banana 2.1 (mask handling, input resolution, aspect ratios, reference limit) could not be fetched because ai.google.dev is blocked in this session.
- No confirmation found on whether Qwen-Image 2.1 supports native mask inpainting outside ComfyUI patches.
- No FLUX 3 Image per-image price on BFL's own page was found. Release date details conflict.
- Firefly, Ideogram and Recraft edit/inpaint API prices could not be verified.
- No 2026-specific evaluation found for SD3/SDXL inpainting. These appear to have been displaced by FLUX/Qwen workflows (inference).

## Q2. Gemini consumer app vs API usage limits

### Takeaway
There's no free API tier for the Nano Banana models (some free use exists in AI Studio). The Gemini app reportedly switched after I/O 2026 to compute-based limits that refresh every 5 hours with a weekly cap, replacing fixed daily image counts. The figures are inconsistent, and official numbers weren't fetched.

### Cited Findings
- There's no free API tier for these models, but the Gemini app and Google AI Studio offer some free image generation. One source says Nano Banana 2 is in the AI Studio free tier with rate limits — [developersdigest.tech](https://www.developersdigest.tech/models/image-generation/google-gemini-api); [aifreeapi.com](https://www.aifreeapi.com/en/posts/gemini-image-generation-free-api); [blog.laozhang.ai](https://blog.laozhang.ai/en/posts/nano-banana-api-pricing-free-vs-pro)
- Since I/O 2026, the Gemini app reportedly uses compute-based limits, refreshing every 5 hours with a weekly cap. Free users get Nano Banana 2 at standard limits; Nano Banana Pro "redos" need a paid tier (source about 5 days old) — [whizi.io](https://whizi.io/resources/gemini-image-generation-limit/)
- Older daily caps (pre-I/O 2026) **[>6 mo]**:
  - Free: 2–3 Nano Banana Pro images per day, then up to 100 per day on Nano Banana (2.5 Flash Image)
  - AI Pro: 100 per day
  - AI Ultra: 1,000 Nano Banana Pro images per day
  - AI Plus: up to 50 per day
  - Sources: [aifreeapi.com](https://www.aifreeapi.com/en/posts/nano-banana-pro-rate-limits); [seamui.com](https://www.seamui.com/guides/gemini/gemini-image-generation-daily-limits); [9to5google.com (Jan 12 2026)](https://9to5google.com/2026/01/12/gemini-nano-banana-pro-milestone/)
- One guide says Google published no Gemini image generation limit as of Oct 2026 — [blog.laozhang.ai](https://blog.laozhang.ai/en/posts/gemini-image-generation-free-limit-2026)
- Consumer-subscription pricing context: Pro is $19.99/mo — [renderahouse.com](https://www.renderahouse.com/blog/nano-banana-pricing)

### Inferences
- For a weekend build, the API is the right channel even though the user has Gemini app access. The app offers no masks, no programmatic compositing and no repeatable prompts. At roughly $0.03–0.11 per image, 100–200 test edits on Nano Banana 2.1 cost about $5–20. The user's "mediocre results with naive prompts" likely reflect the lack of masking and compositing as much as prompt quality.

### Gaps
- Official Gemini app limits page (support.google.com) and API rate-limit tiers not fetched. Whether a consumer Google AI Pro subscription includes any API credit was not established.

## Q3. Hybrid "keep this, change that" pipeline and weekend feasibility in Python

### Takeaway
The robust pattern is: segment, then edit (masked or instruction), then composite the original pixels back over the fixed regions with a feathered edge. This is widely recommended, and every component has a mature Python path. SAM 3 now does text-prompted segmentation directly in Hugging Face Transformers, replacing the Grounding DINO + SAM 2 combination. It's a realistic weekend build.

### Cited Findings
- Developers recommend masking or compositing with the original photo whenever content must stay pixel-exact, because generation can't guarantee it — [dev.to](https://dev.to/drew_grant_7c81ce9e84426a/nano-banana-21-treat-image-edits-like-testable-specs-3do1)
- SAM 3 (`facebook/sam3`) is in Hugging Face Transformers (`Sam3Model`, `Sam3Processor`). It takes text "concept prompts" (short noun phrases) and returns masks, boxes and scores — [huggingface.co/facebook/sam3](https://huggingface.co/facebook/sam3); [HF Transformers docs](https://huggingface.co/docs/transformers/model_doc/sam3)
- Meta's `sam3` package uses `set_text_prompt` and returns (N,H,W) binary masks. The checkpoint is about 1.7 GB — [stable-learn.com](https://stable-learn.com/en/sam3-segment-anything-model-tutorial/); [Roboflow blog](https://blog.roboflow.com/segment-anything-with-text/)
- Roboflow offers a hosted SAM 3 `concept_segment` API (needs an API key), for running without a GPU — [Roboflow blog](https://blog.roboflow.com/segment-anything-with-text/)
- PyImageSearch has 2026 tutorials on SAM 3 multi-modal prompting and an agentic SAM 3 + Qwen segmentation pipeline (Jan–Apr 2026) — [pyimagesearch.com](https://pyimagesearch.com/2026/02/02/advanced-sam-3-multi-modal-prompting-and-interactive-segmentation/); [pyimagesearch.com](https://pyimagesearch.com/2026/04/06/agentic-ai-vision-system-object-segmentation-with-sam-3-and-qwen/)
- ComfyUI depth- and mask-guided options: FLUX Fill plus Depth with automatic crop-and-stitch inpainting (Flux Continuum), and Qwen-Image depth/canny/inpaint patches. The common pattern for architecture is a depth map to keep geometry plus a mask of only the area to change — [github.com/robertvoy/ComfyUI-Flux-Continuum](https://github.com/robertvoy/Comfyui-Flux-Continuum); [docs.comfy.org](https://docs.comfy.org/tutorials/image/qwen/qwen-image); [runcomfy.com](https://www.runcomfy.com/comfyui-workflows/flux-controlnet-inpainting-image-repair) **[>6 mo]**
- Convert to sRGB before upload to avoid color shifts from Display P3 photos — [docs.apiyi.com](https://docs.apiyi.com/en/faq/banana-pro-edit-red-cast)
- Repeated edits in one session can reduce resolution and fidelity; start fresh from the original each time — [ecommerce-ai.beehiiv.com](https://ecommerce-ai.beehiiv.com/p/fix-your-ai-image-quality)

### Inferences
Suggested weekend pipeline. This is an inference from the components above; no source describes this exact pipeline for gardens.
1. Normalize the photo: EXIF rotate, convert to sRGB, record the size.
2. Run SAM 3 with prompts like "house", "wall", "fence", "sky", "tree" to get a KEEP mask. Optionally also prompt "lawn", "flower bed", "path" for an EDIT mask. Use Roboflow's hosted endpoint, or run on CPU/Colab if there's no GPU. Have the user approve the mask with a quick overlay preview.
3. Edit with the chosen model. Claude writes a design spec, then per-view instructions. For Gemini, paint or describe the editable region. For OpenAI or FLUX Fill, pass the binary mask.
4. Resize the output back to the original size. Optionally match colors to the original in the KEEP region (histogram or mean/std matching in LAB), which corrects the pink cast. Then alpha-composite the original over the KEEP mask, using a feathered (Gaussian-blurred, about 5–15 px) and slightly eroded mask to hide seams.
5. For other angles, feed the first approved render as a reference image along with the shared design spec.

Estimated effort: about 200–400 lines of Python (google-genai or openai SDK, transformers, Pillow/OpenCV, numpy), plus a simple Gradio/Streamlit UI. That is feasible in a weekend. The hardest parts are mask quality at boundaries (tree canopies and fences against planting) and blending lighting and shadows across the seam.

Hosted inpainting endpoints avoid the need for a local GPU. The weakest step without one is SAM 3; use CPU, Colab, Roboflow or a fal/Replicate SAM endpoint.

### Gaps
- No source evaluates the full segment, edit and composite pipeline on outdoor or garden photos, so the effort estimate above is my own.
- Grounded-SAM 2's current status vs SAM 3 was not covered by search results.
- Availability of hosted SAM 3 on fal or Replicate was not verified.

## Q4. Hosting open models without a GPU: Replicate, fal.ai, Together

### Takeaway
fal.ai has the broadest catalog of edit and inpaint endpoints: Qwen Image Edit ~$0.021–0.037, FLUX dev Fill ~$0.037, plus Nano Banana 2.1, GPT Image 2 and FLUX 3. Replicate bills per output or per GPU-second and is sometimes cheaper for FLUX. No Together-specific edit pricing was found.

### Cited Findings
- fal: Qwen Image Edit ~$0.021, Edit Plus $0.031, Edit 2511 $0.037. FLUX.1 [dev] Fill with LoRAs $0.037, with no Replicate equivalent listed — [pricepertoken.com](https://pricepertoken.com/fal-ai-pricing). Another source gives Qwen at $0.02/MP on fal — [costbench.com](https://costbench.com/software/ai-media-apis/fal-ai/)
- FLUX.2 Pro: Replicate charges $0.015 plus $0.015 per input/output MP (about $0.055 per 1024² with one input). fal charges about $0.073 — [theplanettools.ai](https://theplanettools.ai/tools/flux-2)
- FLUX.3 at 1K: $0.024 on Replicate vs $0.048 on fal (Nov 2026; sources conflict) — [teamday.ai](https://www.teamday.ai/blog/ai-image-video-api-providers-comparison-2026)
- Replicate bills per output or per second of GPU compute depending on the model — [techsy.io](https://techsy.io/en/blog/best-ai-image-providers); [apiscout.dev](https://apiscout.dev/guides/fal-ai-vs-replicate-vs-modal-2026)
- Nano Banana Pro and Nano Banana 2 are available through Replicate (forum reports of the pink cast via Replicate) — [discuss.ai.google.dev](https://discuss.ai.google.dev/t/edited-images-return-with-a-slight-pink-color-cast-after-migration-from-preview-to-image/176315). Nano Banana 2.1 is on fal — [fal.ai/nano-banana-2.1](https://fal.ai/nano-banana-2.1). GPT Image 2 edit is on fal — [fal.ai](https://fal.ai/models/openai/gpt-image-2/edit)

### Inferences
- With one fal key, you could A/B test Nano Banana 2.1, GPT Image 2.x, FLUX 3, FLUX Fill and Qwen Edit from a single Python client. That is convenient for a weekend comparison, even if the user ends up calling Google directly.

### Gaps
- Together AI's image edit catalog and prices weren't found.
- Official fal and Replicate pricing pages weren't fetched; the figures come from aggregators, some vendor-affiliated.
- ComfyUI cloud hosting options (RunComfy, Comfy Cloud) and their pricing weren't researched.

## Q5. Independent rankings (LMArena / Arena, Artificial Analysis), 2025–2026

### Takeaway
As of Nov 2026, OpenAI's GPT Image 2.5/2.6 (Sunburst, Flare) lead both the Arena (formerly LMArena) image-edit board and Artificial Analysis' AA-Image-Editing v2.1. Microsoft MAI-Image-2.7-Preview is fourth on both. Nano Banana 2.1 is reportedly about 50 Elo behind the leader on Arena. Leaders vary by task category.

### Cited Findings
- Arena single-image edit (12 Nov 2026; 64 models; ~31.9M votes):
  1. GPT-Image-2.5 Sunburst, 1519
  2. GPT-Image-2.5 Flare, 1484
  3. GPT-Image-2.6 Sunburst (Medium), 1476
  4. MAI-Image-2.7-Preview, 1471
  - Multi-image edit: GPT-Image-2.5 Sunburst 1525, Flare 1475
  - Product/commercial design (8 Nov 2026): Sunburst first, 1542
  - Sources: [arena.ai/leaderboard/image-edit](https://arena.ai/leaderboard/image-edit); [arena.ai multi-image](https://arena.ai/leaderboard/image/image-edit/multi-image); [arena.ai commercial design](https://arena.ai/leaderboard/image/image-edit/single-image-commercial-design) (from search snippets; direct fetch blocked)
- Reported Arena edit scores: GPT Image 2.6 Sunburst 1476 vs Nano Banana 2.1 1427 (2.6 preliminary at the time) — [GPT Image 2.6 vs Nano Banana 2.1 comparisons](https://www.orcarouter.ai/blog/gpt-image-2-6-vs-nano-banana-2-1); [teamorouter.com](https://teamorouter.com/blogs/gpt-image-2-6-vs-nano-banana-seedream-qwen) (unverified; the search summary didn't attribute this to a single page)
- llm-stats.com claims Gemini 3.1 Flash Image (Nano Banana 2) is the top image editor, with score 2858. That scale doesn't match Arena's, so it is likely a different metric or a stale snapshot — [llm-stats.com](https://llm-stats.com/leaderboards/best-ai-for-image-editing)
- Artificial Analysis AA-Image-Editing v2.1:
  1. GPT Image 2.6 Sunburst (max), 1210
  2. GPT Image 2.6 Flare (max), 1206
  4. MAI-Image-2.7-Preview, 1198
  - Source: [artificialanalysis.ai](https://artificialanalysis.ai/image/leaderboard/editing)
- About 72 days earlier (around early Sep 2026), AA rebuilt the arena into 17 categories. MAI-Image-2.6-Preview led overall and won 7 of the 17 boards. GPT Image 2 (high) was second, leading the object-level and composition categories. **Seedream 5.0 Pro led identity-preserving edits** — [superpowerdaily.com](https://superpowerdaily.com/posts/artificial-analysis-rebuilds-image-editing-arena-with-different-leaders-by-task); [alphasignal.ai](https://alphasignal.ai/news/artificial-analysis-rebuilds-its-image-editing-arena-across-17-specialized); [x.com/ArtificialAnlys](https://x.com/ArtificialAnlys/status/2095245450899239072)
- benchmarklist.com snapshots from late Aug / early Sep 2026 show GPT Image 2 on top (outdated) — [benchmarklist.com](https://benchmarklist.com/arenas/arena_ai_image_edit/)

### Inferences
- Arena votes reward overall visual appeal and instruction-following, not pixel preservation of untouched regions, so they are only a partial proxy for this use case. AA's "identity-preserving edits" category is the closest to "keep the house, change the garden", and Seedream 5.0 Pro led it in about Sep 2026.
- Open-weights models (Qwen, FLUX Klein) were not reported near the top in any snapshot found.

### Gaps
- Nano Banana 2.1's exact current Arena and AA rank couldn't be confirmed (pages not fetchable).
- No category specific to landscapes, exteriors or architecture was found on either board.
- The exact date of AA v2.1 wasn't confirmed.

## Q6. Does Mistral offer an image-editing model?

### Takeaway
No Mistral-built image generation or editing model was found. Le Chat's image generation and editing are powered by Black Forest Labs models, and the editing feature uses Kontext. No Mistral image-editing API was found.

### Cited Findings
- Mistral partnered with BFL to bring its Flux models into Le Chat (Flux Pro at launch, later called Flux Ultra) — [mistral.ai/news/mistral-chat](https://mistral.ai/news/mistral-chat/); [mistral.ai/news/all-new-le-chat](https://mistral.ai/news/all-new-le-chat/) **[>6 mo]**
- Le Chat added image editing with BFL (Kontext): text commands to remove objects or change scenes while keeping key elements. The announcement was about 485 days old — [the-decoder.com](https://the-decoder.com/mistral-ai-adds-deep-research-voice-mode-image-editing-and-more-to-le-chat/); [mistral.ai/news/le-chat-dives-deep](https://mistral.ai/news/le-chat-dives-deep/) **[>6 mo]**
- Wikipedia reports a May 2026 rebrand of Le Chat to "Mistral Vibe" (not verified against a primary source) — [Wikipedia: Mistral Vibe](https://en.wikipedia.org/wiki/Mistral_Vibe)

### Inferences
- For this project, Mistral adds nothing beyond using BFL directly. Going straight to BFL (FLUX Fill or FLUX 3) via the API is strictly more controllable.

### Gaps
- No 2026 Mistral announcement of an image model was found. Mistral's API docs weren't checked for a passthrough image endpoint.

---

### Synthesis for primary/fallback choice (inference, for the report writer)
- **Primary, "use what you have":** **Nano Banana 2.1 via the Gemini API.** It's cheap ($0.034–0.113), takes 14 references for cross-view consistency, outputs up to 4K, and the user already has a Google account. Wrap it in the SAM 3 mask, color-match and composite-back pipeline (Q3). That compositing removes Gemini's main weaknesses: drift outside the edit region, a possible pink cast, and size changes.
- **Fallback, "true mask and top-ranked quality":** **GPT Image 2.5/2.6 `images.edit` with a binary mask.** It leads Arena and AA, has explicit mask support, always uses high input fidelity, and preserved non-target content in one head-to-head test. It costs about $0.04–0.06 per edit.
- **Alternative fallback, "deterministic inpainting":** **FLUX.1 Fill [pro]** ($0.05, BFL or fal) for pure masked fill, or the open Qwen-Image Edit/inpaint models on fal (~$0.02–0.04).
- **Avoid:** Gemini 2.5 Flash Image (retired), Imagen editing (shut down), and Adobe Firefly API (enterprise-only).
