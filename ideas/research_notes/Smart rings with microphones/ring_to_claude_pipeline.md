# Ring → Phone → Speech-to-Text → Claude → GitHub: Pipeline Architecture (as of November 2026)

Scope note: research done 2026-11-21. Anthropic documentation was fetched directly (code.claude.com, platform.claude.com). Third-party pricing and wearable claims mostly come from secondary sources and are flagged as such.

## Q1. Anthropic options: which official surfaces can a third-party (ring/phone) app use to make Claude act on a specific GitHub repo + branch, and what are the auth constraints?

### Takeaway
There are now two documented, programmatic ways for your own app to start a Claude coding agent on a given repo/branch: (a) **Claude Code cloud "scheduled tasks" (formerly routines) with an API trigger**, an HTTP `POST .../fire` that uses a per-task bearer token, starts a cloud session and returns its URL (claude.ai subscription, research preview); and (b) the **Claude Managed Agents Sessions API** (`POST /v1/sessions`, Console API key), which mounts a `github_repository` resource and accepts an explicit `checkout: {type: "branch", name: ...}`. The CLI can also queue follow-up messages into an existing cloud session (`claude -p "..." --cloud <session-id>`). Remote Control and teleport only work with claude.ai subscription login and do not accept API keys. Anthropic forbids third-party apps from offering claude.ai login or routing requests through consumer-plan credentials on users' behalf; products must use API keys.

### Cited Findings

**Claude Code cloud sessions (Claude Code on the web)**
- Cloud sessions are available on Pro, Max, Ultra and Team plans, and to Enterprise users with premium or Chat + Claude Code seats. They run on Anthropic-managed VMs (or a self-hosted environment) and count toward plan usage limits, with "no separate charge for the cloud VM". — [Claude Code docs: Use Claude Code in the cloud](https://code.claude.com/docs/en/claude-code-on-the-web)
- You can start a cloud session from the browser (claude.ai/code), the **Code tab in the Claude mobile app**, the Desktop app, the terminal (`claude --cloud "task"`) or cloud scheduled tasks. — [same](https://code.claude.com/docs/en/claude-code-on-the-web)
- `claude --cloud` clones "your current directory's GitHub remote at your current branch". So branch selection from the CLI follows whatever branch is checked out and pushed. `--remote` is a deprecated alias. — [same](https://code.claude.com/docs/en/claude-code-on-the-web)
- **Follow-ups from any machine:** `claude -p "your message" --cloud <session-id>` "queues the message into the session and exits without waiting for a reply". `--output-format json` returns `{ok, session_id, url}`. It needs a claude.ai login (`claude auth login`) and does not work with Bedrock, Vertex or other third-party providers. — [same](https://code.claude.com/docs/en/claude-code-on-the-web)
- GitHub access works through either the Claude GitHub App or `/web-setup`, which sends your local `gh` token to your Claude account. In Anthropic-hosted environments "your GitHub credentials stay encrypted on Anthropic's servers and never enter a session's VM", and a GitHub proxy attaches credentials server-side. — [same](https://code.claude.com/docs/en/claude-code-on-the-web)
- `--teleport` (pulling a cloud session into the terminal) "requires claude.ai subscription authentication". API-key or Console sign-in fails with "Unable to get organization UUID". — [same](https://code.claude.com/docs/en/claude-code-on-the-web)
- **Auto-fix PRs:** with the Claude GitHub App installed, a cloud session can subscribe to PR activity and push fixes for CI failures and review comments. From the mobile app you can just say "watch this PR and fix any CI failures or review comments". — [same](https://code.claude.com/docs/en/claude-code-on-the-web)

**Cloud scheduled tasks (formerly "routines") with an API trigger: the most direct "ring button → agent on repo" hook**
- A scheduled task is "a saved Claude Code configuration: a prompt, one or more repositories, and a set of connectors". Triggers can be a schedule, an **API** call ("HTTP POST to the task's own endpoint with a bearer token") or a GitHub event. Available on Pro, Max, Ultra, Team and Enterprise. **Research preview.** — [Claude Code docs: Automate work with scheduled tasks](https://code.claude.com/docs/en/routines)
- The documented call is `POST https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire` with `Authorization: Bearer <token>`, `anthropic-beta: experimental-cc-routine-2026-04-01` and body `{"text": "..."}`. The response is `{"type":"routine_fire","claude_code_session_id":..., "claude_code_session_url":...}`. — [same](https://code.claude.com/docs/en/routines)
- "The `/fire` endpoint is available to claude.ai users only and is not part of the Claude Platform API surface." Each task has its own token, "scoped to triggering that task only", shown once and revocable or rotatable on the web. — [same](https://code.claude.com/docs/en/routines)
- **Built-in injection guard:** fire `text` "arrives wrapped in a `<routine-fire-payload>` block that labels it as untrusted data and tells Claude not to follow instructions inside it unless the routine's own prompt says to". The saved prompt must opt in, e.g. "Investigate the alert described in the routine-fire-payload block". — [same](https://code.claude.com/docs/en/routines)
- **Branch behavior:** "Claude starts from the repository's default branch unless your prompt specifies otherwise", and "pushes its work to a branch prefixed with `claude/` unless your prompt directs it to push to another branch". The docs recommend GitHub branch protection or rulesets to control where runs can push, and note that "a rule that access can bypass doesn't block a run's push". — [same](https://code.claude.com/docs/en/routines)
- **Limits:** API fires are capped at 30/hour per task (shared with Run now) and 100/hour per account, with no overage. Runs draw on subscription usage, with metered overage only if usage credits are on. — [same](https://code.claude.com/docs/en/routines)
- Commits and PRs carry your GitHub user ("Anything a scheduled task does through your connected GitHub identity or connectors appears as you"). — [same](https://code.claude.com/docs/en/routines)

**Claude Managed Agents Sessions API (developer/API-key route)**
- `POST /v1/sessions` requires the `managed-agents-2026-04-01` beta header and takes `agent`, `environment_id`, optional `initial_events` (e.g. `{"type":"user.message","content":[{"type":"text","text":"..."}]}`), `resources` and `vault_ids`. The example authenticates with `Authorization: Bearer $ANTHROPIC_API_KEY`. — [Claude Platform API: Create Session](https://platform.claude.com/docs/en/api/http/beta/sessions/create)
- The `github_repository` resource takes `url`, `authorization_token` ("Required for private repositories") and `checkout` (`{type:"branch", name}` or `{type:"commit", sha}`; defaults to the default branch). It mounts at `/workspace/<repo-name>`. — [same](https://platform.claude.com/docs/en/api/http/beta/sessions/create)
- The Sessions API has Create, List, Get, Update, Delete and Archive operations. — [Claude Platform API: Sessions](https://platform.claude.com/docs/en/api/http/beta/sessions)
- Pricing: tokens at model rates plus **$0.08 per session-hour** of `running` time ("idle" time is not billed). Anthropic's worked example is a 1-hour Opus 5.5 session with 50k input and 15k output tokens costing $0.58, or $0.428 with caching. — [Claude pricing docs](https://platform.claude.com/docs/en/about-claude/pricing)

**Remote Control (steering a local session from the phone)**
- Remote Control connects claude.ai/code or the Claude iOS/Android app to a Claude Code session running on your own machine. Code execution stays local. — [Claude Code docs: Remote Control](https://code.claude.com/docs/en/remote-control)
- It is available on Pro, Max, Ultra, Team and Enterprise. "**API keys are not supported.**" With `ANTHROPIC_API_KEY` set, you get the error "Remote Control requires claude.ai subscription auth." — [same](https://code.claude.com/docs/en/remote-control)
- The local session "makes outbound HTTPS requests only and never opens inbound ports". There is an optional "Trusted Devices" requirement, and Claude can send push notifications to the phone. — [same](https://code.claude.com/docs/en/remote-control)

**Claude Code GitHub Action (`@claude`)**
- The action is `anthropics/claude-code-action@v1`. In interactive mode it responds to `@claude` in issue and PR comments, PR reviews, or new issue titles and bodies, and can "implement changes, and push commits" and "turn issues into pull requests". — [Claude Code docs: GitHub Actions](https://code.claude.com/docs/en/github-actions)
- Auth options: `ANTHROPIC_API_KEY` (Console), `CLAUDE_CODE_OAUTH_TOKEN` (subscription token from `claude setup-token`; Pro, Max, Ultra, Team, Enterprise), OIDC workload identity federation, or Bedrock, Vertex or Foundry. — [same](https://code.claude.com/docs/en/github-actions)
- On issue and PR events "the triggering user must have write access to the repository", and bot actors are rejected unless they are listed in `allowed_bots`. — [same](https://code.claude.com/docs/en/github-actions)
- Costs: GitHub Actions minutes plus API tokens, or subscription usage if you use the OAuth token. — [same](https://code.claude.com/docs/en/github-actions)

**Claude API (Messages) and audio**
- The Messages API reference describes input as text and/or image content. I found no official audio content block, so STT must happen before Claude. — [Claude API: Create a Message](https://platform.claude.com/docs/api/messages/create); third-party course material says the same: "Claude API does not directly accept audio" — [TDS course notes](https://tds.s-anand.net/2026-02/docs/week-3/multimodal-inputs/)
- Current API prices per MTok (input/output): Opus 5.5 $4/$20, Sonnet 5.5 $2/$10, Sonnet 5 $2/$10, Haiku 5.5 $0.10/$0.50 (prompts ≤100k tokens). Cache hits cost 0.05x on Opus 5.5 and Sonnet 5.5. The Batch discount is 50%. — [Claude pricing docs](https://platform.claude.com/docs/en/about-claude/pricing)

**Claude mobile app / iOS integration**
- The Claude iOS app exposes an "**Ask Claude**" App Intent for Siri, Spotlight, Shortcuts and the Share sheet (iOS 18+). It uses the app's default model and counts toward usage limits. A widget has a mic button that "open[s] the app in dictation mode". — [Claude Help Center: App Intents, Shortcuts and Widgets on iOS](https://support.claude.com/en/articles/10263469-using-claude-app-intents-shortcuts-and-widgets-on-ios)

**Authentication / terms constraints**
- "OAuth authentication is intended exclusively for purchasers of Claude Free, Pro, Max, Ultra, Team, and Enterprise subscription plans and is designed to support ordinary use of Claude Code and other native Anthropic applications." — [Claude Code docs: Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)
- "Developers building products or services ... including those using the Agent SDK, should use API key authentication through Claude Console or a supported cloud provider. Anthropic does not permit third-party developers to offer Claude.ai login into their own applications, or to route requests through Free, Pro, Max, or Ultra plan credentials on behalf of their users ... developers may not collect, store, or intermediate Claude.ai credentials or session tokens." — [same](https://code.claude.com/docs/en/legal-and-compliance)
- Configuring your own API key "for use by the customer's own authorized users" is allowed if usage is billed to the key owner and isn't resold. — [same](https://code.claude.com/docs/en/legal-and-compliance)
- Feb 19, 2026: news coverage of Anthropic clarifying that consumer-plan OAuth tokens in third-party tools violate terms — [WinBuzzer](https://winbuzzer.com/2026/02/19/anthropic-bans-claude-subscription-oauth-in-third-party-apps-xcxwbn/); [Gigazine](https://gigazine.net/gsc_news/en/20260220-anthropic-third-party-block)
- **Conflicting or unverified:** VentureBeat reports that from mid-June 2026 subscribers get an "Agent SDK credit" that third-party Agent SDK apps (e.g. Conductor, OpenClaw) can draw on through local Claude Code credentials — [VentureBeat](https://venturebeat.com/ai/anthropic-reinstates-openclaw-and-third-party-agent-usage-on-claude-subscriptions-with-a-catch/). The current official legal page (fetched today) still contains the prohibition above, so treat the VentureBeat claim as unconfirmed by primary docs.

### Inferences
- **Best fit for a personal ring → Claude Code pipeline today:** create one cloud scheduled task per repo/branch target. Its saved prompt says "work on branch X, follow the instructions in the routine-fire-payload block, open a draft PR, never push to main". Generate the API token once and store it in the phone's Keychain or Keystore. The companion app transcribes and POSTs `{"text": transcript}` to `/fire`, then shows or pushes the returned `claude_code_session_url`, which opens in the Claude app's Code tab for review or steering. This is your own token for your own task, which matches the documented use ("internal tools"). It is not a third-party app intermediating claude.ai login. It is still research preview and capped at 30 fires/hour per task.
- **For a distributable product** (other users' rings), the compliant route is the Managed Agents Sessions API or the Agent SDK with each user's **own Console API key**. The app must not hold claude.ai credentials.
- For a multi-turn voice conversation with one session, the app (or a small server it calls) can run `claude -p "..." --cloud <session-id>`, which needs a claude.ai CLI login on a server you control. With Managed Agents you post events to the session instead.
- Remote Control isn't suitable as a third-party integration point (claude.ai auth only, no API). It's a human-in-the-loop phone UI.

### Gaps
- I didn't fetch the Managed Agents "send event to session" endpoint page or its streaming details, so check the exact event schema.
- I didn't confirm whether Claude mobile **voice mode** can create or steer Claude Code (Code tab) sessions by voice. Only dictation in the widget is documented in the sources found.
- No official doc found for a public API to create a claude.ai/code session ad hoc (outside routines) with arbitrary repo and branch. An unofficial source mirror suggests the CLI uses `/v1/sessions` internally ([tangled.org mirror](https://tangled.org/oppi.li/claude-code/raw/main/bridge/createSession.ts)), but that's unsupported.
- The scheduled-tasks API surface may change (beta header `experimental-cc-routine-2026-04-01`).

## Q2. Alternative routes (GitHub issue → Action, GitHub API + Claude tools, Shortcuts/Android intents, Siri/Gemini)

### Takeaway
The most robust "no Anthropic beta" route is to have the phone create a GitHub issue or comment containing `@claude <transcript>` through the GitHub REST API. The Claude Code GitHub Action then runs on a GitHub runner and opens a PR. On iOS, the Claude app's "Ask Claude" App Intent lets Shortcuts send text to Claude chat, but that is chat, not a Claude Code agent with repo access.

### Cited Findings
- `@claude` mentions in issue and PR comments trigger the Action. Claude "replies in a comment on the same issue or PR and updates it as it works", and can push commits and open PRs. — [Claude Code docs: GitHub Actions](https://code.claude.com/docs/en/github-actions)
- The commenting user must have write access, so a phone app posting with the owner's fine-grained PAT satisfies this. Bot actors are rejected unless allow-listed (`allowed_bots`). — [same](https://code.claude.com/docs/en/github-actions)
- Cloud scheduled tasks can also be triggered by GitHub events (PR opened, releases, etc.) with filters such as base and head branch or labels. Events are subject to "per-task and per-account hourly caps". — [Claude Code docs: scheduled tasks](https://code.claude.com/docs/en/routines)
- Siri "Ask Claude", Shortcuts action "Ask Claude" and Share-sheet chaining are documented for iOS 18+. — [Claude Help Center](https://support.claude.com/en/articles/10263469-using-claude-app-intents-shortcuts-and-widgets-on-ios)
- Pebble Index 01: the button is programmable, and Pebble plans optional click-and-hold routing to "general voice agents". One outlet mentions MCP support for developers. — [Linuxiac](https://linuxiac.com/?p=203221); [The Gadgeteer](https://the-gadgeteer.com/?p=492252)

### Inferences
- A "GitHub API + Claude Messages API with tools" DIY agent is feasible: GitHub contents and PR endpoints exposed as tools, or the official GitHub MCP server. But it reimplements what Claude Code, the Action and Managed Agents already do (cloning, tests, iterative edits). Using one of those is lower risk.
- A practical iOS bridge: ring app (or ring button → Shortcut) → transcription → Shortcuts "Get Contents of URL" POST to the routine `/fire` endpoint or GitHub Issues API. This avoids building a custom backend. I didn't verify that any specific ring app exposes a Shortcuts action.
- Siri or Gemini as the front end adds a second LLM hop and gives no repo access. Useful only as a dictation surface.

### Gaps
- I didn't research Android intent support in the Claude Android app (no source found).
- I didn't research Gemini or Google Assistant extension routes.

## Q3. Speech-to-text choices: on-device vs cloud, latency, cost

### Takeaway
On-device STT is free and fast enough for short ring memos. Apple SpeechAnalyzer (iOS 26+) and WhisperKit or whisper.cpp both reach roughly sub-second post-speech latency on recent hardware. Cloud STT costs roughly $0.0025–0.008 per minute: AssemblyAI Universal-2 is cheapest and Deepgram Nova-3 the most variable. For a few minutes of commands per day, STT cost is negligible either way.

### Cited Findings
- OpenAI gpt-4o-transcribe costs about $0.006/min and gpt-4o-mini-transcribe about $0.003/min. A newer "gpt-transcribe" is listed at $0.0045/min. — secondary: [DigitalApplied (Aug 2026)](https://www.digitalapplied.com/blog/openai-gpt-transcribe-stt-model-comparison-2026); [PerkStack tracker](https://perkstack.co/blog/cheapest-gpt-4o-transcribe-api)
- AssemblyAI Universal-2 costs about $0.15/hr ($0.0025/min), and Universal-3 Pro about $0.0035/min. — secondary: [AssemblyAI blog](https://assemblyai.com/blog/speech-to-text-api-pricing); [awesomeagents pricing](https://awesomeagents.ai/pricing/transcription-api-pricing/)
- Deepgram Nova-3: figures conflict. One source gives $0.0043/min for batch, a July 2026 tracker gives $0.0077/min, and streaming is about $0.46/hr. — [Deepgram blog](https://deepgram.com/blog/speech-to-text-api-pricing-breakdown-2025); contradicted by [PerkStack tracker](https://perkstack.co/blog/cheapest-gpt-4o-transcribe-api)
- Argmax's benchmark (vendor of WhisperKit) gives Apple SpeechTranscriber 14.0 error rate at speed factor 70, WhisperKit whisper-base.en 15.2 at 111, and whisper-small.en 12.8 at 35. Apple supports about 10 languages versus 100 for WhisperKit. — [Argmax](https://www.argmaxinc.com/blog/apple-and-argmax)
- In an independent-leaning Mac benchmark, Apple SpeechAnalyzer had 1.98% WER and a median post-speech latency of about 125–132 ms. whisper.cpp small.en had 4.28% WER and about 122–125 ms. — [DEV: Apple SpeechAnalyzer vs whisper.cpp](https://dev.to/iravoice/apple-speechanalyzer-vs-whispercpp-a-40-speaker-mac-benchmark-40i4)
- The WhisperKit paper reports 0.46 s latency and 2.2% WER (M3 Max). — [arXiv 2507.10860](https://arxiv.org/abs/2507.10860)
- Developers complain about SpeechTranscriber finalization latency. — [Apple Developer Forums](https://developer.apple.com/forums/thread/794720)
- Pebble Index 01 runs STT and an LLM locally in its open-source phone app. — [TechCrunch](https://techcrunch.com/2025/12/09/pebbles-founder-introduces-a-75-ai-smart-ring-for-recording-brief-notes-with-a-press-of-a-button)

### Inferences
- For Spanish or English mixed commands with code identifiers (file names, function names), a cloud model (gpt-4o-transcribe-class) or Whisper small/medium with a custom vocabulary or prompt will likely beat Apple's built-in model on technical vocabulary. Not benchmarked here.
- A pragmatic design: transcribe on-device first (privacy, offline), and optionally re-transcribe in the cloud only for commands that will trigger code changes.

### Gaps
- No primary vendor pricing pages fetched for Deepgram or AssemblyAI. Numbers are from trackers and may be stale.
- No reliable benchmark for SpeechAnalyzer on iPhone (vs Mac), or for Spanish accuracy.

## Q4. Existing projects: wearable → LLM → actions

### Takeaway
Several wearable-to-agent projects exist. Nexting (open source, MIT, supports Claude Code; ring in private beta), Natura Interface (ring that sends voice requests to agents including Claude Code), Omi (developer webhooks for real-time transcripts) and Pebble Index 01 (open-source app, programmable button) are the closest to "ring → Claude Code". Several GitHub projects do voice → Claude Code from a watch, glasses or desktop.

### Cited Findings
- **Nexting**: a "wearable agent dispatcher" for your own agents, supporting Claude Code, Codex and OpenClaw. MIT licensed. PIN available at $129, Ring in private beta. — [GitHub wiki](https://github.com/Nexting-ai/nexting/wiki); [Product Hunt](https://www.producthunt.com/products/nexting-2)
- **Natura Interface**: a smart ring where you press, speak and release to send a request to your agent. Listed agents include Claude Code. No open-source repo found. — [GamesBeat](https://gamesbeat.com/natura-launches-interface-a-smart-ring-for-voice-requests-that-connect-to-your-personal-ai-agents/)
- **Omi**: Developer Mode exposes a "Real-Time Transcript Webhook" (segments POSTed during live sessions) and a "Realtime audio bytes" webhook. Store-and-forward uploads don't replay through the real-time webhook. One older page labels it "not stable". — [Omi docs: Integrations](https://docs.omi.me/doc/developer/apps/Integrations); [Omi docs: Audio streaming](https://docs.omi.me/doc/developer/apps/AudioStreaming)
- Omi also integrates with n8n, Zapier and Make. — [Omi blog](https://www.omi.me/blogs/integrations/omi-automation-n8n-zapier-make)
- **Pebble Index 01**: $75 preorder, then $99. Button plus mic, stores about 5 min offline. The open-source app runs STT and LLM locally. Integrations include sending messages via Beeper and music control. Shipping was expected around March 2026 and was "behind schedule". — [Wallpaper](https://www.wallpaper.com/tech/pebble-index-ring-01); [Pebble blog](https://repebble.com/blog/how-i-use-my-index-01-production-update); [Tom's Guide](https://www.tomsguide.com/wellness/smart-rings/the-new-pebble-smart-ring-wont-track-your-health-doesnt-need-to-be-recharged-and-costs-just-usd75-heres-why-i-cant-wait-to-try-one)
- **Voice → Claude Code projects:** Handwave (Apple Watch → Claude Code sessions) — [zackproser.com](https://zackproser.com/blog/handwave); claude-code-g2 (AR glasses) — [GitHub](https://github.com/sam-siavoshian/claude-code-g2); voca (Claude Code voice plugin, Apple Silicon) — [GitHub](https://github.com/patelnav/voca); cctalk (macOS voice input for the CLI) — [GitHub](https://github.com/wisecorner/cctalk); voice-to-claude (Linux) — [GitHub](https://github.com/Eumaios1212/voice-to-claude); claude-code-voice (talk to Claude about projects over the phone) — [PyPI](https://pypi.org/project/claude-code-voice/)

### Inferences
- Omi's real-time webhook plus a tiny server that detects a wake phrase and calls the routine `/fire` endpoint is a low-effort prototype path. But Omi is always-listening, which raises the prompt-injection and privacy risk (see Q5).
- Pebble Index 01's push-to-talk button and open-source app are architecturally the cleanest fit: explicit intent per press, local STT, and an app you can modify to add an HTTP action.

### Gaps
- Didn't verify current shipping status of Pebble Index 01 or Nexting Ring as of Nov 2026.
- Didn't research Bee (Amazon), Limitless, Wispr Flow or SuperWhisper integrations specifically. No sources gathered.

## Q5. Security: confirmation, branch protection, prompt injection, tokens on the phone

### Takeaway
Anthropic's own surfaces include several useful guards: routine fire text is wrapped as untrusted data, GitHub credentials stay off the VM, the Action requires write-access humans, and runs default to `claude/` branches. The pipeline should still add a human confirmation step, use GitHub branch protection or rulesets (which bind to the connected identity), and keep scoped, revocable tokens in OS secure storage.

### Cited Findings
- Routine fire `text` is wrapped in `<routine-fire-payload>`, labeled untrusted, and must be explicitly referenced by the saved prompt. This protects against a leaked token sending direct instructions. — [Claude Code docs: scheduled tasks](https://code.claude.com/docs/en/routines)
- Routine tokens are per-task, shown once, and can be regenerated or deleted instantly. — [same](https://code.claude.com/docs/en/routines)
- Runs push to `claude/`-prefixed branches by default. Use "branch protection rules or rulesets on GitHub". Rules the connected access can bypass won't block pushes. — [same](https://code.claude.com/docs/en/routines)
- Cloud VMs: Network access is limited by default. Git credentials and signing keys stay outside the sandbox, and a proxy uses scoped credentials. — [Claude Code docs: cloud](https://code.claude.com/docs/en/claude-code-on-the-web)
- Auto-fix replies post under your GitHub username, which can trigger `issue_comment` automations (Atlantis, Terraform). Anthropic warns you to review such automation. — [same](https://code.claude.com/docs/en/claude-code-on-the-web)
- The GitHub Action requires write access for triggering users and rejects bots. The Claude GitHub App requests broad permissions (Contents, Workflows and Actions read/write, etc.). A custom app limited to Contents, Issues and PRs is possible for the Action only. — [Claude Code docs: GitHub Actions](https://code.claude.com/docs/en/github-actions)
- Remote Control offers "Trusted Devices", which requires a verified device and recent auth. — [Claude Code docs: Remote Control](https://code.claude.com/docs/en/remote-control)
- Omi's real-time webhook streams ambient conversation segments. — [Omi docs](https://docs.omi.me/doc/developer/apps/Integrations)

### Inferences
- **Confirmation step:** after transcription, show the transcript (watch or phone notification) and require a tap or second ring press before calling `/fire` or creating the issue. Have the agent open **draft PRs only**, so merge is always a human action on GitHub.
- **Prompt injection from ambient speech:** prefer push-to-talk rings (Pebble Index, Natura) over always-on recorders (Omi, Bee, Limitless). Never let ambient transcripts reach a code-executing agent without an explicit trigger plus confirmation. Rely on the routine wrapper, and put guardrails in the saved prompt ("only act on requests that start with ...; never modify CI/workflows or secrets").
- **Tokens on the phone:** store the routine token, GitHub fine-grained PAT (single repo, contents and issues only) or Console API key in iOS Keychain or Android Keystore. Prefer the routine token, which can only fire one task, over a Console API key, which can spend arbitrary money, or a broad PAT. Set Console spend limits if you use an API key.
- Protect `main` (require PR plus review), and optionally restrict the connected GitHub identity from bypassing rules.

### Gaps
- No Anthropic doc found specifically on voice or ambient-audio injection risk. These recommendations are inference.

## Q6. Rough cost per day for a heavy user (STT + Claude)

### Takeaway
STT is pennies per day. Claude agent runs dominate cost. On the API, a heavy user firing about 20 coding tasks/day would spend roughly $5–15/day depending on model (estimate). On a subscription route (routines, cloud sessions, Action with an OAuth token) the marginal cost is $0 until plan limits are hit.

### Cited Findings
- STT: about $0.0025–0.008/min in the cloud (see Q3 sources), or $0 on-device. — [awesomeagents pricing](https://awesomeagents.ai/pricing/transcription-api-pricing/); [PerkStack](https://perkstack.co/blog/cheapest-gpt-4o-transcribe-api)
- Prices per MTok: Sonnet 5.5 $2 in / $10 out / $0.10 cache hit; Opus 5.5 $4 / $20 / $0.20; Haiku 5.5 $0.10 / $0.50. Managed Agents runtime costs $0.08/session-hour. — [Claude pricing docs](https://platform.claude.com/docs/en/about-claude/pricing)
- Anthropic's example: a 1-hour Opus 5.5 coding session with 50k input and 15k output tokens costs $0.58, or $0.43 with caching. — [same](https://platform.claude.com/docs/en/about-claude/pricing)
- Cloud sessions and routines draw on subscription usage with no separate VM charge. — [cloud docs](https://code.claude.com/docs/en/claude-code-on-the-web); [routines docs](https://code.claude.com/docs/en/routines)
- GitHub Action runs also consume GitHub Actions minutes. — [GitHub Actions docs](https://code.claude.com/docs/en/github-actions)

### Inferences (estimates, my own arithmetic)
- **STT:** 40 commands × 20 s ≈ 13 min/day. At $0.006/min that is about $0.08/day; on-device it is $0.
- **Claude per coding task (API):** assume 200k input tokens (150k cached) plus 20k output.
  - Sonnet 5.5: 50k×$2 + 150k×$0.10 + 20k×$10 per M ≈ $0.10 + $0.015 + $0.20 ≈ **$0.32/task**.
  - Opus 5.5: $0.20 + $0.03 + $0.40 ≈ **$0.63/task**.
- **Daily totals:** 20 tasks/day is about $6.30/day (Sonnet 5.5) or $12.60/day (Opus 5.5). Add about $0.10–0.50/day of Managed Agents runtime if 1–6 running hours. A Haiku 5.5 "router" that classifies each transcript before firing adds well under $0.01/day.
- **Rough monthly API cost:** about $130–400 for a heavy user. A Max or Ultra subscription using the routine `/fire` route may be cheaper if usage stays within plan limits.

### Gaps
- Subscription plan prices and exact usage-limit sizes not fetched.
- Real token consumption per Claude Code task varies widely with repo size. The 200k/20k assumption is illustrative, not measured.
