// Ring bridge: voice -> Claude Code scheduled task (personal use).
//
// Runs as a Cloudflare Worker. It serves a small phone page (talk, review, send)
// and relays the confirmed text to your Claude Code scheduled task's API trigger.
// The scheduled-task token never leaves the server.
//
// Secrets (set with `wrangler secret put NAME`):
//   ROUTINE_TOKEN  the API-trigger token of your scheduled task
//   APP_PASSCODE   a passcode you type once on your phone
//   RING_SECRET    (optional) random string that forms the ring webhook URL
// Vars (wrangler.toml):
//   ROUTINE_ID     the scheduled task id (trig_...)

const FIRE_BASE = "https://api.anthropic.com/v1/claude_code/routines";
const ROUTINE_BETA = "experimental-cc-routine-2026-04-01";
const MAX_TEXT = 4000;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    try {
      if (request.method === "GET" && path === "/") return html(PAGE);
      if (request.method === "GET" && path === "/manifest.webmanifest") {
        return new Response(JSON.stringify(MANIFEST), {
          headers: { "content-type": "application/manifest+json" },
        });
      }
      if (request.method === "POST" && path === "/api/send") return handleSend(request, env);
      if (request.method === "POST" && path.startsWith("/ring/")) {
        return handleRing(request, env, path.slice("/ring/".length));
      }
      return json({ error: "not_found" }, 404);
    } catch (err) {
      console.log("unhandled error", err && err.stack ? err.stack : String(err));
      return json({ error: "internal_error" }, 500);
    }
  },
};

// Phone page -> confirmed text -> scheduled task.
async function handleSend(request, env) {
  if (!env.APP_PASSCODE || !safeEqual(request.headers.get("x-passcode") || "", env.APP_PASSCODE)) {
    return json({ error: "wrong_passcode" }, 401);
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "bad_json" }, 400);
  }
  const text = cleanText(body && body.text);
  if (!text) return json({ error: "empty_text" }, 400);
  if (text.length > MAX_TEXT) return json({ error: "text_too_long", max: MAX_TEXT }, 413);
  return fire(env, `[source: phone, confirmed by owner]\n${text}`);
}

// Ring webhook (e.g. Pebble Index 01) -> scheduled task.
// The URL itself is the secret: /ring/<RING_SECRET>.
async function handleRing(request, env, secret) {
  if (!env.RING_SECRET || !safeEqual(secret, env.RING_SECRET)) return json({ error: "not_found" }, 404);
  const raw = await request.text();
  // Log the payload so the first real ring message shows its exact format (`wrangler tail`).
  console.log("ring payload", raw.slice(0, 2000));
  const text = cleanText(extractRingText(raw));
  if (!text) return json({ error: "no_text_found" }, 422);
  if (text.length > MAX_TEXT) return json({ error: "text_too_long", max: MAX_TEXT }, 413);
  return fire(env, `[source: ring]\n${text}`);
}

// The ring's payload format is not documented yet; try the usual field names.
export function extractRingText(raw) {
  let data;
  try {
    data = JSON.parse(raw);
  } catch {
    return raw; // plain-text body
  }
  if (typeof data === "string") return data;
  const keys = ["transcript", "transcription", "text", "content", "message", "note"];
  const seen = new Set();
  const walk = (node, depth) => {
    if (!node || typeof node !== "object" || depth > 4 || seen.has(node)) return "";
    seen.add(node);
    for (const k of keys) {
      if (typeof node[k] === "string" && node[k].trim()) return node[k];
    }
    for (const v of Object.values(node)) {
      const found = walk(v, depth + 1);
      if (found) return found;
    }
    return "";
  };
  return walk(data, 0);
}

async function fire(env, text) {
  if (!env.ROUTINE_ID || !env.ROUTINE_TOKEN) return json({ error: "bridge_not_configured" }, 500);
  const res = await fetch(`${FIRE_BASE}/${encodeURIComponent(env.ROUTINE_ID)}/fire`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.ROUTINE_TOKEN}`,
      "anthropic-beta": ROUTINE_BETA,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  const payload = await res.text();
  if (!res.ok) {
    console.log("fire failed", res.status, payload.slice(0, 500));
    return json({ error: "claude_rejected", status: res.status, detail: payload.slice(0, 300) }, 502);
  }
  let data = {};
  try {
    data = JSON.parse(payload);
  } catch {
    /* keep empty */
  }
  return json({
    ok: true,
    sessionUrl: data.claude_code_session_url || null,
    sessionId: data.claude_code_session_id || null,
  });
}

export function cleanText(value) {
  if (typeof value !== "string") return "";
  return value.replace(/\u0000/g, "").trim();
}

// Constant-time string comparison.
export function safeEqual(a, b) {
  const enc = new TextEncoder();
  const x = enc.encode(String(a));
  const y = enc.encode(String(b));
  let diff = x.length ^ y.length;
  const n = Math.max(x.length, y.length);
  for (let i = 0; i < n; i++) diff |= (x[i] || 0) ^ (y[i] || 0);
  return diff === 0;
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}

function html(body) {
  return new Response(body, {
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "content-security-policy":
        "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'",
    },
  });
}

const MANIFEST = {
  name: "Ring to Claude",
  short_name: "Ring→Claude",
  start_url: "/",
  display: "standalone",
  background_color: "#111111",
  theme_color: "#111111",
};

const PAGE = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#111111">
<link rel="manifest" href="/manifest.webmanifest">
<title>Ring to Claude</title>
<style>
  :root { color-scheme: dark; font-family: system-ui, sans-serif; }
  body { margin: 0; background: #111; color: #eee; display: flex; flex-direction: column; min-height: 100vh; }
  main { flex: 1; display: flex; flex-direction: column; gap: 14px; padding: 18px; max-width: 560px; margin: 0 auto; width: 100%; box-sizing: border-box; }
  h1 { font-size: 1.1rem; margin: 0; font-weight: 600; }
  select, textarea, input, button { font: inherit; border-radius: 12px; border: 1px solid #333; background: #1c1c1c; color: #eee; }
  select, input { padding: 10px; }
  textarea { min-height: 140px; padding: 12px; resize: vertical; }
  #talk { height: 150px; font-size: 1.2rem; background: #2a2a2a; touch-action: none; user-select: none; -webkit-user-select: none; }
  #talk.on { background: #b3261e; border-color: #b3261e; }
  #send { padding: 16px; background: #c96442; border-color: #c96442; color: #fff; font-weight: 600; }
  #send:disabled { opacity: .4; }
  #status { min-height: 1.4em; color: #aaa; }
  #status a { color: #f0a07a; }
  .row { display: flex; gap: 10px; }
  .row > * { flex: 1; }
</style>
</head>
<body>
<main>
  <h1>Ring → Claude Code</h1>
  <div class="row">
    <select id="lang" aria-label="Language">
      <option value="es-419">Español</option>
      <option value="en-US">English</option>
    </select>
    <input id="pass" type="password" placeholder="Passcode" autocomplete="current-password" aria-label="Passcode">
  </div>
  <button id="talk" type="button">Hold to talk</button>
  <textarea id="text" placeholder="Your request appears here. You can edit it before sending."></textarea>
  <button id="send" type="button" disabled>Send to Claude</button>
  <div id="status" role="status"></div>
</main>
<script>
  const $ = (id) => document.getElementById(id);
  const talk = $("talk"), text = $("text"), send = $("send"), status = $("status"), lang = $("lang"), pass = $("pass");
  pass.value = localStorage.getItem("ringPass") || "";
  lang.value = localStorage.getItem("ringLang") || "es-419";
  lang.onchange = () => localStorage.setItem("ringLang", lang.value);

  const update = () => { send.disabled = !text.value.trim(); };
  text.oninput = update;

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  let rec = null, base = "", finalText = "";
  if (!SR) {
    talk.disabled = true;
    talk.textContent = "Speech recognition not available here. Type instead, or use Chrome.";
  }

  function start(e) {
    if (!SR || rec) return;
    e.preventDefault();
    base = text.value.trim() ? text.value.trim() + " " : "";
    finalText = "";
    rec = new SR();
    rec.lang = lang.value;
    rec.continuous = true;
    rec.interimResults = true;
    rec.onresult = (ev) => {
      let interim = "";
      for (let i = ev.resultIndex; i < ev.results.length; i++) {
        const r = ev.results[i];
        if (r.isFinal) finalText += r[0].transcript + " ";
        else interim += r[0].transcript;
      }
      text.value = (base + finalText + interim).trim();
      update();
    };
    rec.onerror = (ev) => { status.textContent = "Mic error: " + ev.error; };
    rec.onend = () => { rec = null; talk.classList.remove("on"); talk.textContent = "Hold to talk"; };
    rec.start();
    talk.classList.add("on");
    talk.textContent = "Listening… release to stop";
    if (navigator.vibrate) navigator.vibrate(30);
  }
  function stop() { if (rec) rec.stop(); }
  talk.addEventListener("pointerdown", start);
  talk.addEventListener("pointerup", stop);
  talk.addEventListener("pointercancel", stop);
  talk.addEventListener("pointerleave", stop);

  send.onclick = async () => {
    const body = text.value.trim();
    if (!body) return;
    if (!pass.value) { status.textContent = "Enter your passcode first."; pass.focus(); return; }
    if (!confirm("Send this to Claude?\\n\\n" + body)) return;
    send.disabled = true;
    status.textContent = "Sending…";
    try {
      const res = await fetch("/api/send", {
        method: "POST",
        headers: { "content-type": "application/json", "x-passcode": pass.value },
        body: JSON.stringify({ text: body }),
      });
      const data = await res.json().catch(() => ({}));
      if (res.status === 401) { status.textContent = "Wrong passcode."; localStorage.removeItem("ringPass"); return; }
      if (!res.ok) { status.textContent = "Not sent: " + (data.error || res.status) + (data.detail ? " — " + data.detail : ""); return; }
      localStorage.setItem("ringPass", pass.value);
      text.value = "";
      status.textContent = "";
      const msg = document.createTextNode("Sent. ");
      status.appendChild(msg);
      if (data.sessionUrl) {
        const a = document.createElement("a");
        a.href = data.sessionUrl;
        a.textContent = "Open the Claude session";
        a.target = "_blank";
        a.rel = "noopener";
        status.appendChild(a);
      }
      if (navigator.vibrate) navigator.vibrate([40, 60, 40]);
    } catch (err) {
      status.textContent = "Network error: " + err.message;
    } finally {
      update();
    }
  };
</script>
</body>
</html>`;
