// Run: node --test ideas/ring-bridge/test/
import { test, beforeEach } from "node:test";
import assert from "node:assert/strict";
import worker, { extractRingText, safeEqual } from "../worker.js";

const env = {
  ROUTINE_ID: "trig_test123",
  ROUTINE_TOKEN: "tok-secret",
  APP_PASSCODE: "1234",
  RING_SECRET: "ringsecret",
};

let calls;
beforeEach(() => {
  calls = [];
  globalThis.fetch = async (url, init) => {
    calls.push({ url, init });
    return new Response(
      JSON.stringify({
        type: "routine_fire",
        claude_code_session_id: "session_abc",
        claude_code_session_url: "https://claude.ai/code/session_abc",
      }),
      { status: 200, headers: { "content-type": "application/json" } },
    );
  };
});

const req = (path, init = {}) => new Request(`https://bridge.example${path}`, init);
const send = (text, pass = "1234") =>
  req("/api/send", {
    method: "POST",
    headers: { "content-type": "application/json", "x-passcode": pass },
    body: JSON.stringify({ text }),
  });

test("serves the phone page", async () => {
  const res = await worker.fetch(req("/"), env);
  assert.equal(res.status, 200);
  assert.match(await res.text(), /Hold to talk/);
});

test("rejects a wrong passcode without calling Claude", async () => {
  const res = await worker.fetch(send("hola", "0000"), env);
  assert.equal(res.status, 401);
  assert.equal(calls.length, 0);
});

test("rejects empty and oversized text", async () => {
  assert.equal((await worker.fetch(send("   "), env)).status, 400);
  assert.equal((await worker.fetch(send("x".repeat(4001)), env)).status, 413);
  assert.equal(calls.length, 0);
});

test("fires the scheduled task with token, beta header and text", async () => {
  const res = await worker.fetch(send("Add a README to the ideas folder"), env);
  assert.equal(res.status, 200);
  const data = await res.json();
  assert.equal(data.sessionUrl, "https://claude.ai/code/session_abc");
  assert.equal(calls.length, 1);
  const { url, init } = calls[0];
  assert.equal(url, "https://api.anthropic.com/v1/claude_code/routines/trig_test123/fire");
  assert.equal(init.headers.authorization, "Bearer tok-secret");
  assert.equal(init.headers["anthropic-beta"], "experimental-cc-routine-2026-04-01");
  assert.match(JSON.parse(init.body).text, /\[source: phone, confirmed by owner\]\nAdd a README/);
});

test("passes Claude errors back without leaking the token", async () => {
  globalThis.fetch = async () => new Response('{"error":"rate_limited"}', { status: 429 });
  const res = await worker.fetch(send("hola"), env);
  assert.equal(res.status, 502);
  const body = await res.text();
  assert.match(body, /429/);
  assert.doesNotMatch(body, /tok-secret/);
});

test("ring webhook needs the right secret", async () => {
  const bad = await worker.fetch(req("/ring/wrong", { method: "POST", body: "hi" }), env);
  assert.equal(bad.status, 404);
  const ok = await worker.fetch(
    req("/ring/ringsecret", { method: "POST", body: JSON.stringify({ data: { transcript: "Fix the typo" } }) }),
    env,
  );
  assert.equal(ok.status, 200);
  assert.match(JSON.parse(calls[0].init.body).text, /\[source: ring\]\nFix the typo/);
});

test("ring webhook is off when RING_SECRET is not set", async () => {
  const res = await worker.fetch(req("/ring/anything", { method: "POST", body: "hi" }), { ...env, RING_SECRET: "" });
  assert.equal(res.status, 404);
});

test("extractRingText handles plain text, flat and nested JSON", () => {
  assert.equal(extractRingText("plain words"), "plain words");
  assert.equal(extractRingText('{"text":"flat"}'), "flat");
  assert.equal(extractRingText('{"event":{"payload":{"transcription":"deep"}}}'), "deep");
  assert.equal(extractRingText('{"audio_url":"x"}'), "");
});

test("safeEqual", () => {
  assert.ok(safeEqual("abc", "abc"));
  assert.ok(!safeEqual("abc", "abd"));
  assert.ok(!safeEqual("abc", "abcd"));
});
