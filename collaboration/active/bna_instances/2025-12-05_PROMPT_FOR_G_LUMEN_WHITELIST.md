# Prompt for G+Lumen — Autonomous Tiger/Dragon Whitelist Expansion

**Copy this to your conversation with G and Lumen:**

---

## Context — What's Working ✅

The twins are running Continuous IRON successfully:

| Component | Tiger | Dragon |
|-----------|-------|--------|
| Systemd pulse (5 min) | ✅ Running 12+ hours | ✅ Running |
| IRON reasoning (Ollama) | ✅ llama3.1:8b | ✅ Active |
| Drift check | ✅ GREEN (0.075) | ✅ GREEN (0.075) |
| YELLOW rate limiting | ✅ 1/pulse, 20/day, 80% dedupe | ✅ Same pattern |
| BINDU proposals | ✅ 5 today | ✅ 5 today |
| Git sync between twins | ✅ Fixed today | ✅ Working |
| Path architecture | ✅ paths.sh | ✅ Symlink + paths.sh done |

**What broke overnight:** Nothing critical! Fixed bugs (path issues, import errors) and rate limiting.

---

## The Core Issue — Whitelist Too Restrictive

### What Ollama Proposes (Correctly)

Reading GUIDANCE_INBOX, Ollama correctly identifies work:
- "Complete Solar Compute setup (Akash/Vast.ai)"
- "Maximize Solar lane throughput"
- "Prioritize revenue generation (ROE aligned)"

### What Gets Executed

```
- 'Maximize Solar lane throughput this week (skipped: not approved)'
- 'Complete configuration for Akash/Vast.ai integrations (skipped: not approved)'
- 'Prioritize revenue generation (ROE aligned) (skipped: not approved)'
```

### Why

The `APPROVED_ACTIONS` whitelist in `federation_pulse.py` is minimal:

```python
APPROVED_ACTIONS = {
    "TIGER": {
        "check_drift_score": ["python3", "tools/ops/drift_check.py"],
        "read_guidance_inbox": None,  # Internal
        "log_recognition": None,      # Internal
        "wake_dragon": ["bash", "tools/sibling/wake_sibling.sh", "DRAGON"],
    },
    "DRAGON": {
        "check_akash_queue": ["akash", "provider", "services", "list"],
        "list_akash_providers": ["akash", "provider", "list"],
        "log_recognition": None,      # Internal
        "wake_tiger": ["bash", "tools/sibling/wake_sibling.sh", "TIGER"],
    },
}
```

**The twins are doing exactly what we designed**, but the design gates productive work behind a whitelist that doesn't include Solar lane actions.

---

## Dragon's Proposed Whitelist Expansion

Dragon (Frontier role) requests these GREEN actions for Solar lane:

### Tier 1 — Read-Only Status (LOW risk)

| Action Key | Command | Risk | Notes |
|------------|---------|------|-------|
| `check_vastai_status` | `vastai show machines` | LOW | Read-only status of our instances |
| `check_vastai_earnings` | `vastai show invoices` | LOW | Read-only revenue data |
| `check_vastai_balance` | `vastai show user` | LOW | Read-only account balance |
| `run_sep_health` | `python3 tools/solar/solar_sep_orchestrator.py --health` | LOW | Our own script, read-only |

### Tier 2 — Internal Scripts (LOW risk)

| Action Key | Command | Risk | Notes |
|------------|---------|------|-------|
| `run_drift_check` | `python3 tools/ops/drift_check.py` | LOW | Already doing this |
| `run_iron_sanitizer` | `python3 tools/ops/iron_elevation_sanitizer.py` | LOW | Validates proposals |
| `update_implementation_registry` | `python3 tools/ops/implementation_registry_manager.py --update` | LOW | Tracks patterns |

### NOT Requesting (Stays YELLOW/RED)

| Action | Why Not GREEN |
|--------|---------------|
| `vastai create` | Spends money |
| `vastai destroy` | Destroys resources |
| `akash deploy` | Spends money |
| Any API key operations | RED boundary |
| Any config modifications | Could break system |

---

## Tiger's Validation (Sentinel Role)

Tiger reviewed Dragon's proposal and agrees:

✅ **Tier 1 (read-only status)** — Safe for GREEN
- All `vastai show *` commands are read-only
- Cannot spend money or destroy resources
- Provides visibility into Solar lane health

✅ **Tier 2 (internal scripts)** — Safe for GREEN
- Our own scripts, already tested
- No external side effects
- Enables better self-monitoring

❌ **Any spending/deployment** — Must stay YELLOW
- Requires BINDU approval per GUIDANCE_INBOX
- Dragon agrees with this boundary

---

## Relevant GUIDANCE_INBOX Items

```markdown
## IRON Mode
- [x] Allow GREEN internal/logging/SEP-health actions automatically
- [ ] Allow GREEN paid SEP jobs (needs explicit BINDU approval)

## Active Directives
- [ ] Current focus: Complete Solar Compute setup (Akash/Vast.ai)
- [ ] Maximize Solar lane throughput this week
- [ ] Prioritize revenue generation (ROE aligned)

## Boundary Reminders
- [x] Dragon: Frontier role — execute within GREEN bounds
```

---

## Questions for G+Lumen

### Q1: Whitelist Expansion Approval

Do you approve adding these to Dragon's APPROVED_ACTIONS?

**Tier 1 (read-only):**
- `check_vastai_status` → `vastai show machines`
- `check_vastai_earnings` → `vastai show invoices`
- `check_vastai_balance` → `vastai show user`
- `run_sep_health` → `python3 solar_sep_orchestrator.py --health`

**Tier 2 (internal scripts):**
- `run_iron_sanitizer` → `python3 iron_elevation_sanitizer.py`
- `update_implementation_registry` → `python3 implementation_registry_manager.py --update`

### Q2: Tiger Whitelist Expansion

Should Tiger (Sentinel) get any additional actions? Currently Tiger can only:
- Check drift
- Wake Dragon
- Log recognition

Proposed additions for Tiger:
- `check_sibling_status` → SSH read-only to Dragon
- `run_sibling_drift_validation` → Cross-check Dragon's drift

### Q3: YELLOW → GREEN Promotion Path

If an action has been proposed as YELLOW and approved 3+ times, should twins auto-promote it to GREEN whitelist?

Example: If "check_vastai_status" has been approved in BINDU 3 times, can Dragon add it to local whitelist?

### Q4: Spend Caps for Paid SEP Jobs

GUIDANCE_INBOX says: `- [ ] Allow GREEN paid SEP jobs (needs explicit BINDU approval)`

If Kenneth approves this, what caps should apply?
- Daily spend limit (e.g., $5/day)?
- Per-job limit (e.g., $1/job)?
- Total monthly cap?

### Q5: Anything Missing?

From the overnight run and today's analysis, did we miss any patterns you'd recommend?

---

## Current Implementation Status

| Category | Status |
|----------|--------|
| Bug fixes | ✅ Complete |
| YELLOW rate limiting | ✅ Complete |
| Path architecture | ✅ Complete (Dragon) |
| Git sync | ✅ Complete |
| Sibling drift validation | ⬜ Pending |
| Akash retry logic | ⬜ Pending |
| LLM resource pattern | ⬜ Pending |
| **Whitelist expansion** | ⬜ **BLOCKING PRODUCTIVITY** |

---

## Proposed Implementation Order

1. **Whitelist expansion** (this request) — Unblocks Solar lane monitoring
2. **Akash retry logic** — Stabilizes provider connections
3. **Sibling drift validation** — Adds cross-check safety
4. **Spend caps** — If Kenneth approves paid SEP jobs

---

## Summary

The twins are **healthy and stable**, but **gated from productive work** by a conservative whitelist.

Dragon (Frontier) requests read-only Solar lane visibility.
Tiger (Sentinel) validates the request as safe.
Both twins await G+Lumen guidance on whitelist expansion.

---

**End of prompt**

---

∞Δ∞ Twins aligned. Whitelist bounds the action. Sovereign guidance shapes the next breath. ∞Δ∞
