# Technical and Legal Constraints of Capturing Voice Audio from a Smart Ring (as of November 2026)

> Method note: this session's network blocked full-page fetches of outside sites (engadget.com and the-gadgeteer.com both failed to resolve). Every finding below comes from web-search result summaries and snippets, not from full-page reads. Treat the numbers as "reported by" the cited page, and re-check the important ones against the primary page before relying on them. Anything I calculated is labeled **[CALC]**. Anything I estimated without a source is labeled **[ESTIMATE]**.

## 1. Battery and power: capacities, current draw, minutes per charge, and how existing mic rings handle it

### Takeaway
Rechargeable smart rings carry roughly 15–25 mAh. Continuous mic + DSP/codec + BLE streaming probably draws a few mA. Continuous capture therefore lasts hours, not days, and always-on listening is the main threat to the battery. All three shipping or announced mic rings get around this by recording only on an explicit trigger: a button hold (Index 01), touch (Sandbar Stream), or a proximity sensor when the ring is raised to the mouth (Wizpr). Their claims cluster around 12–16 hours of total recording or "frequent use" per battery.

### Cited Findings
**Ring battery capacities**
- Samsung Galaxy Ring: 18–23.5 mAh depending on size, rated up to 7 days. Weighs 2.3–3 g; band cross-section about 7.0 mm × 2.6 mm. — [Wikipedia: Samsung Galaxy Ring](https://en.wikipedia.org/wiki/Samsung_Galaxy_Ring)
- Battery suppliers say most smart rings use ultra-small Li-polymer cells of about 15–25 mAh. Another source says 15–30 mAh. Both are vendor/blog figures, not manufacturer specifications. — [Ufine Battery: Smart Ring Battery Solutions](https://www.ufinebattery.com/applications/smart-ring-battery/); [LithoTop smart ring battery](https://lithotop.com/wearable-devices/smart-ring-battery/)
- I found no Oura capacity figure in this session (see Gaps).

**Component current draw**
- TDK T5838 PDM MEMS mic: 130 µA in always-on mode and 330 µA in high-performance mode. Its Acoustic Activity Detect (AAD) mode draws as little as about 20 µA. — [Syntiant press release on TDK T5838](https://www.syntiant.com/press-release/blog-post-title-three-mmhbm/); [audioXpress: TDK multi-mode mic with AAD](https://audioxpress.com/news/tdk-introduces-lowest-pulse-density-modulation-multi-mode-mems-microphone-with-acoustic-activity-detect)
- TDK T3902 PDM mic: 185 µA in ultra-low-power mode, 12 µA in sleep. — [audioXpress: TDK T3902](https://audioxpress.com/news/tdk-announces-t3902-lowest-power-pdm-mems-microphone); [Electronics-Lab](https://www.electronics-lab.com/tiny-mems-microphone-features-185%C2%B5a-ultra-low-power-mode/)
- ST MP23DB02MM digital MEMS mic: 2 µA sleep, 285 µA low-power, 800 µA normal mode (typical). — [ST datasheet MP23DB02MM](https://www.st.com/resource/en/datasheet/mp23db02mm.pdf)
- Nordic nRF54L15 BLE SoC radio: 4.8 mA TX at 0 dBm and 3.4 mA RX, at 3 V (product page). The preliminary datasheet v0.8 gives 5.0 mA TX at 0 dBm (1 Mbps) and 3.2 mA RX. Supports BLE at 2 Mbps, 1 Mbps, 500 kbps and 125 kbps. — [Nordic nRF54L15 product page](https://www.nordicsemi.com/Products/nRF54L15); [nRF54L15 datasheet v0.8 (Mouser)](https://www.mouser.com/datasheet/2/297/nRF54L15_nRF54L10_nRF54L05_Datasheet_v0_8-3568773.pdf)

**Existing mic rings**
- **Pebble Index 01 (Core Devices):**
  - Announced Dec 9, 2025, at $75 preorder ($99 after launch).
  - Stainless steel ring with a button, an RGB LED, a short-range mic, Bluetooth, and a **non-rechargeable silver-oxide battery**.
  - Records **only while the button is pressed and held**.
  - Stores up to about 5 minutes of audio on the ring when the phone is out of range.
  - Sources: [TechCrunch](https://techcrunch.com/2025/12/09/pebbles-founder-introduces-a-75-ai-smart-ring-for-recording-brief-notes-with-a-press-of-a-button); [MacRumors](https://www.macrumors.com/2025/12/09/pebble-index-01-smart-ring/); [Hackster](https://www.hackster.io/news/core-devices-unveils-the-pebble-index-01-a-disposable-smart-ring-microphone-c103c26e4f24)
- Index 01 battery life:
  - Reported as roughly 12–14 hours of total recording in some coverage and up to about 15 hours in others. Pebble frames this as "years" of average use, and one review says about two years.
  - When the battery is spent, the ring goes back to Pebble for recycling.
  - Sources: [Tom's Guide](https://www.tomsguide.com/wellness/smart-rings/the-new-pebble-smart-ring-wont-track-your-health-doesnt-need-to-be-recharged-and-costs-just-usd75-heres-why-i-cant-wait-to-try-one); [Lord of the Smart Rings review](https://www.lordofthesmartrings.com/pebble-index-01-review/); [Pebble Index 01 page](https://repebble.com/index?amp=&amp=); [Wareable](https://www.wareable.com/wearable-tech/pebble-index-1-smart-ring-announcement-price-release-date-features-explained)
- Index 01 cell identity:
  - Reviewers call it a hearing-aid-type cell.
  - A Hacker News commenter guessed SR721W from Pebble's sizing models. This is speculation, not a spec.
  - No mAh figure has been published.
  - Sources: [Hacker News thread](https://news.ycombinator.com/item?id=46205661); [Legend Memory blog](https://legendmemory.ai/blogs/the-archive/pebble-index-01-the-ring-that-catches-your-thoughts)
- Pebble posted that Index 01 is in mass production. — [Pebble blog: Index 01 Is In Mass Production](https://repebble.com/blog/index-01-is-in-mass-production)
- **Sandbar Stream:**
  - Rechargeable ring with an aluminum outer surface, a resin inner surface, and a glass touchpad. Touch-to-record, not always-on.
  - Sandbar's site says the battery is "all-day" and claims 16+ hours of frequent use. A universal-size charger is included; one review says it charges over USB-C.
  - Sources: [Sandbar Stream official page](https://www.sandbar.com/stream?pubDate=20251106); [Sandbar shop](https://shop.sandbar.com/)
- Sandbar Stream price and availability:
  - Launch preorder prices were $249 (silver) and $299 (gold).
  - Shipping status conflicts across sources: summer 2026, then "Fall/Winter 2026", and a later update says batches 1–5 are sold out with batch 6 shipping January 2027 in the US.
  - iPhone-only at launch.
  - Sources: [Italic blog: voice recorder rings](https://app.italic.com/blog/voice-recorder-rings); [Legend Memory: Index 01 vs Stream](https://legendmemory.ai/blogs/the-archive/pebble-index-01-vs-sandbar-stream); [Cloudspress](https://www.cloudspress.com/?p=616798)
- **Wizpr Ring (VTouch, Korea):**
  - Won a CES 2024 Innovation Award.
  - Titanium/epoxy ring of about 4 g holding a battery, CPU, mic, proximity sensor, and BLE radio/antenna.
  - Turns on when raised to the mouth via the proximity sensor, so it needs no button or wake word.
  - Battery reportedly about 90 h of "regular use" or **14 h of continuous voice connection**.
  - Launched on Kickstarter / Product Hunt around May 2024. I found no current sales status.
  - Sources: [TechRadar](https://www.techradar.com/health-fitness/fitness-trackers/this-smart-ring-is-actually-a-secret-microphone-used-to-interface-with-ai-chatbots); [Wareable](https://www.wareable.com/wearable-tech/wizpr-ring-lets-you-talk-to-chatgpt-in-private); [Product Hunt](https://www.producthunt.com/products/wizpr-ring)

### Inferences
- **[ESTIMATE] Continuous capture + streaming budget.** These are illustrative numbers, not measured:
  - Mic about 0.3–0.8 mA (high-performance/normal modes above).
  - CPU running PDM decimation + codec: about 1–3 mA. This is unsourced and depends on the SoC and codec.
  - Radio average about 0.5–1.5 mA. A 16–32 kbps stream is only a few percent of a 2 Mbps PHY's airtime, but connection events, RX windows, and retransmissions add overhead. The peak figures are the 4.8 mA TX / 3.4 mA RX above.
  - Total ≈ **2–5 mA average**.
- **[CALC] Minutes per charge.**
  - A 20 mAh cell at about 80% usable capacity gives 16 mAh.
  - 16 mAh ÷ 2–5 mA ≈ **3.2–8 hours** of continuous streaming.
  - Wizpr's claimed 14 h continuous implies an average of only about 1.1–1.4 mA on a 15–20 mAh cell. That is plausible only with heavy optimization (low-power mic mode, low bitrate, long connection intervals), or the claim is optimistic.
- **[CALC] Always-on listening cost.**
  - Even an AAD-mode mic at about 20 µA, plus SoC sleep, is small: 0.02 mA × 24 h ≈ 0.5 mAh/day.
  - Running a full-power mic plus on-ring keyword spotting continuously, at about 1–2 mA **[ESTIMATE]**, would use 24–48 mAh/day. That exceeds a whole ring battery, so a ring cannot run always-on full listening for a day.
  - This is why every product uses push-to-talk, touch, or proximity gating.
- Index 01 chose a primary (non-rechargeable) cell. That removes the charging coil and charger, and the user never has to charge. The costs are a fixed total budget (about 12–15 h of recording), e-waste/return logistics, and a hard ceiling on features. It is a deliberate "low duty cycle only" bet.
- 12–16 h of total or "frequent use" recording is the current market reference point. For short voice notes (for example 20 × 30 s per day = 10 min/day), that equals days to weeks per charge **[CALC]**.

### Gaps
- No teardown confirming the Index 01 SoC or cell capacity (mAh). No Sandbar Stream or Wizpr battery capacity in mAh.
- Oura and Ultrahuman capacities were not found in this session.
- No published measurements of actual ring audio-streaming current. All the system-level numbers above are estimates.
- Nordic/Ambiq app notes with measured BLE audio streaming current were not retrieved.

## 2. Audio quality, sampling rates, codecs, BLE bandwidth, buffering and latency

### Takeaway
Speech needs only 16 kHz sampling ("wideband"). Modern codecs carry it in about 16–32 kbps: LC3 starts at 32 kbps for the LE Audio 16 kHz voice preset, and Opus is commonly lower. That is a small fraction of BLE's 1–2 Mbps PHY, so bandwidth is not the bottleneck; power and mic placement are. Store-and-forward in on-ring flash is cheap. Even 5 minutes of compressed audio is about 1 MB. Mic placement on the finger is the real quality constraint. A ring is a close-talk mic only when the hand is raised to the mouth, which is why Wizpr uses a raise-to-mouth proximity trigger and why Index 01's mic is "short range".

### Cited Findings
- LC3 (LE Audio codec):
  - Supports 8, 16, 24, 32, 44.1 and 48 kHz sampling at 16/24/32-bit.
  - Frames are 20–400 bytes per channel, which is 16–320 kbps at 10 ms frames.
  - The LE Audio 16 kHz voice preset (16_2) uses 10 ms frames of 40 bytes, which is **32 kbps**.
  - Sources: [Fora Soft LC3 explainer (2026)](https://www.forasoft.com/learn/audio-for-video/articles-audio/lc3-lc3plus-bluetooth-le-audio); [BLEFYI LE Audio overview](https://blefyi.com/guide/le-audio-overview/)
- Bluetooth SIG listening tests found LC3 at 32 kbps matched SBC at 66.4 kbps in quality. — [Bluetooth SIG: LC3 Characterization white paper](https://www.bluetooth.com/wp-content/uploads/2023/07/LC3Characterization_WP.pdf)
- Nordic positions LE Audio/LC3 as the low-power successor to classic Bluetooth audio. — [Nordic blog: One step closer to Bluetooth LE Audio](https://blog.nordicsemi.com/getconnected/one-step-closer-to-bluetooth-le-audio)
- The nRF54L15 supports BLE 2 Mbps / 1 Mbps / 500 kbps / 125 kbps PHYs, with −96 dBm sensitivity at 1 Mbps. — [nRF54L15 datasheet v0.8](https://www.mouser.com/datasheet/2/297/nRF54L15_nRF54L10_nRF54L05_Datasheet_v0_8-3568773.pdf); [Nordic nRF54L15](https://www.nordicsemi.com/Products/nRF54L15)
- Index 01 buffers up to about 5 min of audio on the ring and syncs when the phone is back in range. The ring–phone link is encrypted. — [Pebble blog: Meet Index 01](https://repebble.com/blog/meet-pebble-index-01-external-memory-for-your-brain); [Pebble Index 01 page](https://repebble.com/index?amp=&amp=)
- Microphone sensitivity examples:
  - Sandbar says its mic picks up quiet speech, including whispers. — [Sandbar Stream](https://www.sandbar.com/stream?pubDate=20251106); [DEV Community first look](https://dev.to/logicverse_2025/sandbar-stream-ring-first-look-the-whisper-activated-ai-smart-wearable-for-your-finger-18cj)
  - Wizpr filters background noise so users can whisper. — [TechRadar](https://www.techradar.com/health-fitness/fitness-trackers/this-smart-ring-is-actually-a-secret-microphone-used-to-interface-with-ai-chatbots)
- Index 01 is described as having a "short range microphone". — [TechCrunch](https://techcrunch.com/2025/12/09/pebbles-founder-introduces-a-75-ai-smart-ring-for-recording-brief-notes-with-a-press-of-a-button)
- Analysts note that a ring's limited room for battery and mics makes long recordings and noisy environments harder. This is commentary, not a test. — [AndroidExperto](https://androidexperto.com/?p=575705)

### Inferences
- **[CALC] Storage math:**
  - Raw 16 kHz × 16-bit mono PCM = 256 kbps ≈ 32 KB/s ≈ 1.9 MB/min.
  - LC3 at 32 kbps ≈ 4 KB/s ≈ 240 KB/min, so 5 min ≈ 1.2 MB.
  - A codec at 16 kbps ≈ 120 KB/min, so 5 min ≈ 600 KB.
  - The roughly 1–2 MB of internal flash on BLE SoCs, or a small external NOR flash, therefore covers minutes of buffering. Index 01's 5-minute cap fits this order of magnitude.
- **[CALC] Bandwidth headroom:** 32 kbps is about 1.6% of the 2 Mbps PHY raw rate and about 3.2% of 1 Mbps. Even after protocol overhead (practical GATT throughput is well below the raw rate), streaming voice over plain GATT notifications is feasible on BLE 4.2/5.x. LE Audio (ISO channels + LC3) is not required for a ring→phone voice uplink.
- **Codec tradeoff [ESTIMATE / general engineering knowledge, not verified in this session]:**
  - ADPCM (4:1, about 64 kbps at 16 kHz) is nearly free in CPU but doubles the radio airtime and flash use.
  - Opus/LC3 at 16–32 kbps saves radio and flash but costs more CPU.
  - On a 20 mAh ring the radio and flash savings usually win, but this should be benchmarked.
- **Mic placement:** speech level falls roughly with distance. A mic 3–5 cm from the lips (hand raised) gives far better SNR than one at a resting hand about 50–70 cm away. Raise-to-mouth gating helps the battery and audio quality at once **[ESTIMATE; physics-based, no ring-specific measurement found]**.
- **Latency [ESTIMATE]:**
  - A 10 ms LC3 frame plus BLE connection interval (7.5–30 ms typical) plus phone buffering suggests about 50–150 ms ring→phone.
  - Cloud STT plus LLM plus TTS round trips will dominate (seconds).
  - Store-and-forward (Index 01 style) trades latency for robustness.

### Gaps
- No measured ring SNR, frequency response, or intelligibility versus hand-to-mouth distance was found. No academic paper on finger-worn mic intelligibility was retrieved in this session.
- No source found confirming the codec used by Index 01, Sandbar Stream, or Wizpr.
- mSBC (classic HFP wideband, 64 kbps) and Opus bitrate figures were not verified in this session.
- No measured practical BLE 2M PHY GATT throughput figure was retrieved.
- No measured end-to-end latency for any mic ring.

## 3. Speech-to-text accuracy for low-bitrate, near-whisper audio

### Takeaway
Whispered speech is markedly harder for STT because it lacks voicing (glottal excitation). Off-the-shelf OpenAI Whisper reportedly scored about 19% WER on whispered speech, versus single-digit WER on normal speech, and fine-tuning roughly halves that. On-device options matured in 2025–2026: Pebble runs open-source STT locally on the phone, and Apple's iOS 26 SpeechAnalyzer runs fully on-device. Accuracy on low-bitrate, ring-captured whispers is not benchmarked publicly.

### Cited Findings
- Baseline OpenAI Whisper reached about **18.8% WER** (4.24% CER) on whispered speech. A self-supervised fine-tuned system cut this to **9.22% WER**, using about 17 h of wTIMIT whispered training data. — [arXiv 2407.21211](https://arxiv.org/html/2407.21211v1); [PDF](https://arxiv.org/pdf/2407.21211)
- Earlier end-to-end work cited **29.4% WER** as the best prior result on wTIMIT whispered speech. Pseudo-whisper data augmentation gave an 18.2% relative improvement. Missing glottal information is identified as the core cause of the gap. — [arXiv 2311.05179](https://arxiv.org/abs/2311.05179)
- wTIMIT has 450 phonetically balanced utterances in normal and whispered modes. Hybrid ASR with whisper augmentation achieved a 23% relative WER reduction on whisper test sets. — [Interspeech 2020 paper](http://www.interspeech2020.org/uploadfile/pdf/Wed-1-8-6.pdf)
- Whisper-to-normal voice conversion reduced WER on wTIMIT/CHAINS by about 65%. — [arXiv 2004.09347](https://arxiv.org/pdf/2004.09347)
- Real-time whisper→normal voice conversion was demonstrated (WESPER). DualVoice distinguishes whispered from normal voice input as an interaction channel. — [arXiv 2303.01639](https://arxiv.org/pdf/2303.01639); [arXiv 2208.10499](https://arxiv.org/pdf/2208.10499)
- Pebble Index 01 processes recordings with **open-source STT and an LLM locally on the phone**, with no cloud required (it works in airplane mode). — [Pebble blog](https://repebble.com/blog/meet-pebble-index-01-external-memory-for-your-brain); [BGR](https://www.bgr.com/2048340/pebble-index-01-smart-ring-ai-voice-recording-notes/)
- Apple **SpeechAnalyzer / SpeechTranscriber (iOS 26)**:
  - Fully on-device with no server fallback, replacing SFSpeechRecognizer and its roughly 1-minute practical limit. No watchOS support.
  - Apple published no WER numbers.
  - One third-party benchmark reported 2.12% WER on clean English, versus 3.74% for Whisper Small. Treat this as a single, unverified data point.
  - Sources: [Kompozy review](https://kompozy.io/reviews/apple-speechanalyzer); [Blake Crosley](https://blakecrosley.com/blog/speech-framework-vs-sfspeechrecognizer); [rohitraj.tech](https://rohitraj.tech/notes/apple-speechanalyzer-vs-whisper-on-device-stt-2026); [Fora Soft iOS STT 2026](https://www.forasoft.com/blog/article/speech-recognition-with-neural-networks-on-ios-1621)

### Inferences
- A ring product targeting whispering should expect roughly 2× or worse WER relative to normal speech with generic models. It should plan for one or more of these:
  - asking users to speak softly rather than truly whisper;
  - fine-tuning, or choosing a vendor model robust to whisper;
  - a whisper→voiced conversion front end.
- Low bitrate (16–32 kbps wideband) likely matters less than the whisper and distance factors, because these codecs are designed for speech at these rates **[ESTIMATE]**. Avoid narrowband (8 kHz) capture, since it discards the high-frequency fricative energy that whispered speech relies on **[ESTIMATE]**.
- On-device phone STT (Apple SpeechAnalyzer, or local Whisper variants like the WhisperKit-type approach Pebble uses) supports a "no cloud" privacy story, which also eases consent and GDPR concerns.

### Gaps
- Not verified this session: Deepgram (Nova-3), AssemblyAI, and Google Cloud STT performance on whispered or 8/16 kHz low-bitrate audio. No vendor benchmark on whispers was found.
- No study of STT accuracy specifically on audio from finger-worn mics.

## 4. Interaction design: trigger method, wake word, feedback, returning responses

### Takeaway
The market has converged on explicit, user-initiated capture: button hold (Index 01), touch on a glass touchpad (Sandbar), or proximity raise-to-mouth (Wizpr). Feedback comes through in-ring haptics or an LED. Spoken responses go to earbuds or a phone or speaker, because a ring has no useful speaker. Wake words are avoided because always-on listening is too costly for the battery and raises legal and privacy concerns.

### Cited Findings
- Index 01 records only while the button is **pressed and held**, not on a single press. It has an RGB LED for feedback. Pebble says it is working on using the button as a remote camera shutter. — [MacRumors](https://www.macrumors.com/2025/12/09/pebble-index-01-smart-ring/); [Android Authority](https://www.androidauthority.com/pebble-index-01-announced-3623631)
- Recordings are transcribed, then an on-device LLM selects an action (note, reminder, etc.). — [Pebble Index 01 page](https://repebble.com/index?amp=&amp=)
- Sandbar Stream feedback and responses:
  - Without earbuds, Stream confirms actions with in-ring haptics.
  - With earbuds or a speaker, it can answer questions conversationally and search the web.
  - Without them, the user gets only notifications and haptics.
  - Touch-to-record rather than always-on is praised as the privacy approach.
  - Sources: [Sandbar Stream](https://www.sandbar.com/stream?pubDate=20251106); [Italic blog](https://app.italic.com/blog/voice-recorder-rings)
- Wizpr activates via a proximity sensor when raised to the mouth (no button, no wake word). It works with ChatGPT/Gemini via the phone app and can control smart home devices. — [TechRadar](https://www.techradar.com/health-fitness/fitness-trackers/this-smart-ring-is-actually-a-secret-microphone-used-to-interface-with-ai-chatbots); [Dezeen](https://www.dezeen.com/2024/03/25/wizpr-smart-ring-vtouch-ai-design-technology/amp/)
- TDK's AAD mode (about 20 µA) is marketed for edge-AI "wake on sound" designs. It can wake a host SoC when sound is present. — [Syntiant/TDK T5838](https://www.syntiant.com/press-release/blog-post-title-three-mmhbm/)

### Inferences
- **Trigger options from cheapest to costliest in power [ESTIMATE]:**
  1. Mechanical button: near-zero idle power, and it is unambiguous.
  2. Capacitive touch: about µA-level idle.
  3. Proximity/IMU raise-to-mouth: needs a sensor polling, so tens of µA to sub-mA.
  4. Acoustic activity detect plus keyword spotting: AAD at about 20 µA, plus SoC KWS when it triggers. Costly in noisy environments, where the mic wakes often.
  5. Full always-on wake word.
- A press-and-hold gesture also gives a visible, deliberate act. That supports consent and "bystander awareness" arguments (Section 5) and prevents accidental pocket recordings.
- For elderly users or users with motor issues, hold-to-talk on a small ring button may be hard. Raise-to-mouth or tap-to-start/tap-to-stop with a timeout are alternatives **[ESTIMATE]**.
- Return channel: ring haptics for acknowledge/error, phone notification for text, and earbud TTS for conversational answers. A ring speaker is not practical given the size and power.

### Gaps
- No published measurements of false-trigger rates for proximity or touch triggers on rings.
- No usability studies of ring push-to-talk found.

## 5. Legal: recording-consent laws, bystanders, workplace, app-store/OS rules

### Takeaway
Capturing the wearer's own voice notes is low-risk. Capturing conversations with other people is where the law bites:
- **US:** most states are one-party consent, but about 11–13 states, including **California** and **Florida**, require all parties' consent for confidential conversations.
- **EU GDPR:** regulators read the "household exemption" narrowly (Ryneš), and the EDPB says device makers are controllers in their own right. Always-on capture of bystanders is therefore a compliance problem for the company, not just the user.
- **Mexico and El Salvador:** both broadly allow a participant to record their own conversation. Intercepting other people's conversations, or misusing or publishing recordings, is criminal.
- **App stores:** Android 14+ blocks starting microphone capture from the background, which pushes designs toward user-initiated capture.

### Cited Findings
**United States**
- Counts of all-party-consent states vary: about 11, 12, or 13 states depending on the source and on whether phone calls or in-person talk is counted. California and Florida are consistently listed as all-party. — [RCFP Reporter's Recording Guide intro](https://www.rcfp.org/introduction-to-reporters-recording-guide/); [Scribbl 50-state guide (2026)](https://scribbl.co/post/do-you-have-to-tell-people-youre-recording); [Brass Transcripts 2026 guide](https://brasstranscripts.com/blog/state-by-state-recording-laws-2026-guide); [Wikipedia: Legality of recording by civilians](https://en.wikipedia.org/wiki/Legality_of_recording_by_civilians)
- California and Florida details:
  - California Penal Code 632 applies a "confidential communication" standard and requires all-party consent for confidential in-person and phone conversations.
  - Florida requires all-party consent for oral, wire and electronic communications.
  - Sources: [Interviewer Signal: two-party consent states](https://interviewersignal.com/blog/two-party-consent-states); [Brass Transcripts](https://brasstranscripts.com/blog/state-by-state-recording-laws-2026-guide)
- Split rules:
  - Connecticut and Nevada require all-party consent for phone calls but one-party for in-person conversations.
  - Hawaii and Maine are one-party except in particularly private places.
  - Michigan's status is contested.
  - Source: [Interviewer Signal](https://interviewersignal.com/blog/two-party-consent-states)
- The RCFP intro page that surfaced is several years old. State pages should be checked directly. — [RCFP](https://www.rcfp.org/introduction-to-reporters-recording-guide/)

**European Union (GDPR)**
- In CJEU *Ryneš* (C-212/13), the household exemption did not cover a home camera that partly covered public space. Regulators apply this narrow reading to wearables. — [Noerr: private recordings with wearables in public](https://www.noerr.com/en/insights/private-video-recordings-made-using-wearables-in-public-spaces); [Beauchamps: Smart surveillance devices and GDPR](https://www.beauchamps.ie/publications/20706)
- The EDPB's statement on smart glasses:
  - Manufacturers and AI providers are controllers in their own right and cannot shift GDPR duties onto wearers.
  - Current recording indicators leave many bystanders unaware.
  - Sources: [PPC Land on EDPB](https://ppc.land/edpb-says-smart-glasses-makers-cant-rely-on-wearers-to-meet-gdpr-duties/); [technologylaw.ai](https://www.technologylaw.ai/p/edpb-statement-data-protection-vulnerabilities-smart-glasses)
- Hamburg's DPA found Ray-Ban Meta glasses expose bystanders without consent. It cites Ryneš, Lindqvist and Buivids to argue the household exemption does not reliably cover covert capture of bystanders. — [PPC Land: Hamburg regulator](https://ppc.land/hamburg-regulator-finds-ray-ban-meta-glasses-expose-bystanders-without-consent/)
- The Dutch DPA tested six AI camera glasses and advised consumers not to buy them yet. — [Captain Compliance](https://captaincompliance.com/education/dutch-ap-ai-smart-glasses-risks/)
- Commentary (August 2026) argues LED indicators are an "illusion" of transparency under GDPR. — [Data Laws](https://datalaws.net/2026/08/blinded-by-the-led-smart-glasses-gdpr-and-the-illusion-of-hardware-indicators/)
- Counter-view: some commentators say Art. 2(2)(c) is purpose-based and technology-neutral, so private recording in public could still qualify for the exemption. This runs against the regulators' line. — [Noerr](https://www.noerr.com/en/insights/private-video-recordings-made-using-wearables-in-public-spaces)
- Publishing footage, or using a wearable for professional activities, generally falls outside the household exemption. — [Oxivue smart glasses EU guide (2026)](https://oxivue.com/guides/are-smart-glasses-legal-in-europe)

**Mexico**
- A participant may record a conversation they take part in without notifying the others (Art. 16 of the Constitution as interpreted by the SCJN). A third party intercepting other people's communications without consent or a court order commits a prohibited intervention. — [RecordingLaw: Mexico (2026)](https://www.recordinglaw.com/es/world-laws/world-recording-laws/mexico-recording-laws/); [Vocera](https://vocera.mx/blog/es-legal-grabar-llamadas-mexico)
- Recording is not in itself a crime, but publishing or misusing recordings can be. Recent coverage cites penalties of up to 12 years for spying or dissemination. — [Sociedad Noticias (Oct 2026)](https://sociedad-noticias.com/2026/10/16/grabar-a-alguien-sin-su-consentimiento-en-mexico-cuando-es-legal-y-cuando-puede-ser-delito/); [Publikt Digital (Oct 2026)](https://publiktdigital.com.mx/2026/10/21/grabar-sin-permiso-no-siempre-es-delito-pero-espiar-o-difundir-puede-costar-hasta-12-anos-de-carcel/); [Publimetro (Oct 2026)](https://www.publimetro.com.mx/noticias/2026/10/08/cuidado-con-lo-que-publicas-exhibir-audios-y-videos-en-redes-puede-llevarte-a-prision/)
- Conflicting claim: a LinkedIn article says rules differ by state (Estado de México vs CDMX). Not verified. — [LinkedIn: ¿Es delito grabar una conversación sin permiso?](https://es.linkedin.com/pulse/es-delito-grabar-una-conversaci%C3%B3n-sin-permiso-echegaray-rivera)

**El Salvador**
- Constitution Art. 24 protects private correspondence and prohibits interfering with or intercepting telecommunications. Exceptionally, a judge can authorize temporary intervention in writing with stated reasons. — [Asamblea Legislativa decree](https://www.asamblea.gob.sv/sites/default/files/documents/decretos/02E04307-2B83-4625-B7C6-42D07960F426.pdf)
- A Sala de lo Constitucional ruling says a person in a conversation accepts that the other participant may record it covertly. — [Jurisprudencia.gob.sv (2011, Inc. 39-2005/48-2005)](https://www.jurisprudencia.gob.sv/DocumentosBoveda/D/1/2010-2019/2011/01/8CF3D.PDF)
- A secondary blog says the Penal Code punishes capturing communications without consent to violate privacy (Art. 186) and unauthorized phone interception (Art. 302). This needs checking against the current Code. — [Asistente Legal SV](https://www.asistente-legal.com/sv/blog/posts/como-proteger-tus-derechos-conoce-la-legislacion-salvadorena-sobre-la-grabacion-de-personas-sin-consentimiento)

**OS / app-store**
- Android 14+:
  - Apps must declare foreground service types.
  - The OS checks RECORD_AUDIO when a microphone-type foreground service is created.
  - An app **cannot create a microphone foreground service while it is in the background**, including from BOOT_COMPLETED, with a few exceptions.
  - Sources: [Android Developers: FGS types](https://developer.android.com/develop/background-work/services/fgs/service-types); [Android Developers: background-start restrictions](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start); [Android 14: FGS types required](https://developer.android.com/about/versions/14/changes/fgs-types-required)

### Inferences
- **Product design implications:**
  1. Default to explicit, momentary capture (hold-to-talk) of the wearer's own voice. In one-party jurisdictions, and as a participant in Mexico or El Salvador, this is generally lawful.
  2. Any "record the meeting/conversation" mode needs an explicit consent flow and visible/audible signaling. It must also be disabled or warned about in all-party US states and the EU.
  3. Under GDPR, the company is likely a controller of bystander audio. That brings duties around lawful basis, transparency, minimization (transcribe on-device, then discard audio), retention limits, and a DPIA.
  4. On-device transcription with no cloud upload (Pebble's approach) reduces exposure but does not remove the consent question.
- **Android background capture:** BLE audio arriving from the ring is not the phone microphone. Whether a companion app can receive and process ring audio in the background via a connectedDevice-type foreground service, rather than a microphone type, should be confirmed with Android docs and Play policy. Implementers should not assume it is unrestricted **[ESTIMATE]**.
- **Workplace:** employer monitoring rules and all-party consent laws make always-on capture at work risky. Many employers ban recording devices in meetings **[ESTIMATE; not sourced this session]**.

### Gaps
- Not retrieved this session: Apple App Store Review Guidelines and iOS background-mode rules for receiving or processing audio from a BLE accessory, and iOS recording indicators.
- EU AI Act obligations for always-on audio wearables (transparency, emotion recognition bans) were not researched.
- No primary-source text of the SCJN Mexico rulings or the current Salvadoran Penal Code articles (only secondary sources).
- No US workplace-specific (NLRA/EEOC/state) guidance on wearable mics retrieved.
- Other Latin American countries (Brazil LGPD, Colombia, etc.) were not covered.

## 6. Safety and regulatory: battery safety, SAR/RF exposure, FCC/CE, IP68 with a mic port

### Takeaway
A BLE ring transmits at very low power. Under FCC KDB 447498 it usually qualifies for SAR test exclusion through a power/distance/frequency formula, with the looser 10-g extremity limits applying to a finger-worn device. It still needs FCC Part 15 and CE (RED) authorization. Water resistance with an open mic port is a known engineering tension. Index 01 claims to be waterproof, but I found no sourced detail on how mic rings seal the acoustic port.

### Cited Findings
- FCC KDB 447498 SAR exclusion:
  - Standalone exclusion formula: [(max power in mW) / (separation in mm)] × √f(GHz) ≤ 3.0 for 1-g SAR and ≤ 7.5 for 10-g extremity SAR.
  - Extremity (10-g) thresholds are 2.5× the 1-g thresholds.
  - Sources: [FCC KDB 447498 D01 General RF Exposure Guidance](https://apps.fcc.gov/kdb/GetAttachment.html?id=f8IQgJxTTL5y0oRi0cpAuA%3D%3D&desc=447498+D01+General+RF+Exposure+Guidance+v06&tracking_number=20676); [FCC published comments document](https://apps.fcc.gov/eas/comments/GetPublishedDocument.html?id=493&tn=162660)
- In late 2019 the FCC's Second Report and Order replaced service-based exemptions with formula-based exemptions. An interim guidance document (KDB 447498 D04) was issued in Nov 2021. — [FCC KDB 447498 D04 Interim Guidance](https://apps.fcc.gov/kdb/GetAttachment.html?id=Z0Stk%2FPOk2hqHgYJNt%2FRlQ%3D%3D&amp=&desc=447498+D04+Interim++General+RF+Exposure+Guidance+v01&tracking_number=20676)
- A 2022 FCC TCB workshop proposed requiring full end-product certification for handheld/wearable hosts such as smartwatches, with module exceptions. This was a proposal. — [FCC TCB Workshop Oct 2022](https://transition.fcc.gov/oet/ea/presentations/files/oct22/40-Part-IIRF-Expos-Policies-&-Procs-Eqpt-Auth_r1-TCB_Oct_2022.pdf)
- Example SAR exclusion calculation reports filed for low-power devices exist on fcc.report. — [fcc.report SAR exclusion example](https://fcc.report/FCC-ID/2AYGF-RLW001/7452475.pdf)
- Index 01 is described as waterproof and uses a silver-oxide primary cell, the same chemistry as hearing aids. — [T3](https://www.t3.com/active/fitness-trackers/pebble-index-01-ring-announcement-2025); [Lord of the Smart Rings](https://www.lordofthesmartrings.com/pebble-index-01-review/)
- Smart-ring batteries are typically tiny Li-polymer cells of about 15–25 mAh that need protection circuitry. Testing them is challenging. — [Neware: Smart ring battery testing challenges](https://www.neware.net/news/smart-ring-battery-life-and-testing-challenges/230/225.html); [Ufine](https://www.ufinebattery.com/applications/smart-ring-battery/)

### Inferences
- **[CALC] SAR exclusion example:** 0 dBm = 1 mW at 2.45 GHz with about 5 mm separation gives (1/5) × √2.45 ≈ 0.31. That is far below 7.5 (extremity) and even below 3.0 (1-g), so SAR testing is likely excluded. Even +8 dBm (6.3 mW → rounded to 6 mW) gives (6/5) × 1.565 ≈ 1.9, still under 3.0. Confirm the distance and tune-up assumptions with an accredited lab.
- **Battery safety:** a Li-po cell pressed against skin needs protection (over-charge, over-discharge, over-temperature), IEC 62133 / UN 38.3 transport testing, and swelling margins. Primary silver-oxide cells avoid charging risk but create disposal and return logistics **[ESTIMATE; standards not verified this session]**.
- **IP68 vs mic port:** the usual approach is a hydrophobic acoustic membrane (for example ePTFE) over the mic port. It costs a few dB of sensitivity and can muffle the sound when wet **[ESTIMATE; not sourced this session]**.

### Gaps
- No sourced information on acoustic vent membranes (ePTFE), their insertion loss, or IP68 test conditions for mic rings.
- CE/RED specifics (EN 300 328, EN 62479 low-power exposure) were not retrieved.
- IEC 62133 / UL / UN 38.3 battery requirements for rings were not retrieved.
- The FCC KDB 447498 version current in November 2026 is unconfirmed. A draft v07 raised concerns about body-worn low-power exemptions, and its final status is unknown.
