# Dev kits, open ring platforms and components for prototyping a microphone smart ring (as of Nov 2026)

Research note on method: about 20 searches and fetches. Several primary-source hosts could not be reached from this research session (DNS blocked by the session's network allowlist): linuxiac.com, hackster.io, techcrunch.com, wiki.seeedstudio.com, gadgetbridge.org, bestmag.co.uk. For those, I used search-result snippets or left the point as a gap. Search-snippet claims are marked "(snippet)" where I could not open the page.

## 1. What open or hackable ring platforms exist?

### Takeaway
The cheapest way to hack a real ring is the Colmi R02 family (BlueX RF03 SoC, unsigned OTA firmware, several open clients). It has no microphone, so it is good for practising IMU and PPG work but not audio. The Pebble Index 01 is the only consumer ring with a microphone that its maker calls open source. Omi (Based Hardware) has fully open nRF5340 hardware under MIT, but as a pendant, not a ring. Nordic and Ambiq do not publish an official smart-ring reference design. Instead, ring makers use ready-made "ring chiplets" (Bravechip) and SiP modules built on nRF54L15 or Apollo330B Plus. For bench prototyping, the Seeed XIAO nRF52840 Sense (mic + IMU, about $16–21) and the Arduino Nicla Voice (NDP120 wake-word chip + nRF52832, about €55–87) are the practical stand-ins.

### Cited Findings
**Colmi R02 / RF03-family rings (hackable, no microphone)**
- The atc1441 repo ATC_RF03_Ring has findings and custom firmware for the Colmi R02 "and similar" rings. Specs: SoC BlueX Micro RF03 (Cortex-M0, 200 KB RAM, 512 KB flash), heart-rate sensor VCare VC30F, accelerometer STK8321, 17 mAh battery, SWD debug pins P00/P01. Firmware is flashed OTA from a browser (Web Bluetooth) using the ATC_RF03_Writer tool. The repo includes an example mod firmware "R02_3.00.06_FasterRawValuesMOD.bin". It does not mention a microphone — [GitHub atc1441/ATC_RF03_Ring](https://github.com/atc1441/ATC_RF03_Ring)
- Hackaday reported the firmware has "no signing, no encryption, and you can upload your own firmware over BLE" (snippet) — [Hackaday, "New part day: a hackable smart ring" (2024-06-16)](https://hackaday.com/2024/06/16/new-part-day-a-hackable-smart-ring)
- Open clients for stock firmware: tahnok/colmi_r02_client, a Python client installable with pipx — [GitHub](https://github.com/tahnok/colmi_r02_client), [docs](https://tahnok.github.io/colmi_r02_client/colmi_r02_client.html). qlam-ai/qring, a Python client that works with rings sold for the "QRing" app (snippet) — [GitHub](https://github.com/qlam-ai/qring). smittytone's ringcli, a Go CLI whose author found three R02s running slightly different firmware (snippet) — [blog](https://blog.smittytone.net/2025/04/09/hoard-of-the-rings-colmi/); [Hackaday 2025-03-04](https://hackaday.com/2025/03/04/cheap-hackable-smart-ring-gets-a-command-line-client)
- Hackaday's 2025 coverage says some firmware details are still unknown, such as how day phases are tracked and how SpO2 works (snippet) — [Hackaday 2025-03-04](https://hackaday.com/2025/03/04/cheap-hackable-smart-ring-gets-a-command-line-client)
- Community projects include a Colmi R02 MIDI-controller mod (smartringmidi), which also ships firmware with faster raw-data streaming (snippet) — [TechEBlog](https://www.techeblog.com/colmi-r02-smart-ring-midi-controller-mod/); [uithub mirror](https://uithub.com/mrfloydst/smartringmidi). Hugging Face's "Halo" open health-tracking project also uses the ring (snippet) — [HF blog](https://huggingface.co/blog/cyrilzakka/halo-introduction)
- Gadgetbridge lists Colmi as "Highly supported / No-vendor pair" and has a Yawell ring page. I could not open the pages to confirm models and features (snippet) — [Gadgetbridge Colmi](https://gadgetbridge.org/gadgets/wearables/colmi); [Gadgetbridge Yawell rings](https://gadgetbridge.org/gadgets/rings/yawell/)
- The "opensmartring" GitHub org builds GPL-3.0 alternative firmware for the "RF02" ring. It has 3 repos, 0 stars, and its last update was Nov 2024, so it is early-stage and quiet — [GitHub opensmartring](https://github.com/opensmartring)

**Pebble Index 01 (Core Devices), a consumer ring with a microphone**
- Announced Dec 9, 2025. It has one button and a microphone and records only while the button is held. It stores up to about 5 minutes of audio on the ring. The battery is non-rechargeable: when it runs out, you mail the ring back for recycling and replacement. Speech-to-text and AI run locally on the phone through the Pebble app. Reported prices are $75 (pre-order) and $99 (snippets) — [TechCrunch](https://techcrunch.com/2025/12/09/pebbles-founder-introduces-a-75-ai-smart-ring-for-recording-brief-notes-with-a-press-of-a-button); [Engadget](https://www.engadget.com/wearables/pebble-is-making-a-weird-little-smart-ring-for-recording-thoughts-161723645.html); [MacRumors](https://www.macrumors.com/2025/12/09/pebble-index-01-smart-ring/)
- On openness, coverage says the software is open source and "designed to be hacked". Migicovsky says Pebble is "leaving the side door open for folks to customize" (snippets) — [Techdirt](https://www.techdirt.com/2025/12/11/repebble-creates-an-open-source-99-voice-recorder-ring-you-can-hack/); [Linuxiac](https://linuxiac.com/pebble-index-01-arrives-as-a-private-open-source-voice-capture-ring/); [Hackster](https://www.hackster.io/news/core-devices-unveils-the-pebble-index-01-a-disposable-smart-ring-microphone-c103c26e4f24)

**Omi / Based Hardware**
- The Omi Consumer hardware is MIT-licensed. Published design files include schematics, Gerbers, STEP files, BOM and assembly guides. The main board uses an nRF5340 dual-core BLE SoC plus an nRF7002 Wi-Fi chip (Wi-Fi not enabled in current firmware). There is also a magnetic charger dock and a flex PCB. Firmware uses Zephyr/nRF Connect in C. The docs warn that nRF5340/nRF7002 lead times are 2–4 weeks at Mouser and DigiKey (snippet) — [Omi docs: consumer hardware](https://docs.omi.me/doc/hardware/consumer); [BasedHardware/omi README](https://raw.githubusercontent.com/BasedHardware/omi/main/README.md)
- I found no ring form factor in Omi's hardware docs (see Gaps).

**Nordic- and Ambiq-based ring reference material**
- My search found no official Nordic "smart ring reference design" for the nRF54L15. Nordic publishes generic reference layouts for the QFN48 and CSP47 packages — [Nordic nRF54L15 reference layout](https://www.nordicsemi.com/Products/nRF54L15/Reference-layout). A user-shared "Smart Ring" schematic with an nRF54L15 MCU sheet (Rev 1, dated 12-11-2025) is on DevZone. It is a community file, not a Nordic design — [DevZone Smart_Ring.pdf](https://devzone.nordicsemi.com/cfs-file/__key/communityserver-discussions-components-files/4/Smart_5F00_Ring.pdf)
- Commercial nRF54L15 rings: Yuwell Smart Ring R3. Nordic's write-up credits the nRF Connect SDK reference designs — [Nordic news, Jul 2026](https://cm.nordicsemi.com/Nordic-news/2026/07/Health-monitoring-ring-Yuwells-Smart-Ring-R3-and-the-nRF54L15). IDO IDR01, whose maker cites Nordic's "high-quality reference designs" — [Nordic news, Oct 2025](https://www.nordicsemi.com/Nordic-news/2025/10/IDOs-IDR01-smart-ring-integrates-Nordics-nRF54L15-SoC)
- Ring-ready modules: Bravechip BCL603S2H, a 5×5 mm smart-ring chiplet built on the nRF54L15 — [Nordic news, Aug 2025](https://www.nordicsemi.com/Nordic-news/2025/08/Bravechip-chiplet-integrates-nRF54L15-to-supervise-sensors-and-power-seamless-wireless-connectivity). Tangshan Hongjia HJ-N54L SiP, with antenna, dual crystals, RF matching and DC-DC built in, aimed at rings and hearing aids — [Nordic news, Jan 2026](https://www.nordicsemi.com/Nordic-news/2026/01/Tangshan-Hongjias-employs-Nordics-nRF54L15-SoC-to-power-smart-rings-and-hearing-aids)
- Ambiq + Bravechip BCL603S3H (announced Jan 6, 2026): a SiP built on the Apollo330B Plus that integrates more than 20 components. The vendor claims "up to 85%" lower smart-ring cost, 20% better yield and up to 7 days of battery life. The baseline for the 85% figure is not given — [Ambiq press release](https://ambiq.com/news/ambiq-and-bravechip-cut-smart-ring-costs-by-85-with-new-edge-ai-chiplet/). The earlier BCL603S3L used the Apollo3 Blue in a 4×6.8 mm LGA — [Ambiq news, 2024](https://ambiq.com/news/bravechip-and-ambiq-bring-low-power-innovation-to-smart-rings-with-bcl603s3l/)
- Ambiq's customer page lists the Noise Luna Ring on the Apollo3 Blue Plus — [Ambiq customers](https://ambiq.com/customers)
- The Apollo4 Lite is aimed at watches and bands, not rings. Its dev kit is the AMAP4LEVB, and the chip comes in a 5×5 mm BGA (snippet) — [Mouser Apollo4 Lite](https://www.mouser.in/new/ambiq/ambiq-apollo4-lite-soc/); [Apollo4 Lite product brief](https://contentportal.ambiq.com/documents/20123/1730118/Apollo4-Lite-SoC-Product-Brief.pdf)

**Bench stand-ins**
- Seeed XIAO nRF52840 Sense: Pimoroni's listing names the LSM6DS3TR IMU and the MSM261D3526H1CPM PDM microphone — [Pimoroni](https://shop.pimoroni.com/products/seeed-xiao-ble-nrf52840-sense). Prices: £15.90 inc. VAT at The Pi Hut — [Pi Hut](https://thepihut.com/products/seeed-xiao-ble-nrf52840-sense); $16.82 (sale) and $20.84 (with tariffs) at RobotShop — [RobotShop](https://robotshop.com/products/seeed-studio-xiao-nrf52840-sense). A separate "XIAO nRF52840 Sense Plus" also exists — [Pi Hut](https://thepihut.com/products/xiao-nrf52840-sense-plus)
- Arduino Nicla Voice: nRF52832 BLE MCU plus a Syntiant NDP120 neural decision processor (Cortex-M0 + HiFi 3 DSP + Syntiant Core 2). It has a microphone, a 6-axis IMU and a magnetometer, measures 22.86 × 22.86 mm and weighs about 2 g — [Make:](https://makezine.com/products/boards/arduino-nicla-voice); [Arduino store](https://store.arduino.cc/en-pt/collections/home-automation/products/nicla-voice). Launch price was $82 / €69 — [CNX Software](https://cnx-software.com/2023/01/28/arduino-nicla-voice-always-on-speech-recognition-syntiant-ndp120-neural-decision-processor). Current listings range from about €55.30 to €86.60 — [Arduino store](https://store.arduino.cc/collections/pro-family/products/nicla-voice); [Arduino store BG](https://store.arduino.cc/en-bg/products/nicla-voice). RS lists £59.20 ex-VAT — [RS](https://uk.rs-online.com/web/p/arduino/2654984)

### Inferences
- Fastest prototyping path (inference). (a) Bench-test the audio and wake-word pipeline on the XIAO nRF52840 Sense or Nicla Voice. (b) Learn ring mechanics, PPG/IMU data and the BLE protocol on a $20–30 Colmi R02 with open clients. (c) Move to a custom flex PCB around a ring SiP/chiplet (Bravechip nRF54L15 or Apollo330B Plus parts, or the Hongjia HJ-N54L) instead of laying out a bare CSP SoC yourself.
- The Pebble Index 01 is the closest commercial analogue to a "mic ring". Since its software is reportedly open, it is worth buying and studying for its UX: push-to-talk, on-ring storage, phone-side STT. Its non-rechargeable battery design shows one way to avoid the charging problem altogether.
- The Colmi RF03 SoC is a Cortex-M0 with a 17 mAh cell and no audio interface noted. It is unlikely to be a usable base for audio even with custom firmware (inference from the specs above).

### Gaps
- The Pebble Index 01's SoC, microphone part, battery chemistry, repo location and license could not be verified: the primary articles were blocked and the snippets did not name them.
- Omi ring form factor: none found. Omi docs list only the consumer pendant and older dev kits in the pages I saw.
- I did not research Colmi R06 hacking specifically. I could not open the Gadgetbridge pages to confirm which models (R02/R03/R06/R09/R10) and features are supported.
- Hackaday.io "open ring" projects beyond the above: none found in my searches.
- Movesense, Ultrahuman developer offerings and the Oura API (data-only) were not researched due to the tool budget. Arduino Nicla Voice was covered.
- I found no official Nordic or Ambiq "ring reference design" document. Ambiq says it partners on smart rings, but the design files appear to come through partners like Bravechip and are not public.

## 2. Key SoCs: power draw and audio capabilities

### Takeaway
The nRF54L15 is now the default BLE SoC in new rings: a 2.45 × 2.25 mm CSP, about 3.4 mA RX and 4.8 mA TX at 0 dBm. However, Nordic says it lacks an audio PLL and has only limited LE Audio support. If you need LC3/LE Audio streaming, the nRF5340 (which Omi uses) is the safer Nordic choice. Ambiq's Apollo330B Plus is the low-power edge-AI alternative and is already packaged as a ring SiP.

### Cited Findings
- nRF54L15: the CSP package is 2.45 × 2.25 mm (snippet) — [Nordic nRF54L15](https://www.nordicsemi.com/products/nrf54l15). The product page lists 3.4 mA RX and 4.8 mA TX at 0 dBm (3 V) (snippet) — [Nordic nRF54L15](https://nordicsemi.com/Products/nRF54L15)
- A datasheet excerpt quoted on DevZone gives 3.2 mA RX at 1 Mbps (3.0 V) and about 2.1 mA RX with DC/DC. Nordic staff note that the SoftDevice Controller enables constant-latency mode, which adds current. One user measured a 3.73 mA average RX on the DK — [DevZone thread 127777](https://devzone.nordicsemi.com/f/nordic-q-a/127777/nrf54l15-ble-rx-current-comsumption/566776); [DevZone thread 116451](https://devzone.nordicsemi.com/f/nordic-q-a/116451/bluetooth-le-rx-current-comsumption-for-nrf54l15-dk-is-higher)
- On LE Audio, Nordic replies on DevZone say the nRF54L series has no audio PLL, so TWS use cases are not possible, and audio sample support is "limited" — [DevZone thread 117778](https://devzone.nordicsemi.com/f/nordic-q-a/117778/nrf54l15-support-le-audio)
- nRF5340: dual-core BLE SoC used in Omi's open-source wearable — [Omi docs](https://docs.omi.me/doc/hardware/consumer)
- Ambiq Apollo330B Plus: shares the Apollo510B architecture minus the GPU, for a smaller footprint and lower power; it is the base of the BCL603S3H ring SiP — [Ambiq press release](https://ambiq.com/news/ambiq-and-bravechip-cut-smart-ring-costs-by-85-with-new-edge-ai-chiplet/). The Apollo330 Plus series is a Cortex-M55 family with optional BLE 5.4 / 802.15.4 radios — [CNX Software, May 2025](https://www.cnx-software.com/2025/05/30/ambiq-apollo330-plus-soc-series-cortex-m55-mcu-family-offers-optional-bluetooth-5-4-le-and-802-15-4-radios/?amp=1)
- Ambiq has also announced "Atomiq", described as an ultra-low-power NPU SoC built on its SPOT platform (headline only) — [Barchart/press](https://www.barchart.com/story/news/36904932/ambiq-unveils-atomiq-the-worlds-first-ultra-low-power-npu-soc-built-on-spot)

### Inferences
- For a ring that captures voice memos and sends them in bursts over GATT (not real-time LE Audio streaming), the nRF54L15 is enough and has the best ring-module ecosystem. The decision to make early: do you need real-time LC3 / Auracast to earbuds or phones? If yes, prototype on the nRF5340 Audio DK.

### Gaps
- Not researched due to the tool budget: nRF54H20 power and audio, Apollo4/Apollo5 audio interfaces and current, Realtek RTL87xx, Bluetrum and Telink chips. Their PDM/I2S and LC3 capabilities and µA/MHz figures need a follow-up.
- I found no measured current for LC3 encoding on the nRF54L15 or nRF5340.

## 3. Tiny MEMS microphones and voice-activity / wake-word chips

### Takeaway
The TDK InvenSense T5838 is the reference low-power PDM mic. It draws about 20 µA with on-mic acoustic activity detection (AAD), about 120–130 µA in low-power mode and about 310–330 µA in high-quality mode, so the ring can sleep until sound arrives. For on-device wake words, the Syntiant NDP120 claims under 280 µW for "Hey Google" detection, and it is available on the Arduino Nicla Voice for prototyping.

### Cited Findings
- T5838: AAD with three modes, from 20 µA total. Sleep is about 9 µA, low-power mode about 120–130 µA, high-quality mode 330 µA in an older release and 310 µA at 1.8 V in a later one. Modes include high quality, low-power (always-on), ultrasonic and sleep — [TDK T5838 product page](https://invensense.tdk.com/products/digital/t5838/); [T5838 datasheet DS-000383 v1.0](https://www.mouser.lt/catalog/specsheets/TDK_DS-000383-T5838-v1.0.pdf); [TDK launch release](https://invensense.tdk.com/news-media/tdk-introduces-worlds-lowest-power-PDM-microphone-with-acoustic-activity-detect/); [TDK edge-AI release](https://invensense.tdk.com/news-media/tdk-low-power-t5838-mems-microphones-edge-ai-applications/)
- The XIAO nRF52840 Sense uses the MSM261D3526H1CPM PDM mic (a reference for a cheap commodity mic) — [Pimoroni](https://shop.pimoroni.com/products/seeed-xiao-ble-nrf52840-sense)
- Syntiant NDP120: vendor claim of under 280 µW for "Hey Google / OK Google" detection on Syntiant Core 2. Its predecessor, the NDP100, was certified for Alexa wake words in 2019 — [Amazon developer blog](https://developer.amazon.com/en-US/blogs/alexa/alexa-skills-kit/2021/02/syntiant-low-power-semiconductors.html); [EE World](https://www.eeworldonline.com/low-power-conversational-ai-chips-support-google-hot-words/); [NDP120 product brief](https://static1.squarespace.com/static/6488b0b8150a045d2d112999/t/650b29219d8c3f0e27f4651e/1695230242406/Syntiant-Product_Brief_NDP120.pdf)
- AONDevices AON1120: a sensor-fusion IC introduced at CES 2025 for voice commands, sound classification and biometrics. The coverage I found gives no µW figure — [All About Circuits](https://www.allaboutcircuits.com/news/aondevices-shows-off-sensor-fusion-ic-targeting-always-on-designs)

### Inferences
- Lowest-power architecture (inference): T5838 AAD (about 20 µA) wakes the SoC, then the SoC records PDM at about 310 µA mic current only while voice is present. Or skip always-on listening entirely and use a push-to-talk button, as the Pebble Index 01 does.
- A separate wake-word chip (NDP120) adds board area and current, roughly 280 µW ≈ 75 µA at 3.7 V (my calculation). That only pays off if hands-free wake words are a core feature.

### Gaps
- Knowles (SiSonic, AISonic), Infineon XENSIV IM69D/IM73, TDK ICS-41352 and Vesper (now Qualcomm) specs and package sizes were not researched due to the tool budget.
- No unit prices were found for the T5838 or NDP120.

## 4. IMUs and PPG sensors

### Takeaway
The ST LSM6DSV16X has an on-chip machine-learning core (MLC) and finite-state machine, so it can classify gestures and activity without waking the MCU. ST shows about 19 µA when still. ADI's MAX86176 is a 2.7 × 2.7 mm WLP PPG + ECG front-end with under 11 µA per optical channel at 25 fps. Cheap rings use commodity parts instead (Colmi: STK8321 accelerometer + VCare VC30F HR sensor).

### Cited Findings
- LSM6DSV16X: 0.65 mA in combined high-performance mode (accelerometer + gyroscope) — [ST product page](https://www.st.com/en/mems-and-sensors/lsm6dsv16x.html); [ST blog](https://blog.st.com/?p=25597). An adaptive self-configuration demo shows 19.46 µA when STILL and 689.70 µA when FASTMOVING. The MLC lets you avoid waking the MCU — [ST community article](https://community.st.com/t5/mems-and-sensors/how-to-save-power-with-lsm6dsv16x-by-leveraging-on-its-adaptive/ta-p/580690); [Future Electronics](https://www.futureelectronics.com/ftm/ai-edge-solutions/stmicroelectronics-lsm6dsv16x-imu)
- MAX86176: two optical PPG readout channels plus single-lead ECG, running at the same time. 2.728 × 2.708 mm WLP, optical channel under 11 µA typical at 25 fps, shutdown under 1 µA, in production — [ADI MAX86176](https://www.analog.com/en/products/max86176.html); [datasheet](https://www.analog.com/MAX86176/datasheet)
- Colmi R02 parts: STK8321 accelerometer and VCare VC30F heart-rate sensor — [ATC_RF03_Ring](https://github.com/atc1441/ATC_RF03_Ring)

### Inferences
- For gestures (tap, twist) and step counting on a ring, an MLC/FSM IMU such as the LSM6DSV16X lets the SoC stay asleep. This matters more than raw sensor current on a 15–30 mAh budget.

### Gaps
- Bosch BMI270 / BHI380 current figures were not found in this session. ams PPG parts and the MAX86178 were not researched in depth.
- No component prices were found for the IMUs or PPG front-ends.

## 5. Batteries, charging and the energy budget for audio

### Takeaway
Curved ring Li-po cells sit roughly in the 15–30 mAh range at 3.7–3.8 V. Ufine lists 16, 18 and 20 mAh curved cells, and a Global Sources seller lists a 24 mAh cell at $1.55–1.85 (MOQ 1,000). The Colmi R02 uses 17 mAh. A 20 mAh cell stores about 74 mWh, so continuous audio capture and streaming lasts hours, not days.

### Cited Findings
- Ufine 150732 curved cell: 3.7 V, 20 mAh, about 0.074 Wh, internal resistance under 1000 mΩ, no PCM or NTC, about 0.52 g — [Ufine 20 mAh](https://www.ufinebattery.com/products/3-7-v-20mah-curved-battery-150732). Ufine also lists 16 mAh and 18 mAh curved cells — [Ufine 16 mAh](https://www.ufinebattery.com/products/3-7-v-16mah-curved-battery-156825); [Ufine 18 mAh](https://ufinebattery.com/products/3-7-v-18mah-curved-battery-160630)
- A Global Sources seller lists a 3.8 V 24 mAh "150732" arc cell at $1.55–1.85 per piece, MOQ 1,000 (snippet) — [Global Sources](https://www.globalsources.com/knowledge/lithium-polymer-battery-for-smart-rings/)
- Grepow: patented curved ring battery tech (Oct 2025) claiming 30% more capacity, UN38.3 and CB certified, ISO 13485 production (snippet) — [Grepow smart ring](https://www.grepow.com/wearables/smart-ring.html); [PR Newswire release](https://tools.prnewswire.com/en-us/live/20813/release/20251015EN98565)
- MOTOMA lists custom-arc ring cells from 20 to 100 mAh at 3.7–3.88 V, and its 2026 guide puts 20–25 mAh cells in NFC payment rings. These are vendor marketing claims (snippet) — [MOTOMA](https://motoma.com/lip-applications/2026-smart-ring-battery-trends-polymer-lithium-battery-solutions.html)
- The Colmi R02 battery is 17 mAh — [ATC_RF03_Ring](https://github.com/atc1441/ATC_RF03_Ring)
- The Pebble Index 01 avoids charging altogether with a sealed non-rechargeable battery and a mail-back replacement (snippet) — [Engadget](https://www.engadget.com/wearables/pebble-is-making-a-weird-little-smart-ring-for-recording-thoughts-161723645.html)
- The Omi pendant uses a magnetic charging dock (snippet) — [Omi docs](https://docs.omi.me/doc/hardware/consumer)

### Inferences
These are estimates: my arithmetic from the cited figures, not measurements.
- Energy: 20 mAh × 3.7 V ≈ 74 mWh (matches Ufine's 0.074 Wh).
- Always-listening floor: T5838 AAD 20 µA plus a few µA of SoC sleep is about 25–30 µA. A 20 mAh cell would then last about 650–800 h (27–33 days) if nothing else ran.
- Active recording: mic 310 µA plus SoC/PDM processing of about 1–2 mA gives roughly 1.5–2.5 mA, about 8–13 h of recording on 20 mAh.
- Continuous BLE streaming: adding radio activity (3.4 mA RX / 4.8 mA TX peaks, with duty cycling) gives about 3–5 mA average, roughly 4–7 h.
- So a mic ring needs push-to-talk or VAD gating, on-ring buffering and burst transfer to reach multi-day battery life. Continuous streaming is not viable on 15–30 mAh.

### Gaps
- No ring-specific charger IC or wireless/contact charging part (e.g., Nordic nPM1300 / nPM2100, TI BQ25120-class) was researched. Only a DevZone thread mentions an nRF5340 + nPM1300 schematic request — [DevZone](https://devzone.nordicsemi.com/f/nordic-q-a/121143/to-get-the-reference-schematic-in-terms-of-nrf5340-npm1300)
- Grepow's NeoRRow capacity table could not be loaded.

## 6. Approximate BOM cost for a microphone ring

### Takeaway
I found no published component-level BOM for a microphone ring. The only cited price points are the about $1.55–1.85 curved cell, about $16–21 bench boards and a $75–99 retail price for the Pebble Index 01. Any full BOM figure is an estimate (below).

### Cited Findings
- 24 mAh curved cell: $1.55–1.85 at MOQ 1,000 (snippet) — [Global Sources](https://www.globalsources.com/knowledge/lithium-polymer-battery-for-smart-rings/)
- Retail price of a shipping mic ring (Pebble Index 01): $75 pre-order / $99 (snippets) — [MacRumors](https://www.macrumors.com/2025/12/09/pebble-index-01-smart-ring/); [Techdirt](https://www.techdirt.com/2025/12/11/repebble-creates-an-open-source-99-voice-recorder-ring-you-can-hack/)
- Ambiq/Bravechip claim their integrated ring SiP cuts ring cost by "up to 85%" (no baseline given) — [Ambiq](https://ambiq.com/news/ambiq-and-bravechip-cut-smart-ring-costs-by-85-with-new-edge-ai-chiplet/)
- Complete hackable rings (Colmi R02) are sold cheaply enough to be called "cheap hardware" by Hackster and Hackaday. I did not verify an exact current price — [Hackster](https://www.hackster.io/news/unlocking-the-potential-of-cheap-hardware-f02f20797794); [Tedium review](https://tedium.co/2024/11/08/colmi-r02-hacker-ring-review/)

### Inferences
The figures below are an ESTIMATE from my own industry judgement, not sourced, at about 10k units:
| Part | Estimated cost |
|---|---|
| BLE SoC or ring SiP (nRF54L15-class) | $1.5–4 |
| PDM MEMS mic (T5838-class) | $0.5–1.5 |
| 6-axis IMU with MLC | $1–2 |
| PPG front-end + LEDs + photodiode (optional) | $2–4 |
| SPI NOR flash for audio buffering (8–16 MB) | $0.3–0.8 |
| Curved cell (cited) | about $1.6–1.9 |
| PMIC/charger + passives | $1–2 |
| Flex PCB + assembly | $2–5 |
| Shell (titanium or steel + epoxy fill) | $3–10 |

- That totals roughly **$12–30 for a mic + IMU ring without PPG**, and roughly $15–35 with PPG, before charger dock, packaging and certification. Founders should validate this with distributor quotes (DigiKey/Mouser/LCSC) and a contract manufacturer.
- Prototype-stage spend (estimate): $20–90 per bench board (XIAO Sense / Nicla Voice), $20–30 per Colmi R02 for teardown and hacking, plus flex PCB prototype runs, which typically cost hundreds of dollars per spin.

### Gaps
- No teardown with a component cost breakdown was found for any microphone ring (Pebble Index 01, or others in the companion research).
- No distributor unit prices were retrieved for the nRF54L15, T5838, LSM6DSV16X or MAX86176.
