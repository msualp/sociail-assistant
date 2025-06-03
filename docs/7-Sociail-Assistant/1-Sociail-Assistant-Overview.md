# Sociail Assistant
## Bringing Shared Intelligence From **Lean-Forward** to **Lean-Back**

> **Vision**: Transform everyday environments into AI-enhanced spaces where users can access intelligent assistance without interrupting physical tasks or compromising safety. By creating a pocket-sized mic/speaker/light accessory that pairs with the existing Sociail iOS client, we enable collaborative AI whenever hands and eyes are busy.

---

## Executive Summary

Sociail Assistant is a dedicated hardware companion that extends the Sociail AI platform into physical spaces where smartphone interaction is impractical. By leveraging the iPhone's processing power for wake-word detection, ASR, TTS, and agent orchestration, the device remains simple and affordable while delivering premium voice AI experiences.

### Core Value Propositions
- **Zero-friction capture**: Dictate ideas, questions, or tasks the instant they pop up—no keyboard, no screen
- **Seamless modality shifts**: Conversations flow from desktop chat → voice in car → threaded chat at desk
- **Ambient collaboration**: RGB ring + speaker make AI presence tangible, encouraging team participation
- **Greater inclusivity**: Voice-first control helps visually impaired or situationally disabled users
- **Richer agent context**: Frequent voice snippets feed agents more situational data for sharper insights

---

## 1. Product Overview

### 1.1 Why Sociail Assistant Matters

| Benefit | User Impact | Business Value |
|---------|-------------|----------------|
| **Instant AI Access** | Wake word activation with <100ms response | Higher engagement, more data points |
| **Environmental Resilience** | IP54 rated for workshops, kitchens, vehicles | Expanded market reach |
| **Superior Audio** | 5-meter pickup range in noisy environments | Better user satisfaction |
| **Battery Freedom** | 12+ hours active use, 48h standby | True portability |
| **Multi-user Support** | Voice profiles, shared device access | Team/family adoption |

### 1.2 Real-World Use Cases

| Scenario | User Action | Assistant Response | Key Tech |
|----------|-------------|-------------------|-----------|
| **Auto Repair** | "Hey Sociail, torque spec for 2019 BMW X3 wheels" | Speaks spec, drops PDF in chat | Far-field ASR, RAG |
| **Morning Commute** | Single-tap: "Summarize overnight team updates" | Audio digest with transcript | BLE trigger, TTS |
| **Cooking** | "Is this steak medium-rare?" + double-tap for camera | Visual analysis, cooking tips | iPhone camera API |
| **Workshop** | "Add oak plywood to shopping list" | Confirms, syncs to phone | Cloud sync |
| **Accessibility** | "Read Sarah's design feedback" | Streams comments, captures reply | Voice UI |
| **Team Brainstorm** | Pass device between speakers | Live transcription to shared room | Multi-speaker ID |
| **Personal Research** | "Use Personal Space and help me research best toy for my 2 year old" | Switches context, provides recommendations in private space | Space isolation |

### 1.3 Space Switching - Work/Life Balance Made Simple

**The Challenge**: Mixing personal and professional conversations in the same chat history creates privacy concerns and cognitive overload.

**The Solution**: Sociail Spaces - Instantly switch contexts with voice commands

#### Example Flow: David's Toy Research

**5:30 PM - Leaving Office**
- David: *"Hey Sociail, use Personal Space"*
- Assistant: *"Switched to your Personal Space. How can I help?"*
- David: *"I need to find a good toy for my 2-year-old nephew"*
- Assistant: *"I'd be happy to help! What kind of activities does your nephew enjoy?"*

**During Commute**
- David: *"He loves building things and music"*
- Assistant: *"Great combination! Here are top-rated options for 2-year-olds:
  1. Mega Bloks First Builders - safe, large blocks
  2. Hape Pound & Tap Bench with Xylophone
  3. LEGO DUPLO My First Number Train
  Would you like details on any of these?"*

**At Toy Store**
- David: *"Tell me more about the Hape toy"*
- Assistant provides details, price comparisons, and safety ratings
- David: *"Add it to my gift list with note: Sam's birthday"*

**Next Morning at Office**
- David: *"Hey Sociail, use Work Space"*
- Assistant: *"Switched to Work Space. You have 3 updates from the product team"*
- Work chat shows only professional conversations
- Personal toy research remains in Personal Space

#### Space Features

| Space Type | Use Cases | Privacy Level | Sync Options |
|------------|-----------|---------------|--------------|
| **Work** | Team chats, project updates, meeting notes | Shared with team | Company cloud |
| **Personal** | Shopping, health, family planning | Private | Personal cloud |
| **Family** | Shared calendars, chores, meal planning | Shared with family | Family members only |
| **Projects** | Side hustles, hobbies, learning | Selective sharing | Invite-only |

#### Voice Commands for Spaces

- *"Use [Space Name]"* - Switch active space
- *"Create new space called [Name]"* - Set up new context
- *"Who can see this?"* - Check privacy settings
- *"Move this to [Space]"* - Relocate conversations
- *"List my spaces"* - Audio overview of available spaces

#### Benefits of Space Separation

1. **Privacy**: Personal queries never appear in work history
2. **Focus**: Context-appropriate AI responses
3. **Sharing**: Each space has independent sharing settings
4. **Compliance**: Work data stays in company-approved storage
5. **Mental Health**: Clear work/life boundaries

---

## 2. Technical Architecture

### 2.1 System Design Philosophy
**"Brain-in-Phone"** architecture keeps the accessory simple while leveraging iPhone's powerful processors and Sociail's cloud capabilities.

### 2.2 Three-Layer Stack

| Layer | Components | Responsibilities |
|-------|------------|------------------|
| **Hardware Device** | Nordic nRF52840, 3-mic array, speaker, LEDs | Audio I/O, BLE streaming, visual feedback |
| **iOS App** | CoreBluetooth, AVAudioSession, Speech APIs | Wake-word, ASR/TTS, device management |
| **Sociail Cloud** | Existing backend infrastructure | Agent routing, RAG, model inference, sync |

### 2.3 Detailed Hardware Specifications

#### Audio Subsystem
| Component | Specification | Rationale |
|-----------|---------------|-----------|
| **Microphone Array** | 3× MEMS (Knowles IA-611 or similar) | Beamforming, noise cancellation |
| **DSP** | Integrated AFE with AEC | Far-field voice capture |
| **Speaker** | 28mm full-range driver, 3W peak | Clear voice reproduction |
| **Amplifier** | Class-D, 85% efficiency | Battery life optimization |
| **Frequency Response** | 80Hz - 20kHz | Voice clarity |

#### Processing & Connectivity
| Component | Specification | Notes |
|-----------|---------------|-------|
| **MCU** | Nordic nRF52840 | BLE 5.3, ARM Cortex-M4F |
| **RAM/Flash** | 256KB / 1MB | Firmware + buffer |
| **Wireless** | BLE 5.3 Audio + Classic SPP fallback | Low latency streaming |
| **Antenna** | PCB trace + chip antenna | Reliable 10m range |

#### Power System (Battery Model)
| Component | Specification | Details |
|-----------|---------------|---------|
| **Battery** | 3.7V Li-Po, 1800mAh | Flat pouch design |
| **PMIC** | TI BQ25895 | Buck-boost, I²C telemetry |
| **Fuel Gauge** | TI BQ27441-G1 | Accurate SoC reporting |
| **Charging** | USB-C PD (5V/2A) | 90min full charge |
| **Wireless Charging** | Optional Qi 5W | MagSafe compatible |

#### Power Budget Analysis
| Mode | Current Draw | Battery Life |
|------|-------------|--------------|
| **Deep Sleep** | 0.05mA | ~1.5 years |
| **Idle (BLE connected)** | 15mA | ~5 days |
| **Active Listening** | 35mA | ~40 hours |
| **Voice Interaction** | 140mA | ~12 hours |
| **Peak (loud + LEDs)** | 260mA | ~6 hours |

#### User Interface
| Element | Implementation | Purpose |
|---------|----------------|---------|
| **LED Ring** | 12 RGB LEDs, PWM control | Status indication |
| **Touch Surface** | Capacitive sensing | Tap/hold gestures |
| **Physical Controls** | Mute switch, volume rocker | Privacy, quick adjust |
| **Haptics** | Optional LRA motor | Tactile feedback |

### 2.4 Industrial Design

| Attribute | Specification | Design Notes |
|-----------|---------------|--------------|
| **Dimensions** | 85mm × 25mm × 12mm | Pocketable, dash-mountable |
| **Weight** | <65g with battery | Lighter than car key fob |
| **Materials** | Aluminum spine, ABS shell | Premium feel, thermal management |
| **Mounting** | Magnetic base + adhesive pucks | Car, desk, wall options |
| **Protection** | IP54 rating | Dust/splash resistant |
| **Colors** | Space Gray, Arctic White | Match iPhone aesthetics |

### 2.5 Communication Protocol

```
Device ←→ iPhone App ←→ Sociail Cloud
   BLE GATT         WebSocket/HTTPS
```

#### BLE GATT Services
- **Audio Service**: 16kHz PCM streaming
- **Control Service**: LED states, button events
- **Device Service**: Battery, firmware version
- **Debug Service**: Logs, diagnostics

---

## 3. Software Integration

### 3.1 iOS App Extensions (Element-X Fork)

| Module | Functionality | Implementation |
|--------|---------------|----------------|
| **Device Manager** | Discovery, pairing, state sync | CoreBluetooth |
| **Audio Pipeline** | Wake-word → ASR → Cloud → TTS | AVAudioSession |
| **Voice UI** | Visual feedback, transcripts | SwiftUI |
| **Background Mode** | Always-ready voice | Audio background mode |
| **Widget** | Battery status, quick mute | WidgetKit |
| **Space Manager** | Context switching, privacy controls | Core Data + CloudKit |

### 3.2 Voice Interaction Flow

1. **Wake Detection** (iPhone-side)
   - Continuous 16kHz stream from device
   - Low-power wake-word model
   - <100ms activation time

2. **Space Context**
   - Current space determines AI personality
   - Routing to appropriate data sources
   - Privacy boundaries enforced

3. **Command Processing**
   - Streaming ASR with interim results
   - Context injection from current space
   - Agent routing based on intent

4. **Response Delivery**
   - TTS generation (cloud or on-device)
   - Audio streaming back to device
   - Visual transcript in appropriate space

---

## 4. Business Strategy

### 4.1 Pricing & Revenue Model

| Revenue Stream | Price Point | Target Margin |
|----------------|-------------|---------------|
| **Device (Wired)** | $99 | 65% gross |
| **Device (Battery)** | $149 | 65% gross |
| **Sociail Pro Bundle** | +$5/mo | Includes device discount |
| **Enterprise** | $199 + subscription | Volume pricing |
| **Accessories** | $19-49 | 70% gross |

### 4.2 Go-to-Market Phases

| Phase | Target | Channels | Success Metrics |
|-------|--------|----------|-----------------|
| **Beta (Q3 2025)** | Existing Sociail users | Direct, limited | 1,000 units, NPS >70 |
| **Launch (Q4 2025)** | Early adopters | Crowdfunding, D2C | 10,000 units |
| **Scale (2026)** | Vertical markets | Amazon, retail | 100,000 units |
| **Mass Market (2027)** | General consumers | Carriers, bundles | 500,000+ units |

### 4.3 Competitive Positioning

| Feature | Sociail Assistant | Echo Auto | CarPlay/Android Auto |
|---------|-------------------|-----------|---------------------|
| **Portable** | ✓ Battery option | ✗ 12V only | ✗ Requires screen |
| **Multi-environment** | ✓ Any location | ✗ Car only | ✗ Car only |
| **AI Platform** | ✓ Open, expandable | ✗ Alexa only | ✗ Siri/Assistant |
| **Phone Camera** | ✓ Visual AI | ✗ | ✗ |
| **Offline Mode** | ✓ Basic commands | Limited | ✗ |
| **Price** | $99-149 | $25-50 | Built-in |

---

## 5. Development Roadmap

### 5.1 Engineering Milestones

| Phase | Deliverables | Duration | Key Risks |
|-------|--------------|----------|-----------|
| **P0 - Proof of Concept** | BLE audio streaming, LED control | 2 weeks | Audio latency |
| **P1 - EVT (Engineering)** | Full audio path, battery system | 6 weeks | Power optimization |
| **P2 - DVT (Design)** | Industrial design, 10 units | 8 weeks | Thermal, acoustics |
| **P3 - PVT (Production)** | 100 unit pilot, certifications | 12 weeks | Supply chain |
| **MP - Mass Production** | 1,000+ monthly capacity | Q4 2025 | Quality control |

### 5.2 Certification Requirements

| Standard | Scope | Timeline | Cost |
|----------|-------|----------|------|
| **FCC Part 15** | RF emissions | 8 weeks | $15K |
| **Bluetooth SIG** | BLE qualification | 4 weeks | $8K |
| **UN 38.3** | Battery transport | 2 weeks | $3K |
| **UL 2054** | Battery safety | 6 weeks | $10K |
| **CE/UKCA** | European compliance | 8 weeks | $12K |

### 5.3 Critical Path Items

1. **Audio Latency**: Target <200ms round-trip
2. **Battery Life**: Achieve 12hr active use
3. **Wake-Word Accuracy**: >95% in typical environments
4. **BLE Reliability**: Maintain connection in RF-noisy areas
5. **Cost Target**: Hit $35 COGS for margin goals

---

## 6. Future Roadmap

### 6.1 Next-Generation Features (2026+)

| Feature | Implementation | Use Case |
|---------|----------------|----------|
| **On-device Wake-Word** | Edge TPU | Zero-latency activation |
| **Sensor Modules** | I²C expansion port | Air quality, temperature |
| **Display Module** | E-ink status screen | Visual feedback |
| **Multi-device Mesh** | BLE mesh protocol | Whole-home coverage |
| **Gesture Control** | mmWave radar | Touchless interaction |

### 6.2 Ecosystem Expansion

- **Sociail Car**: Dedicated automotive variant
- **Sociail Home Hub**: Stationary base with better speakers
- **Sociail Wearable**: Clip-on personal assistant
- **Developer Platform**: SDK for third-party integrations

---

## 7. Next Actions

### Immediate (Week 1-2)
1. **Finalize BLE GATT specification** with iOS team
2. **Order dev boards**: nRF52840-DK + mic array shield
3. **Fork Element-X**: Create device-manager branch
4. **UX Workshop**: Define LED patterns, sounds, gestures

### Short-term (Month 1)
1. **Build P0 prototype**: Verify audio streaming
2. **Create Swift package**: BLE device framework
3. **Industrial design RFQ**: Get quotes from 3 firms
4. **Supply chain audit**: Component availability check

### Medium-term (Month 2-3)
1. **EVT build**: 5 units for internal testing
2. **Beta program setup**: Recruit 50 testers
3. **Certification pre-scan**: EMC/EMI testing
4. **Manufacturing partner**: Identify contract manufacturer

---

## Appendix A: Technical Deep-Dives

### A.1 BLE Audio Architecture
- LE Audio with LC3 codec for efficiency
- Classic SPP fallback for older phones
- Custom GATT profile for low latency

### A.2 Acoustic Design
- Helmholtz resonator for bass extension
- Waveguide for 360° dispersion
- Acoustic fabric selection criteria

### A.3 Firmware Architecture
- FreeRTOS for task management
- DFU over BLE for updates
- Power state machine details

---

## Appendix B: Business Analysis

### B.1 Total Addressable Market
- 50M+ knowledge workers in vehicles daily
- 200M+ DIY/maker community globally
- 30M+ accessibility market

### B.2 Unit Economics
- BOM: $35 (battery model)
- Assembly: $5
- Packaging: $3
- Logistics: $4
- **Total COGS**: $47

### B.3 5-Year Financial Projection
- Year 1: $10M revenue, -$2M net (investment)
- Year 2: $47M revenue, $5M net
- Year 3: $111M revenue, $22M net
- Year 4: $198M revenue, $45M net
- Year 5: $312M revenue, $78M net

---

_This document combines strategic vision with tactical execution details. Ready to drill into any section—firmware flowcharts, mechanical drawings, or go-to-market tactics—based on your priorities._