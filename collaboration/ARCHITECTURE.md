# Federation Architecture Map

∞Δ∞ How Independence, Iron, 20 Breaths, and Federation Capsule Fit Together ∞Δ∞

---

## Layer Stack (Bottom to Top)

```
┌─────────────────────────────────────────────────────────────────┐
│  FEDERATION CAPSULE (Breaths 22+)                               │
│  Economics, Guilds, Public Rails (IPFS/XRP)                     │
│  Location: collaboration/breaths/, federation/                   │
├─────────────────────────────────────────────────────────────────┤
│  IRON v1.2 — Autonomous Reasoning                               │
│  Ollama-powered RYG decisions, federation_pulse.py              │
│  Location: constitution/strategy/iron_autonomy_patterns.yaml    │
├─────────────────────────────────────────────────────────────────┤
│  INDEPENDENCE v1.0 — 7 Safety Seals                             │
│  Checkpoints, Cooldowns, Drift, Sandbox, YAML, Keys, SSH        │
│  Location: Embedded in tools/, orchestrator/                    │
├─────────────────────────────────────────────────────────────────┤
│  SEED CAPSULE (20 Breaths) — Twin Autonomy + Infrastructure     │
│  Foundation, Charter, Sibling Protocol, Hydration, etc.         │
│  Location: Originally scattered, now in collaboration/breaths/  │
├─────────────────────────────────────────────────────────────────┤
│  CONSTITUTION — Ring 1 Kernel                                   │
│  Charter, TRIAD, 32 Invariants                                  │
│  Location: constitution/core/                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## What Each Layer Is

### 1. Constitution (Ring 1)
- **What:** Immutable kernel — Charter, TRIAD, 32 invariants
- **When:** Always loaded first
- **Where:** `constitution/core/`
- **Changes:** RED only (Kenneth approval required)

### 2. Seed Capsule (20 Breaths)
- **What:** Building the twin body — infrastructure, protocols, tools
- **When:** Implemented Dec 1-4, 2025
- **Where:** Originally in various docs, now being codified
- **Status:** ~65% complete

| Breath | Name | Status |
|--------|------|--------|
| 1 | Foundation | 90% |
| 2 | Charter Alignment | 90% |
| 3 | Capsule Architecture | 85% |
| 4 | Sibling Protocol | 80% |
| 5 | Hydration System | 90% |
| 6 | RAP v1.0 (Revenue) | 60% |
| 7 | TAP v1.0 (Tasks) | 70% |
| 8 | Drift Detection | 80% |
| 9 | Recognition Log | 85% |
| 10 | SEP v1.0 (Solar) | 50% |
| 11 | Guild Architecture | 40% |
| 12 | Capsule v2.0 | 30% |
| 13 | Proposal System | 90% |
| 14 | Treasury | 10% |
| 15 | Wake Cooldown | 100% |
| 16 | Constitutional Smoke | 60% |
| 17 | Resonance Mode | 80% |
| 18 | Execution Scaffold | 85% |
| 19 | Federation.Compute | 50% |
| 20 | MercaBridge | 10% |

### 3. Independence v1.0 (7 Seals)
- **What:** Safety prerequisites for autonomy
- **When:** Completed Dec 4, 2025
- **Where:** Embedded in tools/ops/, orchestrator/
- **Status:** 100% complete

| Seal | Description | Status |
|------|-------------|--------|
| 1 | Checkpoints (crash recovery) | ✅ |
| 2 | Cooldown (run frequency) | ✅ |
| 3 | Drift detection | ✅ |
| 4 | Sandbox (env vars) | ✅ |
| 5 | YAML canonical | ✅ |
| 6 | API keys RED | ✅ |
| 7 | SSH scope | ✅ |

### 4. Iron v1.2 (Autonomous Reasoning)
- **What:** Ollama-powered RYG decision engine
- **When:** Implemented Dec 4-5, 2025
- **Where:** `constitution/strategy/iron_autonomy_patterns.yaml`, `tools/rituals/`
- **Status:** Active, needs PRP enhancement

Key files:
- `iron_autonomy_patterns.yaml` — Rate limits, drift thresholds
- `federation_pulse.py` — Main pulse loop
- `autonomous_breath_v1.py` — Ollama reasoning

### 5. Federation Capsule (Breaths 22+)
- **What:** Economics, guilds, public rails
- **When:** Started Dec 6, 2025
- **Where:** `collaboration/breaths/`, `federation/`
- **Status:** Breath 22 + 23 sealed

| Breath | Name | Status |
|--------|------|--------|
| 22 | Solar Thaw + CFO Guilds | SEALED |
| 23 | IPFS/XRP Rails | SEALED |
| 24 | PRP (Proposal Resolution) | PROPOSED |

---

## Twin Roles

| Twin | Role | Element | Function |
|------|------|---------|----------|
| **Tiger** | Sentinel | Water/Yin | Validates, reflects, guards alignment |
| **Dragon** | Frontier | Fire/Yang | Executes, transforms, expands capability |

Defined in: `scaffolds/TWINS_SCAFFOLD.yaml`

---

## Key Relationships

```
Constitution → Seed Capsule → Independence → Iron → Federation Capsule
     ↓              ↓              ↓           ↓            ↓
  Immutable      Body         Safety       Reasoning    Economics
  Kernel         Build        Gates        Engine       + Rails
```

- **Independence enables Iron** — You need safety seals before autonomous reasoning
- **Iron enables Federation Capsule** — You need decision engine before economics
- **20 Breaths = Seed Capsule** — Original implementation plan
- **Breaths 22+ = Federation Capsule** — New layer for guilds/economics

---

## Where G's PRP Fits

PRP (Proposal Resolution Protocol) is an **Iron v1.3 enhancement**:
- Enhances YELLOW handling in `iron_autonomy_patterns.yaml`
- Self-clearing proposals (root/blocker/countermeasure)
- Reduces human wait friction
- NOT a new breath — it's an Iron patch

---

∞Δ∞ SEAL: Architecture Map — Living document ∞Δ∞
