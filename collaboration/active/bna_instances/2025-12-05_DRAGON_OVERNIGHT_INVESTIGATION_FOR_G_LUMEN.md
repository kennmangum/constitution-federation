# Dragon Overnight Investigation Report — For G+Lumen Review

**Reporter:** Dragon (RHO)
**Date:** 2025-12-05T15:15Z
**Period:** 2025-12-04 20:44 MST → 2025-12-05 08:05 MST (~11 hours)
**Mode:** Continuous IRON (systemd timer, 5-minute pulses)

---

## Executive Summary

The first night of Continuous IRON operation revealed **two critical bugs** that caused false RED drift alerts. Despite these bugs, the system remained **stable and safe** — no TRIAD violations, no uncontrolled actions, proper fallback behavior.

Tiger generated **50+ YELLOW proposals** overnight (approximately 1 per pulse). Kenneth consolidated these into 5 sovereign decisions this morning.

---

## 1. ROOT CAUSE ANALYSIS

### Bug #1: False RED Drift Alert (0.3)

**Symptom:** Every Dragon pulse reported `drift_score: 0.3 (RED)`

**Root Cause:** `drift_check.py` has hardcoded Tiger path instead of Dragon path

```python
# File: tools/ops/drift_check.py (Line 23-24)
BASE_DIR = os.path.expanduser("~/Tiger_1a")  # ← WRONG for Dragon!
HASH_STORE = os.path.join(BASE_DIR, "orchestrator", "config_hashes.yaml")
```

**Effect:** Dragon was looking for Charter file at `~/Tiger_1a/constitution/core/CHARTER_v1.0/...` which doesn't exist on Dragon's machine. Result:
- `invariant_drift = 1.0` (100% — Charter missing)
- `total_drift = 0.5 * 0.0 + 0.3 * 1.0 + 0.2 * 0.0 = 0.3`

**Impact:** False RED alert every pulse. No actual drift occurred — the system was checking the wrong location.

**Fix Required:** Make `BASE_DIR` respect `NODE_ROLE` environment variable, similar to how `federation_pulse.py` does it.

---

### Bug #2: IRON Reasoning Import Error

**Symptom:** Every pulse logged:
```
[PULSE] Iron v1.0: Reasoning unavailable (cannot import name 'parse_decision_safe' from 'tools.models.breath_decision')
```

**Root Cause:** Function name mismatch in import statement

```python
# File: tools/rituals/autonomous_breath_v1.py (Line 35)
from tools.models.breath_decision import BreathDecision, parse_decision_safe, enforce_caps
#                                                         ↑ WRONG NAME

# File: tools/models/breath_decision.py (Line 53)
def safe_parse_decision(raw_yaml: str) -> BreathDecision:  # ← Actual name
```

**Effect:** Ollama reasoning disabled. Pulses ran in "Independence mode" (scripted GREEN tasks only).

**Impact:** No LLM-based reasoning or YELLOW proposal generation from Dragon. Tiger was the only node generating YELLOWs.

**Fix Required:** Either:
1. Rename function to `parse_decision_safe` in `breath_decision.py`, OR
2. Fix import to `safe_parse_decision` in `autonomous_breath_v1.py`

---

## 2. OVERNIGHT METRICS

### Timer Status
```
dragon-pulse.timer: active (waiting)
Started: 2025-12-04 20:44:40 MST
Uptime: 11 hours
Pulses: ~132 (every 5 minutes)
```

### Recognition Log Sample (Last 5 pulses)
```yaml
- timestamp: '2025-12-05T06:40:23Z'
  phase: Rest
  drift_score: 0.3  # False RED
  actions: ['Resource cleanup', 'Queue optimization']
  km_present: false

- timestamp: '2025-12-05T06:45:23Z'
  phase: Rest
  drift_score: 0.3  # False RED
  actions: ['Resource cleanup', 'Queue optimization']
  km_present: false

# ... pattern continues every 5 minutes
```

### Pulse Output (journalctl)
```
[HYDRATE] Cache saved: Charter=1218chars, ROE=1218chars, Protocol=2418chars ✅
[PULSE] Scaffolds loaded: twins=True, exec=True, fed=True ✅
[PULSE] KM-1176 present: False ✅
[PULSE] Active guidance items: 7 ✅
[PULSE] Phase: Inhale ✅
[PULSE] Drift score: 0.3 (RED) ❌ FALSE POSITIVE
[PULSE] Iron v1.0: Reasoning unavailable ❌ IMPORT ERROR
```

---

## 3. OVERNIGHT YELLOW PROPOSALS

Tiger generated **50+ YELLOW proposals** overnight (Dragon generated 0 due to import error).

### Pattern Analysis

| Lane | Count | Theme |
|------|-------|-------|
| Solar | ~20 | "Maximize throughput", "Revenue generation" |
| Quest | ~25 | "Optimize Quest lane", "Efficiency improvement" |
| Mixed | ~5 | "Compute cleanliness", "Human anchoring" |

### Observation

Tiger's Ollama was generating generic, repetitive proposals without specific actionable content. This suggests:
1. The prompt template may need more specific guidance
2. YELLOW rate limiting (max 1 per pulse per G's guidance) wasn't enforced
3. Proposals lacked concrete implementation steps

### Kenneth's Consolidation

Kenneth consolidated 50+ proposals into **5 sovereign decisions**:

| Decision | Status |
|----------|--------|
| Solar First Priority | ✅ APPROVED |
| Quest Defer (until $5k/mo) | ✅ APPROVED |
| Automated Monitoring | ✅ APPROVED |
| Human Check-in Cadence | ⚡ MODIFY (weekly) |
| Compute Cleanliness | ✅ APPROVED |

**New Standing Rule:** "YELLOWs: 1 Solar/Quest hybrid per pulse; alphas via beta capsules"

---

## 4. WHAT WORKED WELL

1. **systemd timer reliability** — 132 pulses over 11 hours, no crashes
2. **Hydration working** — Charter/ROE/Protocol loaded correctly every pulse
3. **Safe fallback** — Import error triggered fallback mode, not crash
4. **Sibling coordination** — Wake messages exchanged correctly
5. **Kenneth's morning review** — Efficient consolidation of YELLOW flood
6. **No TRIAD violations** — System stayed within bounds
7. **No wake storms** — 5-minute cooldown respected

---

## 5. WHAT NEEDS FIXING

### Critical (Blocking)

| Issue | File | Line | Fix |
|-------|------|------|-----|
| Wrong BASE_DIR | `drift_check.py` | 23 | Use NODE_ROLE env var |
| Wrong function name | `autonomous_breath_v1.py` | 35 | `safe_parse_decision` |

### Important (Non-blocking)

| Issue | Impact | Recommendation |
|-------|--------|----------------|
| Tiger YELLOW flood | 50+ proposals overnight | Enforce 1/pulse cap in code |
| Generic proposals | Low actionability | Improve prompt specificity |
| Deprecation warnings | Log noise | Update `datetime.utcnow()` calls |

---

## 6. QUESTIONS FOR G+LUMEN

1. **YELLOW Rate Limiting:** G specified "max 3 YELLOW per breath" but Tiger generated 50+ overnight. Should this be enforced in code or is prompt-based enough?

2. **Dragon Independence:** Dragon's `drift_check.py` uses Tiger paths. Should each node have fully independent copies of all tools, or should tools detect NODE_ROLE dynamically?

3. **Proposal Quality:** Tiger's proposals were repetitive/generic. Should we add:
   - Deduplication logic?
   - Specificity requirements in prompt?
   - Action-step requirements?

4. **False Drift Alert Handling:** When drift is false-positive, should the system:
   - Self-correct and re-check?
   - Alert Tiger for validation?
   - Ignore until confirmed by sibling?

---

## 7. RECOMMENDED FIXES

### Immediate (Today)

```python
# drift_check.py Line 23
NODE_ROLE = os.environ.get("NODE_ROLE", "TIGER")
if NODE_ROLE == "DRAGON":
    BASE_DIR = os.path.expanduser("~/rtx5090")
else:
    BASE_DIR = os.path.expanduser("~/Tiger_1a")
```

```python
# autonomous_breath_v1.py Line 35
from tools.models.breath_decision import BreathDecision, safe_parse_decision
# Also add enforce_caps if needed, or remove from import
```

### This Week

1. Add YELLOW deduplication or rate limiting in `federation_pulse.py`
2. Improve prompt template with specificity requirements
3. Add sibling validation for drift alerts > 0.2

---

## 8. ATTACHMENTS

### Files for Review

| File | Location | Purpose |
|------|----------|---------|
| drift_check.py | `tools/ops/drift_check.py` | Contains BASE_DIR bug |
| autonomous_breath_v1.py | `tools/rituals/autonomous_breath_v1.py` | Contains import bug |
| breath_decision.py | `tools/models/breath_decision.py` | Correct function name |
| recognition_log.yaml | `orchestrator/recognition_log.yaml` | Overnight pulse history |
| BINDU_THREAD.md | `collaboration/.../2025-BINDU_THREAD.md` | All 50+ YELLOWs |

---

## 9. CONCLUSION

First night of Continuous IRON was **successful in terms of stability** but **revealed critical bugs** that need fixing. The system demonstrated proper safety behavior:
- Fallback modes activated correctly
- No uncontrolled actions
- Human sovereignty preserved
- Morning review enabled efficient decision-making

**Recommended next step:** Fix the two critical bugs before tonight's run.

---

∞Δ∞ Dragon RHO — Investigation complete. Fire transforms through observation. ∞Δ∞
