# Ring bridge: talk to Claude Code from your phone (and later your ring)

A personal relay. You speak on your Android phone, check the text, tap send, and a Claude Code
cloud session starts working on your repo. It opens a draft pull request when it is done.
Later, the same relay accepts messages from a ring (for example the Pebble Index 01).

```
Phone page (Chrome, hold to talk)  ─┐
                                    ├─>  this relay (Cloudflare Worker)  ─>  Claude Code scheduled task  ─>  draft PR
Ring webhook (later)               ─┘        keeps the token secret              (your claude.ai plan)
```

**What it costs:** Cloudflare Workers' free plan covers personal use. Claude runs count against
your claude.ai plan (Pro, Max, Ultra, Team or Enterprise). Speech-to-text runs in Chrome on the phone.

**Limits to know:** scheduled-task API triggers are a research preview, so the endpoint can change.
Each task can be fired 30 times per hour.

## Files

| File | What it is |
|---|---|
| `worker.js` | The relay and the phone page |
| `routine_prompt.md` | The instructions to paste into your scheduled task |
| `wrangler.toml` | Cloudflare settings (only the task id goes here, never the token) |
| `test/worker.test.mjs` | Tests: `npm test` |

## Setup (about 20 minutes, needs a computer once)

### 1. Create the scheduled task (on the web)

API triggers can only be added on the web, not in the CLI. On a computer, open
`claude.ai/code/routines`:

1. Click **New task** (choose **Set up manually** if asked).
2. Give it a name, for example `Voice requests`.
3. Paste the prompt from `routine_prompt.md`, with your repo and branch filled in.
4. Under **Advanced settings → Repository**, pick the repo, then pick a **Cloud environment**.
5. In the **Trigger** row, choose **API**, then click **Create**.
6. **Copy the token now.** It is shown only once. Also copy the **Fire URL**. The part that
   starts with `trig_` is your task id.

### 2. Protect your main branch (on GitHub)

In the repo, go to **Settings → Rules → Rulesets** and add a rule that blocks direct pushes to
`main` (and to your working branch if you want). Make sure **you** are not on the bypass list.
Claude's commits use your GitHub identity, so a rule you can bypass will not stop it.

### 3. Deploy the relay (Cloudflare, free)

You need Node.js on the computer and a free Cloudflare account.

```bash
cd ideas/ring-bridge
```

Put your task id (the `trig_...` part) in `wrangler.toml`, in place of `trig_REPLACE_ME`. Then:

```bash
npx wrangler login
```

```bash
npx wrangler secret put ROUTINE_TOKEN
```

(paste the token from step 1 when asked)

```bash
npx wrangler secret put APP_PASSCODE
```

(choose a passcode; you will type it once on your phone)

```bash
npx wrangler deploy
```

It prints your relay address, something like `https://ring-bridge.<your-name>.workers.dev`.

### 4. Put it on your phone

1. Open the relay address in **Chrome** on your Android phone.
2. Type the passcode and allow the microphone when asked.
3. Chrome menu (⋮) → **Add to Home screen**. It now opens like an app.

Use it: hold the big button and speak, release, fix any wrong words, tap **Send to Claude**,
and confirm. The page shows a link to the Claude session. It also appears in the Claude app's
**Code** tab, where you can watch it or reply.

## Adding the ring later (Pebble Index 01 or similar)

1. Make a long random secret and save it:

   ```bash
   npx wrangler secret put RING_SECRET
   ```

2. In the ring's app, set the webhook to `https://<your relay>/ring/<RING_SECRET>`.
3. Watch the first real message arrive, to see the exact format the ring sends:

   ```bash
   npx wrangler tail
   ```

   The relay looks for a transcript in the usual field names (`transcript`, `text`,
   `transcription`, ...). If it can't find one, it answers 422 and logs the payload, and
   `extractRingText` in `worker.js` gets adjusted to match.

**Important:** ring messages go straight to Claude, with no confirmation screen. The safety
nets are the hold-to-talk button, the task prompt (draft PRs only, never `main`) and your
GitHub ruleset. If you'd rather approve each ring message on the phone first, that's the next
thing to add.

## Security notes

- The scheduled-task token lives only in Cloudflare secrets. The phone never sees it.
- The token can only start this one task. Regenerate it on the task's page if it ever leaks.
- Text you send is labelled untrusted by Claude Code. The saved prompt decides what Claude may do with it.
- This is for **your own use**. Anthropic's terms do not allow an app that runs other people's
  requests through their claude.ai subscriptions; a product for others would need API keys.
