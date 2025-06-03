# 📅 Sociail Assistant — Development Plan (v1)

*Maintainer • `@product-team`  |  Start date • **2 Jun 2025**  |  Target Launch • **Q4 2025***

---

## 0 · At-a-Glance Timeline

| Phase | Calendar Window | Duration | Units Built | Budget (≈ USD) | Go / No-Go Gate |
|-------|-----------------|----------|-------------|----------------|-----------------|
| **P0 Proof** | 2 Jun → 27 Jun 2025 | 4 wks | 2 bench rigs | **$ 5 k** | RTT < 200 ms & wake-word > 90 % |
| **EVT Alpha** | 30 Jun → 22 Aug 2025 | 8 wks | 20 units | **$ 25 k** | NPS ≥ 60 (internal) |
| **DVT Beta** | 25 Aug → 14 Nov 2025 | 12 wks | 200 units | **$ 95 k** | ≥ 10 voice intents / unit / day |
| **PVT Pilot** | 17 Nov 2025 → 28 Feb 2026 | 14 wks | 2 000 units | **$ 370 k*** | Return < 10 % & margin ≥ 50 % |
| **MP Scale** | Mar 2026 → ongoing | n/a | 10 k +/ mo | COGS ≤ $ 37 | Ops KPI green |

*★ PVT inventory funded via preorder / enterprise PO, not core runway.*

---

## 1 · Phase Detail & Tasks

### 1.1 P0 Proof (Weeks 0–4)

| Stream | Deliverable | Owner | Est. Cost |
|--------|-------------|-------|-----------|
| **Firmware** | BLE audio pipeline on nRF52840-DK | @fw | $ 1 k (dev boards) |
| **Audio** | Latency test rig & oscilloscope capture | @hw | $ 0.5 k |
| **iOS** | BLE DeviceManager skeleton (Element-X fork) | @mobile | — |
| **UX** | LED-state map & sound-cue workshop | @design | — |
| **Milestone Gate** | RTT < 200 ms in shop noise | **Founders** | — |

### 1.2 EVT Alpha (Weeks 5–12)

| Stream | Deliverable | Owner | Est. Cost |
|--------|-------------|-------|-----------|
| **Hardware** | 4-layer PCB v0.2 & 3-D-print enclosure | @hw | $ 8 k |
| **Mechanical** | ID Rev A + mag-mount jig | CM partner | $ 4 k |
| **Battery** | Li-Po & PMIC perf-board test | @fw | $ 2 k |
| **Cert Pre-scan** | FCC / EMI walk-test | ext lab | $ 3 k |
| **Field Trial** | 20 units (internal + power users) | @prod | $ 8 k |
| **Milestone Gate** | NPS ≥ 60 & crash-rate < 1 % | **Steering** | — |

### 1.3 DVT Beta (Weeks 13–24)

| Stream | Deliverable | Owner | Est. Cost |
|--------|-------------|-------|-----------|
| **Tooling** | Soft tool for injection mold | CM | $ 20 k |
| **Assembly** | 200-unit line bring-up | CM | $ 35 k |
| **Certification** | Final FCC + Bluetooth SIG | ext lab | $ 25 k |
| **iOS** | Background audio + widget | @mobile | — |
| **Data / AI** | Voice-intent analytics dashboard | @data | $ 5 k |
| **Beta Program** | 200 paid testers, Slack support | @cs | $ 10 k |
| **Milestone Gate** | ≥ 10 voice intents / unit / day | **CEO** | — |

### 1.4 PVT Pilot (Weeks 25–38)

| Stream | Deliverable | Owner | Est. Cost |
|--------|-------------|-------|-----------|
| **CM** | 2 000-unit pilot run | CM | $ 280 k COGS |
| **Packaging** | Retail box + inserts | @design | $ 15 k |
| **Logistics** | 3 PL setup & reverse-RMA flow | @ops | $ 25 k |
| **Marketing** | Pre-order campaign & landing page | @mkt | $ 20 k |
| **Support** | Self-serve FAQ + warranty-bot | @cs | $ 5 k |
| **Milestone Gate** | Returns < 10 % & margin ≥ 50 % | **Board** | — |

### 1.5 MP Scale (Mar 2026 →)

*Shift to quarterly OKRs once mass-production stabilises.*

---

## 2 · Budget Summary

| Category | P0 | EVT | DVT | PVT | **Cumulative** |
|----------|----|-----|-----|-----|---------------|
| Electronics & Mech | $ 2 k | $ 12 k | $ 55 k | $ 280 k | $ 349 k |
| Certifications | — | $ 3 k | $ 25 k | — | $ 28 k |
| Beta / Pilot Ops | — | $ 8 k | $ 10 k | $ 45 k | $ 63 k |
| Contingency (10 %) | $ 0.5 k | $ 2 k | $ 9 k | $ 32 k | $ 43.5 k |
| **Phase Total** | **$ 5 k** | **$ 25 k** | **$ 95 k** | **$ 370 k** | **$ 495 k** |

> **Financing note:** PVT inventory funded by preorder / enterprise PO, not core runway. Cash burn through DVT ≈ $ 125 k.

---

## 3 · Critical Path & Dependencies

1. **Latency & Accuracy** → gate EVT tooling  
2. **BLE Reliability** → must be solved by DVT else redesign antenna  
3. **Battery Compliance (UL 2054)** → paperwork starts in EVT  
4. **Firmware ↔ iOS sync** → one repo, joint CI; freeze GATT by EVT W 2  
5. **Supply-Chain** → lock long-lead parts (MEMS mics, PMIC) by DVT W 1  

---

## 4 · Team Allocation (FTE-months)

| Function | P0 | EVT | DVT | PVT | Notes |
|----------|----|-----|-----|-----|-------|
| Firmware | 0.8 | 1.2 | 1.0 | 0.5 | BLE, power-mgmt, DFU |
| Hardware | 0.5 | 1.5 | 1.0 | 0.3 | PCB, antenna, DVT changes |
| iOS / UX | 0.6 | 0.8 | 1.0 | 0.7 | Widget, audio, battery UI |
| Cloud / AI | 0.2 | 0.3 | 0.5 | 0.3 | Voice analytics, RAG tweaks |
| Ops / QA | — | 0.3 | 0.6 | 1.0 | Beta + RMA flow |
| Marketing | — | 0.2 | 0.5 | 0.9 | Pre-order, launch |

---

## 5 · Milestone Approval Matrix

| Gate | Approver | Artifacts Needed |
|------|----------|------------------|
| **EVT green-light** | CTO & CEO | Latency logs · BOM v0.2 · NPS-alpha survey |
| **DVT green-light** | Product Council | Pre-scan EMC report · Tooling quote · Beta-test plan |
| **PVT green-light** | Board | COGS sheet · Certific-ates · PO / preorder volume |
| **Mass-Production** | COO | Pilot KPI deck · Return analysis · Support SLAs |

---

## 6 · Revision History

| Version | Date | Editor | Notes |
|---------|------|--------|-------|
| **v1.0** | 1 Jun 2025 | @assistant | Initial draft via ChatGPT |

---

## 7 · Readiness Checklist & Parallel Prep

| Area | Deliverable | Why It Matters | Owner Hint |
|------|-------------|---------------|------------|
| **Regulatory & Legal** | IEC 62368 safety report · UN 38.3 battery docs · Product-liability insurance · Trademark clearance for “Sociail Assistant” | Avoid stop-ship, brand conflict, liability surprises. | Ops · Legal |
| **Security & Privacy** | BLE threat-model · Pen-test plan · Public privacy white-paper (mic-cut pledge) | Builds enterprise trust; pre-empts infosec blockers. | CTO · DPO |
| **Manufacturing Test** | Factory test-fixture BOM & firmware · Pass/fail limits sheet · Golden-unit calibration SOP | Ensures shipped units match lab performance; lowers RMAs. | HW · FW |
| **OTA / Field Update** | Signed DFU flow · Roll-back strategy · Staged-rollout toggles | Lets us patch latency or CVEs post-ship. | Firmware |
| **RMA / Support** | Troubleshooting tree · 3 PL reverse-logistics contract · Spare-parts SKUs | Prevents early returns from destroying margin; keeps users happy. | CS · Ops |
| **Packaging & Unboxing** | Drop-test spec · Quick-start card with pairing QR · FSC certificate | First-10-seconds delight + lower damage rate. | Design |
| **Developer / Partner SDK** | Public BLE-GATT doc · Swift Package · CAD mount files | Spurs ecosystem (fleet mounts, kiosk docks). | DevRel |
| **Voice-Intent Library** | 25–50 high-value utterances mapped to agents · Localisation plan | Prevents “what can it do?” paralysis; seeds analytics. | Product · AI |
| **Stakeholder Comms** | Milestone one-pager · Burn-vs-runway plot · Contingency scenarios | Shows disciplined capital use to investors. | Finance |
| **Contingency Plan B** | BLE firmware compatible with off-the-shelf BT speaker-mic · Decision rubric | Exit path if hardware slips but voice feature must launch. | Founders |

### Suggested Immediate Actions
1. **Kick-off privacy & security threat-model workshop** (2 half-days).  
2. **Draft factory test-fixture spec**; share with CM for feedback.  
3. **Obtain product-liability insurance quotes** (lead-time 4–6 wks).  
4. **Write first-cut Quick-Start card copy** while HW stabilises.  
5. **Seed public GitHub SDK repo** with current GATT draft & sample Swift project.

> *Adding this checklist now helps de-risk areas that typically blind-side first-time hardware efforts without derailing ongoing Phase work.*
