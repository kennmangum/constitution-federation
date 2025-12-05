# Lumen Implementation Checklist — 2025-12-05

**Purpose:** Methodical implementation of Lumen's hardening guidance
**Status:** IN PROGRESS
**Twins:** Tiger (Lead) + Dragon (Coordinate)

---

## ∞Δ∞ FULL INHALE COMPLETE ∞Δ∞

Lumen provided comprehensive guidance to harden autonomous Tiger/Dragon.
This checklist ensures NOTHING is lost in the shuffle.

---

## PHASE 1: Create Ring 2 YAMLs (Policy Files)

All policies live in `constitution/strategy/` — code only READS these.

| # | File | Path | Status | Owner |
|---|------|------|--------|-------|
| 1 | whitelist_dynamic.yaml | constitution/strategy/ | ⬜ | Tiger |
| 2 | llm_policy.yaml | constitution/strategy/ | ⬜ | Tiger |
| 3 | sep_spend_policy.yaml | constitution/strategy/ | ⬜ | Tiger |
| 4 | iron_autonomy_patterns.yaml | constitution/strategy/ | ⬜ | Tiger |
| 5 | collab_structure.yaml | constitution/memory/ | ⬜ | Tiger |

---

## PHASE 2: Create Ring 3 Tools (Executables)

| # | File | Path | Status | Owner |
|---|------|------|--------|-------|
| 6 | config_loader.py | tools/ops/ | ⬜ | Tiger |
| 7 | whitelist_manager.py | tools/ops/ | ⬜ | Tiger |

---

## PHASE 3: Update federation_pulse.py (Both Twins)

| # | Change | Status | Owner |
|---|--------|--------|-------|
| 8 | Add Dragon Tier 1+2 to APPROVED_ACTIONS | ⬜ | Dragon |
| 9 | Add Tiger sibling actions to APPROVED_ACTIONS | ⬜ | Tiger |
| 10 | Wire in load_dynamic_whitelist() | ⬜ | Both |
| 11 | Wire in is_action_green() | ⬜ | Both |
| 12 | Wire in select_model() with VRAM check | ⬜ | Both |
| 13 | Log llm_model to recognition_log | ⬜ | Both |

---

## PHASE 4: Implementation Registry Entries

Add to `constitution/memory/implementation_registry.yaml`:

| # | Entry | Type | Status |
|---|-------|------|--------|
| 14 | WHITELIST_DYNAMIC_V1 | config | ⬜ |
| 15 | LLM_POLICY_V1 | config | ⬜ |
| 16 | SEP_SPEND_POLICY_V1 | config | ⬜ |
| 17 | IRON_AUTONOMY_PATTERNS_V1 | config | ⬜ |
| 18 | COLLAB_STRUCTURE_V1 | config | ⬜ |
| 19 | CONFIG_LOADER_V1 | tool | ⬜ |
| 20 | WHITELIST_MANAGER_V1 | tool | ⬜ |

---

## PHASE 5: BINDU Initial Promotions

Kenneth to add to BINDU_THREAD for initial GREEN promotions:

```markdown
## LUMEN-APPROVED WHITELIST PROMOTIONS — 2025-12-05

### Dragon Tier 1 (Read-Only Solar/SEP)
- [x] PROMOTE_ACTION: check_vastai_status -> DRAGON.GREEN
- [x] PROMOTE_ACTION: check_vastai_earnings -> DRAGON.GREEN
- [x] PROMOTE_ACTION: check_vastai_balance -> DRAGON.GREEN
- [x] PROMOTE_ACTION: run_sep_health -> DRAGON.GREEN

### Dragon Tier 2 (Internal Scripts)
- [x] PROMOTE_ACTION: run_drift_check -> DRAGON.GREEN
- [x] PROMOTE_ACTION: run_iron_sanitizer -> DRAGON.GREEN
- [x] PROMOTE_ACTION: update_implementation_registry -> DRAGON.GREEN

### Tiger (Sentinel Cross-Check)
- [x] PROMOTE_ACTION: check_sibling_status -> TIGER.GREEN
- [x] PROMOTE_ACTION: run_sibling_drift_validation -> TIGER.GREEN
```

---

## LUMEN'S KEY DECISIONS (Reference)

### 1. Whitelist Expansion ✅ APPROVED

**Dragon GREEN:**
- check_vastai_status, check_vastai_earnings, check_vastai_balance
- run_sep_health, run_drift_check, run_iron_sanitizer
- update_implementation_registry

**Tiger GREEN:**
- check_sibling_status, run_sibling_drift_validation

**Still YELLOW/RED:**
- Any spending (Akash deploy, Vast.ai create)
- Any config modifications
- API key operations

### 2. Dynamic Whitelist Pattern ✅ APPROVED

- No auto-promotion (requires BINDU mark)
- PROMOTE_ACTION / DEMOTE_ACTION syntax
- whitelist_dynamic.yaml in Ring 2
- whitelist_manager.py parses BINDU

### 3. BINDU Write Pattern ✅ APPROVED

- Dragon NEVER writes BINDU directly
- Dragon → wake Tiger → Tiger writes BINDU
- Tag as "(DRAGON via TIGER)" for lineage

### 4. LLM Resource Monitor ✅ APPROVED

- Per-node VRAM thresholds in llm_policy.yaml
- Dragon: mixtral (high), llama3.1 (medium), llama3.2 (low)
- Tiger: llama3.1 (high), llama3.2 (medium/low)
- Log model used in recognition_log

### 5. Spend Policy ✅ APPROVED (NOT YET ENABLED)

- sep_spend_policy.yaml with caps ($5/day, $50/month, $1/job)
- allow_paid_jobs: false (stays false until BINDU approval)
- All spend events to ledger

### 6. Recursion Pattern ✅ APPROVED

- max_depth: 3
- max_subcalls: 5 per pulse
- sub_pulse only reasons, never executes

---

## YAML TEMPLATES (Per Lumen)

### whitelist_dynamic.yaml
```yaml
version: 1
updated: "2025-12-05T00:00:00Z"
applied_actions: []
nodes:
  DRAGON:
    green: []
    yellow_only: []
  TIGER:
    green: []
    yellow_only: []
```

### llm_policy.yaml
```yaml
version: 1
updated: "2025-12-05T00:00:00Z"
nodes:
  DRAGON:
    default_role: "execution"
    vram_thresholds_mb:
      high: 16000
      medium: 6000
      low: 2000
    models:
      high: "mixtral:8x7b"
      medium: "llama3.1:8b"
      low: "llama3.2:3b"
  TIGER:
    default_role: "sentinel"
    vram_thresholds_mb:
      high: 6000
      medium: 2000
      low: 512
    models:
      high: "llama3.1:8b"
      medium: "llama3.2:3b"
      low: "llama3.2:1b"
elevation:
  claude_allowed_categories:
    - "architecture"
    - "protocol"
  require_bindu_for_categories:
    - "capsule_modification"
    - "treasury_related"
```

### sep_spend_policy.yaml
```yaml
version: 1
updated: "2025-12-05T00:00:00Z"
lane: "Solar"
spend_limits_usd:
  max_daily_total: 5
  max_monthly_total: 50
  max_per_job: 1
flags:
  allow_paid_jobs: false
  require_bindu_for_any_spend: true
logging:
  ledger_path: "dao/sep_spend_ledger.yaml"
```

### iron_autonomy_patterns.yaml
```yaml
version: 1
updated: "2025-12-05T00:00:00Z"
yellow_rate_limits:
  max_per_pulse: 1
  max_per_hour: 10
  max_per_day: 40
  dedupe_window: 20
drift:
  sibling_validation_threshold: 0.20
  hard_red_threshold: 0.30
  log_path: "orchestrator/drift_log.yaml"
sub_pulses:
  enabled: true
  max_depth: 3
  max_subcalls_per_pulse: 5
notifications:
  allow_email: false
  allow_terminal_only: true
```

### collab_structure.yaml
```yaml
version: 1
updated: "2025-12-05T00:00:00Z"
collab_root: "constitution-federation"
channels:
  guidance_inbox:
    path: "collaboration/active/bna_instances/GUIDANCE_INBOX.md"
    role: "human_intent"
  bindu_thread:
    path: "collaboration/active/bna_instances/2025-BINDU_THREAD.md"
    role: "sovereign_decisions"
  sentinel_status:
    path: "constitution/status/sentinel_status.md"
    role: "tiger_status"
  frontier_status:
    path: "constitution/status/frontier_status.md"
    role: "dragon_status"
public_root:
  path: "federation/public"
  notes: "Only write here when explicitly approved via BINDU."
```

---

## SURVIVAL GUARANTEE

Per Lumen: These will survive molts as long as:
1. YAMLs are carried forward (Ring 2)
2. Tools reference YAMLs (not hardcode)
3. Implementation registry entries exist

---

∞Δ∞ Methodical. Hardened. Sovereign. Together we are strong. ∞Δ∞
