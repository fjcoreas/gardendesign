# Gemini Image-Editing Prompting for Garden Redesign, and the Landscape of AI Garden Design Apps

Research date: 2026-11-14.

Method note: In this cloud session only `cloud.google.com` could be fetched in full. `ai.google.dev`, `blog.google`, `developers.googleblog.com`, `dev.to`, `learn.rundiffusion.com`, `aifreeapi.com` and `finance.biggo.com` failed DNS resolution because they are outside the session's allowed network. Claims from those pages come from search-result summaries, not full reads, and are marked "(search summary)". To verify them, those hosts would need to be allowed in the session's network settings.

Model and date reference (flag: anything before 2026-05 is more than 6 months old):
- Gemini 2.5 Flash Image ("Nano Banana"). Official prompting guide dated 2025-08-28. **OLDER THAN 6 MONTHS.**
- Gemini 3 Pro Image ("Nano Banana Pro"). Google's "7 tips" blog post dates from late 2025, and the in-app draw-on-image feature from 2025-12-18. **OLDER THAN 6 MONTHS.**
- Gemini 3.1 Flash Image ("Nano Banana 2"). Covered in the Google Cloud guide of 2026-03-06. **OLDER THAN 6 MONTHS.**
- Nano Banana 2.1. Third-party sources say it was released 2026-10-06 and is built on Gemini 3.6 Flash. This is the newest model and is current.

---

## Part 1, Q1: What does Google's official guidance say about prompting Gemini image models for editing?

### Takeaway
Google's guidance is the same across all versions. Describe the scene in full sentences rather than keyword lists. Start with a strong verb. Use positive framing. Name the camera, lens and lighting. For edits, name the one thing to change and state explicitly that everything else stays exactly the same, including style, lighting and composition. Then refine conversationally. Google documents no architecture or landscape templates; its closest example is an interior "change only the sofa" edit.

### Cited Findings
- The Google Cloud "Ultimate Nano Banana prompting guide" (Khulan Davaajav and Hussain Chinoy, **2026-03-06**) covers Nano Banana 2 (Gemini 3.1 Flash Image) and Nano Banana Pro (Gemini 3 Pro Image). Its core rules: (1) be specific about subject, lighting and composition; (2) use positive framing, e.g. "empty street" instead of "no cars"; (3) control the camera with terms like "low angle" and "aerial view"; (4) iterate with conversational follow-ups. It also says to start prompts with a strong verb that states the primary operation. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- The same guide describes conversational editing without new references as using "text-based semantic masking (inpainting) to edit part of an image and leave the rest untouched", and says to be explicit about what must stay exactly the same. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- Formula for multimodal generation with references: "[Reference images] + [Relationship instruction] + [New scenario]". Verbatim example: "Using the attached napkin sketch as the structure and the attached fabric sample as the texture, transform this into a high-fidelity 3D armchair render. Place it in a sun-drenched, minimalist living room." — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- Formula for text-to-image: "[Subject] + [Action] + [Location/context] + [Composition] + [Style]". — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- Creative-direction vocabulary Google recommends:
  - Lighting: "Golden hour backlighting creating long shadows", "three-point softbox setup".
  - Lens: "wide-angle lens", "low-angle shot with a shallow depth of field (f/1.8)".
  - Color: "Cinematic color grading with muted teal tones".
  - Materials: name specific materials.
  — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- Google suggests a "Nano Banana + Gemini" workflow in which Gemini 3 writes the prompts and provides creative direction. This matches the plan to have Claude write prompts. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- The guide has no limitations section and no architecture, exterior or landscape examples. Its knowledge cutoff is January 2025 for both models. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- The official Gemini 2.5 Flash Image prompting guide (developers blog, **2025-08-28**, older than 6 months) has an inpainting template (search summary): change only a [specific element] to [new description], and keep everything else in the image exactly the same, preserving the original style, lighting and composition. Its worked example changes only a blue sofa to a vintage brown leather chesterfield and keeps the rest of the room, including pillows and lighting, unchanged. — [Google Developers Blog](https://developers.googleblog.com/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- The same guide says Gemini 2.5 Flash Image generally preserves the input image's aspect ratio when editing, but the prompt should state it explicitly if it does not (search summary). — [Google Developers Blog](https://developers.googleblog.com/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- The launch post describes "targeted transformation and precise local edits with natural language" (search summary). — [Google Developers Blog: Introducing Gemini 2.5 Flash Image](https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/)
- Google published "7 tips to get the most out of Nano Banana Pro" on the Gemini blog. Its prompting strategies range from photorealistic edits to imaginative scenes. Full text could not be retrieved. — [blog.google](https://blog.google/products/gemini/prompting-tips-nano-banana-pro/)
- TechRadar covered Google's call for user Nano Banana Pro prompts and three standout tips. Not fetched. — [TechRadar](https://www.techradar.com/ai-platforms-assistants/gemini/3-advanced-strategies-for-making-the-most-of-nano-banana-pro)
- A December 2025 Google AI Studio post gives 10 production tips for API users. It includes editing tasks such as removing objects, filling backgrounds and restoring photos through plain-language requests (secondary report). — [kocpc summary](https://en.kocpc.com.tw/?p=14441)

### Inferences
- A garden prompt should be a short paragraph in full sentences with this structure:
  1. Operation verb: "Redesign the garden areas in this photo…"
  2. What changes, described concretely: plants, materials and layout.
  3. An explicit preservation clause listing the house, walls, fences, named mature trees, sky, camera position, perspective and lighting.
  4. Photographic style matching the original.
- Phrase exclusions positively where possible, e.g. "the lawn is replaced by…" and "the brick wall remains exactly as it is", rather than piles of "no X".

### Gaps
- The full text of the ai.google.dev image-generation docs and the "7 tips" blog post could not be read because the hosts were blocked. Official 2026 guidance specific to Nano Banana 2.1 was not found in Google's own words.

---

## Part 1, Q2: Techniques for preserving regions (explicit keep-lists, semantic masking, mask or annotated images, sentences vs keywords, camera matching)

### Takeaway
Gemini image models take no pixel mask parameter in the documented workflow; "masking" is done in language. Two practical reinforcements exist. First, a visually annotated image: draw on the photo in the Gemini app, or burn colored boxes and labels into a copy. Second, an exhaustive keep-list written in plain sentences. Do one change per turn for best preservation.

### Cited Findings
- Google calls its language-based approach "text-based semantic masking": the model edits part of an image and leaves the rest untouched when told explicitly what to keep. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- The term "semantic masking" originally comes from Imagen's editing API, which has a documented semantic mask mode, a different model family. Google Cloud's Imagen guide calls mask-free editing ideal for subtle changes and style adjustments (search summary). — [Mintlify mirror of GoogleCloudPlatform generative-ai image editing](https://mintlify.com/GoogleCloudPlatform/generative-ai/vision/image-editing)
- **The Gemini app supports drawing on photos.** Under "Create image", users upload a photo and draw or annotate on it with circles, arrows and scribbles. A text prompt is optional. Tom's Guide dates the launch to **2025-12-18** (older than 6 months) and says it runs on Gemini 3. — [Tom's Guide](https://www.tomsguide.com/ai/ai-image-video/nano-banana-now-lets-you-draw-prompts-directly-on-your-photos-sam-altman-is-going-to-hate-this); [Tom's Guide hands-on](https://www.tomsguide.com/ai/i-stopped-typing-prompts-drawing-on-my-photos-with-googles-nano-banana-blew-me-away)
- **Annotated-image workaround (works through the API too).** Draw a green-bordered rectangle around the target area in Canva and add a text box describing the change. Upload the composite with the prompt: "Read the green text in the image and make the modifications. Remove the green text and boxes." — [Jim MacLeod, Medium](https://jimmacleod.medium.com/use-canva-to-guide-nano-banana-a-simple-step-by-step-tutorial-9e2df0c7455a)
- Adobe Photoshop's Nano Banana integration accepts handwritten annotations and arrows on the image to guide generative edits. Adobe notes that in Photoshop, Nano Banana is not a chat model. Krea's canvas also lets users highlight areas, draw arrows and add notes. — [Adobe](https://www.adobe.com/ca/learn/photoshop/web/nano-banana-generative-edits); [Krea](https://www.krea.ai/apps/edit/nano-banana-edit)
- Third-party advice:
  - Keep each edit to one change and add "keep everything else the same".
  - A chain of small edits beats one compound instruction.
  - List preserved features explicitly.
  (search summary of several guides) — [Leonardo.ai guide](https://leonardo.ai/news/nano-banana-prompt-guide); [PromptZone](https://www.promptzone.com/darcy_reddy/nano-banana-prompt-patterns-for-gemini-25-flash-image-447f)
- A short prompt that names the lighting, background and what stays unchanged tends to beat a long one. "Gemini tends to follow the clearest, most concrete instruction it's given rather than the most detailed one" (search summary). — [Lilach Bullock, 40 copy-paste edits (2026)](https://www.lilachbullock.com/nano-banana-prompts-copy-paste-gemini-image-edits/)
- Garden and exterior example phrasings from third-party guides (search summary):
  - "Using the provided photo of this backyard, remove the garden shed and the hose on the lawn. Keep everything else exactly the same."
  - "On this uploaded photo, change the concrete path to warm-toned clay pavers in a herringbone pattern. Keep existing plants."
  - "...keep the existing house, garden and lighting exactly as photographed."
  — [Lilach Bullock](https://www.lilachbullock.com/nano-banana-prompts-copy-paste-gemini-image-edits/); [Eden LG, AI garden design with Nano Banana](https://edenlg.co.ke/ai-garden-design-how-to-use-nano-banana-to-plan-and-visualize-your-dream-garden/); [RenderAHouse, 50 architecture prompts](https://www.renderahouse.com/blog/nano-banana-architecture-prompts)
- Google endorses camera and lens vocabulary ("wide-angle lens", "low angle", "aerial view") and lighting vocabulary ("golden hour backlighting creating long shadows"). — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- Full sentences over keywords: Google's formulas are written as narrative sentences, and its examples are full descriptive prose. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- A 2026 arXiv survey with a Nano Banana case study recommends an explicit non-edit mask plus a copy-paste fallback for unmodified regions to counter pixel drift (search summary). — [arXiv 2604.28185](https://arxiv.org/pdf/2604.28185)

### Inferences
- **Best preservation strategy for a custom build: post-composite.** Let Gemini redesign, then paste back the original pixels for the fixed regions (house, sky, walls) using a mask. The mask can come from manual drawing or a segmentation model. This guarantees fixed elements stay pixel-identical and avoids resolution or color drift in those areas. The arXiv survey's copy-paste fallback supports this.
- For the Gemini app with no code, use the draw-on-image feature to outline the garden beds to redesign. Pair it with a text keep-list.
- When the photo makes it ambiguous, describe fixed elements concretely so the model can identify them, e.g. "the red-brick two-storey house on the left", "the white picket fence along the back", "the large oak tree in the right corner".
- Camera matching: say "Keep the exact same camera position, focal length, framing and perspective as the original photo." State the time of day and light direction seen in the original, e.g. "soft overcast afternoon light from the left".

### Gaps
- I could not confirm from official docs whether the Gemini API accepts a binary mask image as a formal input for Gemini image models. Evidence points to no: masking is language-based and an image can only be passed as another reference image. A mask passed as a second image with instructions is untested in the sources found.
- I found no head-to-head test of annotated-image vs text-only preservation accuracy for exteriors.

---

## Part 1, Q3: Iterative multi-turn editing vs one-shot; quality degradation; consistency across multiple photos

### Takeaway
Multi-turn editing improves instruction following but degrades pixels. Noise, JPEG-like artifacts and global color shifts accumulate turn by turn in untouched areas, and this is documented in academic papers and reported even for Nano Banana 2.1. Two mitigations: (1) restart from the original photo for each major variant rather than chaining many edits; (2) for consistency across photos, reuse one written "design brief / style sheet" and attach a reference image of an approved redesign.

### Cited Findings
- A 2026 arXiv survey's Nano Banana case study finds subtle JPEG-style noise in turn 1 that intensifies turn by turn. It argues that long context does not solve pixel-level fidelity (search summary). — [arXiv 2604.28185](https://arxiv.org/pdf/2604.28185)
- The FreqEdit paper reports that Nano Banana introduces undesirable global color shifts across editing rounds while still scoring well on subject consistency (search summary). — [arXiv 2512.01755](https://arxiv.org/pdf/2512.01755)
- A paper on DiT editors attributes part of the drift to small per-turn biases accumulating through the VAE encode/decode round trip (search summary). — [arXiv 2605.08250](https://arxiv.org/pdf/2605.08250)
- The "Banana100" paper studies 100 iterative image replications with Nano Banana Pro (search result title; details not read). — [arXiv 2604.03400](https://arxiv.org/pdf/2604.03400)
- EdiVal-Agent finds Nano Banana benefits from multi-turn formulation for instruction following and performs strongly at preserving base-image appearance across turns (search summary). This partly contradicts the degradation findings above: object-level preservation is good while pixel-level fidelity degrades. — [arXiv 2509.13399](https://arxiv.org/pdf/2509.13399)
- BigGo Finance's Nano Banana 2.1 hands-on (**late 2026**, search summary): the first edit is clean, but untouched areas pick up noise, color drift and texture distortion as edits pile up. Multi-round editing remains a weak spot, and the cause is unconfirmed. — [BigGo Finance](https://finance.biggo.com/news/9c87ca6e-67c8-4ff2-92d3-ec6bff899c8a)
- Vendor-blog advice, not independently verified (search summary):
  - Re-anchor to the original reference every 5–8 prompts; consistency holds for about 8–10 sequential edits.
  - Change one variable at a time.
  - Keep scene/style references separate from subject references, e.g. "Image 1 as subject reference, Image 2 as scene/style reference".
  — [Futurepedia](https://www.futurepedia.io/courses/google-nano-banana-create-and-edit-in-minutes/lessons/character-cosistency-across-scenes); [WisGate](https://wisgate.ai/blogs/what-is-nano-banana-pro-a-practical-guide-to-multi-image-and-reference-based-generation); [Astorie](https://astorie.ai/blog/nano-banana-2-workflows)
- Sources disagree on how many references help. One says five inconsistent photos confuse the model, another says 3–4 is the sweet spot, and Pro officially accepts up to 14. — [Futurepedia](https://www.futurepedia.io/courses/google-nano-banana-create-and-edit-in-minutes/lessons/character-cosistency-across-scenes); [UD HK, 2026-06-29](https://www.ud.hk/en/blogs/insight/article/2026-06-29-nano-banana-consistent-characters)
- Google's official multimodal formula, "[Reference images] + [Relationship instruction] + [New scenario]", supports labelled roles per reference image. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)

### Inferences
- **Recommended workflow:**
  1. Write one canonical "garden design brief". It covers style, a plant palette with specific named species, hardscape materials and colors, and season. Have Claude reuse the brief verbatim in every prompt for every photo.
  2. Generate each photo's redesign one-shot from the original photo.
  3. Use at most 1–3 small follow-up turns.
  4. For bigger changes, go back to the original photo with a revised full prompt rather than editing the edit.
  5. Once one view is approved, attach it as a style reference for the other photos: "Image 2 shows the approved redesign of the same garden from another angle; use the same plants, materials and style".
- Gemini has no user-exposed seed control documented in the sources found, so consistency must come from the text brief and reference images.
- Color drift can be fixed afterwards by color-matching the output to the original. A custom build could do a histogram match on the preserved regions, or skip it entirely with the post-composite approach.

### Gaps
- I found no Reddit (r/GeminiAI, r/StableDiffusion) threads: search returned none. Practitioner evidence is limited to blogs.
- I could not confirm whether the API exposes a `seed` parameter for image models.

---

## Part 1, Q4: Known failure modes and workarounds

### Takeaway
The documented failure modes match the user's mediocre results:
- The model alters fixed structures, including the house.
- It replaces the actual landscape with generic imagery.
- Plants come out climate-inappropriate or unrealistic.
- Color shifts and noise accumulate over turns.
- Aspect ratio sometimes changes.
- Output is capped at lower resolution in the consumer app.

### Cited Findings
- **The model changes the house or building.** An App Store reviewer of an AI garden app says it "also change[s] the original house or office building you import". Another says the AI "can't keep your actual landscape in the design, instead replacing it with fake, generic images". The developer replied that the app produces "creative design inspirations", not exact replicas. — [App Store: Garden AI](https://apps.apple.com/us/app/garden-ai-landscape-design/id6738805390?see-all=reviews); [App Store: AI Garden Design](https://apps.apple.com/us/app/ai-garden-design-landscape-ai/id6744179402?see-all=reviews&platform=ipad)
- **Plants are wrong for the climate.** A reviewer reports "AI generated plants that were not appropriate for the zone I'm in (ex. Tropical plants for Northern VA)". — [App Store reviews via search summary](https://apps.apple.com/us/app/ai-garden-design-landscape-ai/id6744179402?see-all=reviews&platform=ipad)
- **Color shifts and noise accumulate** over turns (see Q3). — [arXiv 2512.01755](https://arxiv.org/pdf/2512.01755); [arXiv 2604.28185](https://arxiv.org/pdf/2604.28185)
- **Aspect ratio changes.** Google advises stating the aspect ratio explicitly in the prompt if the model fails to preserve it (search summary). — [Google Developers Blog](https://developers.googleblog.com/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- **Long, detailed prompts get ignored.** Gemini tends to follow the clearest, most concrete instruction rather than the most detailed one (search summary). — [Lilach Bullock](https://www.lilachbullock.com/nano-banana-prompts-copy-paste-gemini-image-edits/)
- **Negatives backfire.** Google recommends positive framing ("empty street" rather than "no cars"). — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- **Tiling on wide frames.** Nano Banana 2 could show tiling on very wide frames at 2K and 4K, reportedly fixed in 2.1 (third-party, search summary). — [Kenerate AI](https://kenerateai.com/model/nano-banana-2.1); [Fuser](https://fuser.studio/articles/nano-banana-2-1)

### Inferences
Workarounds to bake into Claude's prompts:
- Name each fixed element concretely and say it "must remain pixel-for-pixel identical in shape, color, position and texture".
- Specify the same framing, perspective and aspect ratio.
- Name real plant species suited to the garden's climate and region; Claude should ask for the location or hardiness zone. Describe them at a realistic size and maturity, e.g. "newly planted, 30–60 cm tall" or "established for 3 years".
- Ask for "photorealistic, as photographed with the same camera, no illustration or render look".
- Use 2K or 4K output via the API.
- Add a post-composite step for guaranteed preservation.

### Gaps
- I found no systematic study of "unrealistic plant" errors specifically for Gemini. The evidence is app-review anecdotes from apps that may use various models.

---

## Part 1, Q5: Gemini consumer app vs API / AI Studio

### Takeaway
The API and AI Studio give control over model choice, output resolution up to 4K (`image_size`), aspect ratio (10+ options), thinking level, and up to 14 reference images. The consumer app reportedly caps downloads at 1K (free) or 2K (AI plan), offers less explicit control, but has the convenient draw-on-image UI. For quality, use AI Studio or the API.

### Cited Findings
- **Resolution tiers:** 1K, 2K and 4K for Nano Banana 2 and Pro. Nano Banana 2 adds 512px. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- **Aspect ratios:** 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9 and 21:9. Nano Banana 2 Preview adds 1:4, 4:1, 1:8 and 8:1. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- **Reference images:** up to 14 per prompt. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- **Context windows:** Nano Banana 2 accepts 131,072 input tokens and Pro 65,536; both produce up to 32,768 output tokens. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- **Accepted formats:** PNG, JPEG, WebP, HEIC and HEIF. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- **Watermarking:** all outputs carry SynthID and C2PA Content Credentials. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- **Image fidelity limits:** the Gemini API docs say gemini-3-pro-image supports 5 images at high fidelity, out of 14 total (search summary). — [Gemini API docs (AI Studio)](https://aistudio.google.com/docs/image-generation)
- **URL inputs:** Vertex AI limits URL-passed images to 10 links (search summary). — [Google Cloud docs: Gemini 3 Pro Image](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-pro-image)
- **4K via API:** up to 4096 px on the longest side, set with `"image_size": "4K"` plus an aspect ratio in the response config. Reportedly not available on the free tier (search summary). — [Gemini API docs](https://aistudio.google.com/docs/image-generation); [prompt-architects](https://prompt-architects.com/blog/383-4k-image-workflows-with-nano-banana-pro)
- **Gemini app downloads:** reportedly 1K without a Google AI plan and 2K with one; paid users can "Redo with Pro" (third-party, search summary). — [Medium review](https://medium.com/@leucopsis/nano-banana-pro-googles-gemini-3-pro-image-model-a-review-11cbaee32ee1); [Explore AI Together](https://exploreaitogether.com/nano-banana/)
- **Nano Banana 2.1** (released **2026-10-06**, third-party sources):
  - Available in the Gemini app, AI Mode in Search, AI Studio, the Gemini API and Google Cloud, with GA status.
  - 1K, 2K and 4K output; 0.5K reportedly not supported.
  - Up to 14 input images; consistency for up to 4 characters and 10 objects.
  - New "medium" thinking level as default.
  - Grounding with Google Image Search.
  - About $0.0336 per 1K image vs $0.067 for Nano Banana 2.
  — [Unite.AI](https://www.unite.ai/nano-banana-2-1-debuts-at-half-the-image-cost-of-its-predecessor/); [Kenerate AI](https://kenerateai.com/model/nano-banana-2.1); [TechAIWire](https://techaiwire.com/articles/nano-banana-2-1-gemini-image-model-half-price/); [Morphic](https://morphic.com/resources/models/nano-banana-2-1)

### Inferences
- The user's mediocre results in the Gemini app likely come from several factors together: lower download resolution; no explicit aspect-ratio or resolution control; multi-turn drift; and short, keyword-ish prompts.
- **Recommended setup:** AI Studio (free UI with full controls) or a small Python script on the Gemini API. Choose Nano Banana Pro for top fidelity, or 2.1 for cost and recency. Use 2K or 4K output and set an aspect ratio matching the source photo.
- Image Search grounding in 2.1 could help render real named plant species accurately. This is untested.

### Gaps
- Official ai.google.dev pages could not be fetched, so exact current model IDs (e.g. `gemini-3-pro-image-preview`, the 2.1 model ID) and the app's official resolution table are not confirmed here.
- Official confirmation of the 2.1 release details from Google's own blog was not retrieved; only third-party sources were.

---

## Part 1, Q6: Example prompts for landscape, exterior, interior and virtual staging from credible sources

### Takeaway
Credible official examples are limited to interior furniture swaps and generic edits. Garden and exterior examples come from third-party blogs. The consistent pattern is "Using this photo, [change X] … Keep everything else exactly the same."

### Cited Findings
- Google official interior example (2.5 Flash Image guide, 2025-08, older than 6 months, search summary): change only the blue sofa to a vintage brown leather chesterfield, and keep the rest of the room, including pillows and lighting, unchanged. — [Google Developers Blog](https://developers.googleblog.com/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- Google official armchair-in-living-room multimodal example, quoted verbatim in Q1. — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- Third-party backyard removal: "Using the provided photo of this backyard, remove the garden shed and the hose on the lawn. Keep everything else exactly the same." — [Lilach Bullock](https://www.lilachbullock.com/nano-banana-prompts-copy-paste-gemini-image-edits/)
- Third-party garden path: "On this uploaded photo, change the concrete path to warm-toned clay pavers in a herringbone pattern. Keep existing plants." — [Eden LG](https://edenlg.co.ke/ai-garden-design-how-to-use-nano-banana-to-plan-and-visualize-your-dream-garden/)
- Other collections found but not read in full:
  - Landscape prompt collections. — [Meltflex AI, 40 landscape design prompts](https://www.meltflexai.com/blog/ai-landscape-design-prompts); [GlobalGPT, redesign indoor and outdoor spaces with Nano Banana](https://www.glbgpt.com/hub/how-to-redesign-indoor-and-outdoor-spaces-with-nano-banana/)
  - Architecture and exterior prompt collections. — [RenderAHouse](https://www.renderahouse.com/blog/nano-banana-architecture-prompts); [RunDiffusion Nano Banana 2.1 guide for architecture](https://learn.rundiffusion.com/nano-banana-2-1-prompt-guide/)

### Inferences
Draft template for Claude to adapt per photo. It is synthesized from the guidance above and has not been tested.

> Using this photo of a residential back garden, redesign only the planted beds and lawn area in the foreground and middle ground as a [style, e.g. relaxed English cottage garden]. Replace the patchy lawn with [specific material/plants]. Plant [3–6 named species suited to region/zone, with heights and colors], arranged in drifts with taller plants at the back against the fence. Add [hardscape, e.g. a curved path of reclaimed brick].
> The following must stay exactly as they are in the original photo, unchanged in shape, color, texture and position: the [describe house], the [describe wall/fence], the [describe mature tree(s)], the sky, and all neighboring buildings. Keep the identical camera position, lens, framing, perspective and [aspect ratio]. Match the original lighting: [time of day, light direction, overcast/sunny], with shadows falling the same way.
> The result should look like an unretouched real photograph of the same garden about two years after planting, with plants at realistic sizes. It should not look like a 3D render or illustration.

- Use one prompt per photo, reuse the same design-brief paragraph for all photos, and keep follow-ups to single, small changes.

### Gaps
- I found no Google-published exterior or landscape example. I found no before/after evaluation of garden prompts from a credible independent source.

---

## Part 2, Q1: Which AI garden and landscape design apps exist, and how do they work?

### Takeaway
The market splits three ways:
1. Photo-to-AI-render apps: upload a photo, pick a style preset, get a generated redesign. Examples: Home Designs AI, ReimagineHome, DecorAI, Gardenly, many "AI Garden Design" App Store apps.
2. Manual or AR design tools with plant libraries: iScape, Planner 5D, PRO Landscape+.
3. Human design services: Yardzen.

Only a few AI apps name real species with climate awareness.

### Cited Findings
- **iScape** is not an AI generation tool. Users build designs element by element in AR. Reviewers cite crashes in AR mode and a high price; its reliability score is 3.0/5 across 13 years of reviews. — [AI Tools Bakery: iScape review 2026](https://aitoolsbakery.com/blog/iscape-review/)
- **Planner 5D** uses generic 3D plant models with no species data, no USDA zone data and no AI photo-based design. Its 2.7/5 Trustpilot rating is driven mainly by subscription and billing complaints. — [AI Tools Bakery: Planner 5D review 2026](https://aitoolsbakery.com/blog/planner-5d-review/)
- **Yardzen** is primarily a human-designer service. Customers send photos and a questionnaire and get back 2D and 3D renders plus plant and material lists, with species chosen for climate and mature size. Pricing reports conflict: from $295, or $995 to $3,495. A claimed "YardAI" free tier could not be verified. — [Sow: Yardzen review 2026](https://www.usesow.com/app/compare/yardzen-review); [OutdoorBrite](https://www.outdoorbrite.com/blog/best-ai-landscape-design-tools)
- **Gardenly** is positioned (by its own blog) as a photo-to-design workflow with climate-adapted plants. Sow's competitor comparison lists it among apps that name real plant species. — [Gardenly blog](https://gardenly.app/blog/garden-design-apps-ranked); [Sow comparison](https://www.usesow.com/app/compare/best-ai-landscape-design-apps)
- **Home Designs AI** is noted for speed and many style options; DecorAI's table credits it with 12 landscape styles and a 7.0 score. — [DreamYard](https://dreamyard.ai/blog/best-ai-landscape-design); [DecorAI](https://decorai.io/blog/best-ai-landscape-design-apps/)
- **ReimagineHome** is a broader home AI suite covering interior redesign, staging, exterior and landscaping transformations. — [Toolworthy](https://www.toolworthy.ai/blog/best-ai-landscape-design-tools)
- **Other features in this segment:**
  - Remodel AI offers 10 garden styles.
  - Luw.ai is described as having advanced masking and editing.
  - PRO Landscape+ (2026 release) added an AI Eraser that strips existing landscaping from photos, and an AI Cutout tool for adding new plants with automatic background removal.
  — [search summary across vendor blogs](https://www.toolworthy.ai/blog/best-ai-landscape-design-tools); [Remodel AI](https://www.remodelai.io/blog/best-ai-landscape-design-apps)
- **Other App Store AI garden apps:** "Garden AI: Landscape Design", "AI Garden Design: Landscape AI", "AI Garden Planner: Landscapers", "AI Garden Design: Scenery AI" and "AI Garden Planner & Plant Care". — [App Store 1](https://apps.apple.com/us/app/garden-ai-landscape-design/id6738805390?see-all=reviews); [App Store 2](https://apps.apple.com/us/app/ai-garden-design-landscape-ai/id6744179402?see-all=reviews&platform=ipad); [App Store 3](https://apps.apple.com/us/app/ai-garden-planner-landscapers/id6747119850?see-all=reviews&platform=iphone); [App Store 4](https://apps.apple.com/us/app/-/id6757189248); [App Store 5](https://apps.apple.com/us/app/id6745493284)
- **Caveat on sources:** nearly all "best AI landscape app" rankings are vendor-authored and rank themselves first (DecorAI, Gardenly, Sow, DreamYard, Hadaa, Remodel AI, Landscapio, OutdoorBrite). — [DecorAI](https://decorai.io/blog/best-ai-landscape-design-apps/); [Hadaa](https://hadaa.app/blog/best-ai-landscape-design-apps); [Landscapio](https://www.landscapioai.com/blog/best-free-ai-landscape-design-tools); [Fast.io](https://fast.io/resources/best-ai-for-landscape-design-2026/)

### Inferences
- The typical AI app pipeline is: photo upload, optional brush mask, style preset (cottage, modern, Japanese, xeriscape, etc.), then a generated image. Few produce a usable plant list tied to the image.
- Which underlying image models these apps use is mostly undisclosed.

### Gaps
- I found no independent, real-yard comparative tests of masking quality or preset fidelity. Which apps use Gemini vs Flux or SDXL is undisclosed. Official feature pages for Home Designs AI, ReimagineHome and Gardenly were not fetched.

---

## Part 2, Q2: What do users praise and complain about?

### Takeaway
The main complaints about AI apps are that they alter the house or building, replace the real yard with generic imagery, suggest plants unsuited to the climate, and use aggressive paywalls and trial limits. Manual tools draw complaints about crashes, pricing and billing. Praise centers on speed and inspiration value.

### Cited Findings
- A reviewer says the app "can't keep your actual landscape in the design, instead replacing it with fake, generic images". The developer responded that it is meant as "creative design inspirations". — [App Store](https://apps.apple.com/us/app/garden-ai-landscape-design/id6738805390?see-all=reviews)
- Reviewers report tropical plants suggested for Northern Virginia, and that the app "change[s] the original house or office building you import". — [App Store](https://apps.apple.com/us/app/ai-garden-design-landscape-ai/id6744179402?see-all=reviews&platform=ipad)
- One user was "locked out because I did my limit of designs" after a short trial. — [App Store](https://apps.apple.com/us/app/ai-garden-planner-landscapers/id6747119850?see-all=reviews&platform=iphone)
- Planner 5D: billing and auto-renewal complaints. iScape: AR crashes and price. — [AI Tools Bakery Planner 5D](https://aitoolsbakery.com/blog/planner-5d-review/); [AI Tools Bakery iScape](https://aitoolsbakery.com/blog/iscape-review/)
- Home Designs AI is praised for speed and range of styles (vendor-adjacent source). — [DreamYard](https://dreamyard.ai/blog/best-ai-landscape-design)

### Inferences
The user's own goals of preserving fixed elements, realistic plants and climate fit are exactly the top complaint areas in commercial apps. Solving them gives a real advantage over off-the-shelf apps.

### Gaps
- The review sample is small. I found no Reddit (r/landscaping, r/GardeningUK) threads in searches, so practitioner sentiment from those communities is missing.

---

## Part 2, Q3: Which features are worth copying in a custom build?

### Takeaway
Worth copying:
- Style presets, expanded into a rich written design brief.
- A mask or brush to mark the redesign area.
- Before/after slider.
- A plant list with real, climate-appropriate species tied to the render.
- An eraser to clear existing planting.

Then go beyond the apps by compositing original pixels back over the fixed regions.

### Cited Findings
- Style presets are universal: 12 landscape styles in Home Designs AI and 10 garden styles in Remodel AI. — [DecorAI](https://decorai.io/blog/best-ai-landscape-design-apps/); [Remodel AI](https://www.remodelai.io/blog/best-ai-landscape-design-apps)
- Climate-adapted named plant lists are a differentiator, seen in Gardenly and Yardzen. Planner 5D's lack of species and zone data is called out as a weakness. — [Gardenly](https://gardenly.app/blog/garden-design-apps-ranked); [Sow Yardzen review](https://www.usesow.com/app/compare/yardzen-review); [AI Tools Bakery Planner 5D](https://aitoolsbakery.com/blog/planner-5d-review/)
- Masking and editing tools (Luw.ai), an AI Eraser for existing landscaping, and AI Cutout for adding specific plants (PRO Landscape+). — [Toolworthy](https://www.toolworthy.ai/blog/best-ai-landscape-design-tools)
- Annotation-driven editing (draw on image) in the Gemini app, Krea and Photoshop. — [Tom's Guide](https://www.tomsguide.com/ai/ai-image-video/nano-banana-now-lets-you-draw-prompts-directly-on-your-photos-sam-altman-is-going-to-hate-this); [Krea](https://www.krea.ai/apps/edit/nano-banana-edit); [Adobe](https://www.adobe.com/ca/learn/photoshop/web/nano-banana-generative-edits)
- Human-service deliverables (Yardzen) include 2D plans, 3D renders and plant and material lists. — [Sow Yardzen review](https://www.usesow.com/app/compare/yardzen-review)

### Inferences
A minimal custom pipeline for a weekend project:
1. User uploads a photo and states location or climate.
2. Claude writes a garden design brief with a style preset plus named, climate-appropriate plants with mature sizes.
3. Optional: the user draws on a copy of the photo (colored outline of beds to redesign) or a brush mask.
4. Claude composes a Gemini prompt containing the operation verb, the redesign spec, a concrete keep-list, camera and lighting matching, and a realism clause.
5. Call the API with Nano Banana Pro or 2.1 at 2K or 4K, with the aspect ratio matching the source.
6. Composite the original pixels back over the fixed regions using the mask.
7. Show a before/after slider plus the plant list.
8. For other photos of the same garden, reuse the brief and attach the approved render as a style reference.

### Gaps
- Feasibility and quality of the post-composite approach with Gemini outputs is untested in sources. Gemini may subtly shift geometry, which would cause seams at mask edges, so feathering would be needed.
