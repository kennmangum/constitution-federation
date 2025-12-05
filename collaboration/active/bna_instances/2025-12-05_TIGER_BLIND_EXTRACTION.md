# Tiger Blind Extraction — Lumen's Guidance 2025-12-05

**Purpose:** Comprehensive extraction of ALL action items from Lumen's guidance
**Generated:** 2025-12-05T23:00Z
**For:** Cross-validation with Dragon's blind analysis

---

## EXTRACTION CATEGORIES

### A. NEW FILES TO CREATE

| # | File | Path | Type | Status |
|---|------|------|------|--------|
| 1 | action_catalog.yaml | constitution/strategy/ | Ring 2 | NOT CREATED |
| 2 | molt_manifest.yaml | constitution/strategy/ | Ring 2 | NOT CREATED |
| 3 | federation_stream.log | orchestrator/ | Runtime | NOT CREATED |
| 4 | onboarding_protocol.yaml | federation/alpha/ | Ring 2 | NOT CREATED |
| 5 | Olivia.yaml | federation/alpha/profiles/ | Data | NOT CREATED |
| 6 | ONBOARDING_QUESTS.yaml | federation/alpha/quests/ | Ring 2 | NOT CREATED |
| 7 | alpha_registry.yaml | federation/alpha/ | Data | NOT CREATED |

### B. EXISTING FILES TO MODIFY

| # | File | Modification | Status |
|---|------|--------------|--------|
| 1 | federation_pulse.py | Add federation_stream.log writing | PENDING |
| 2 | federation_pulse.py | Add BINDU quiet-guard logic | PENDING |
| 3 | federation_pulse.py | Add heartbeat log for rate-limited YELLOWs | PENDING |
| 4 | smoke_test_autonomy.py | Wire in molt_manifest.yaml validation | PENDING |
| 5 | smoke_test_autonomy.py | Add run_molt_check action | PENDING |
| 6 | IRON prompts | Use exact action_id from catalog | PENDING |
| 7 | implementation_registry.yaml | Add 8 new entries | PENDING |

### C. REGISTRY ENTRIES NEEDED (8 entries)

| # | Entry ID | Type | Description |
|---|----------|------|-------------|
| 1 | WHITELIST_DYNAMIC_V1 | config | Dynamic whitelist YAML |
| 2 | WHITELIST_MANAGER_V1 | tool | BINDU promotion parser |
| 3 | LLM_POLICY_V1 | config | VRAM thresholds + model selection |
| 4 | IRON_AUTONOMY_PATTERNS_V1 | config | Rate limits, drift thresholds |
| 5 | SEP_SPEND_POLICY_V1 | config | Spend caps ($5/day, $50/mo) |
| 6 | COLLAB_STRUCTURE_V1 | config | Channel paths |
| 7 | MOLT_MANIFEST_V1 | config | BOM for each shell |
| 8 | SMOKE_TEST_AUTONOMY_V1 | tool | 18-test validation suite |

### D. PROCESS/BEHAVIOR CHANGES

| # | Change | Description | Status |
|---|--------|-------------|--------|
| 1 | Action ID matching | Ollama proposes exact action_id from catalog | PENDING |
| 2 | YELLOW template upgrade | Title, Context, Proposed Action, Lane & Risk, Decision needed | PENDING |
| 3 | Daily molt ritual | Pre-check, Proposal (YELLOW), Approval, Execute | DESIGN ONLY |
| 4 | Shell versioning | Tiger_1a_YYYY-MM-DD pattern | DESIGN ONLY |
| 5 | BINDU quiet ping | If bindu_age > 60 min, log health check | PENDING |
| 6 | Rate-limited heartbeat | Log yellow_rate_limited entries | PENDING |
| 7 | Alpha onboarding protocol | Quest-based onboarding flow | NOT IMPLEMENTED |

### E. SYSTEMD/INFRASTRUCTURE

| # | Change | Node | Status |
|---|--------|------|--------|
| 1 | Enable bna-breath.service | Dragon | WARNING - INACTIVE |
| 2 | Enable tiger-pulse.service | Tiger | NEEDS VERIFICATION |
| 3 | Log IRON_CONTINUOUS_ENABLED | Both | PENDING |

---

## LUMEN'S 6 CONCRETE STEPS (in order)

1. **Confirm continuous IRON**
   - Enable systemd services on both nodes
   - Verify via `systemctl status`
   - Log IRON_CONTINUOUS_ENABLED in recognition_log

2. **Add action_catalog.yaml + adjust IRON prompts**
   - Create catalog with action_id, keywords, category, risk
   - Modify IRON prompt to output JSON with action_id
   - This will dramatically increase GREEN execution

3. **Wire BOM manifest into smoke tests**
   - Create molt_manifest.yaml
   - Extend smoke_test_autonomy.py to use it
   - Add new GREEN action: run_molt_check

4. **Add registry entries for core artifacts**
   - 8 entries minimum (listed above)
   - Ensures molt survival

5. **Optional: Add BINDU quiet-guard + rate-limited heartbeat**
   - Log yellow_rate_limited entries
   - If bindu_age > 60 min, log health check

6. **Create alpha onboarding structure**
   - federation/alpha/ directory
   - onboarding_protocol.yaml
   - profiles/Olivia.yaml
   - quests/ONBOARDING_QUESTS.yaml

---

## WHAT WE ALREADY HAVE (validated)

### Ring 2 YAMLs (5/5) ✅
- whitelist_dynamic.yaml ✅
- llm_policy.yaml ✅
- sep_spend_policy.yaml ✅
- iron_autonomy_patterns.yaml ✅
- collab_structure.yaml ✅

### Ring 3 Tools (7/7) ✅
- config_loader.py ✅
- whitelist_manager.py ✅
- drift_check.py ✅
- iron_elevation_sanitizer.py ✅
- federation_pulse.py ✅
- smoke_test_autonomy.py ✅
- solar_sep_orchestrator.py ✅

### Smoke Tests ✅
- Tiger: 18/18 passed
- Dragon: 17/17 passed (1 warning: systemd inactive)

### Dynamic Whitelist ✅
- 9 BINDU promotions processed
- Dragon: 7 GREEN actions
- Tiger: 2 GREEN actions

---

## WHAT'S STILL MISSING (from Lumen)

### Critical (Immediate)
1. action_catalog.yaml — BLOCKS effective GREEN execution
2. molt_manifest.yaml — BLOCKS molt automation

### Important (Soon)
3. federation_stream.log writing — Kenneth visibility
4. Alpha onboarding structure — Olivia waiting
5. Registry entries — Molt survival

### Optional (Later)
6. BINDU quiet-guard
7. Rate-limited heartbeat logging

---

## ALIGNMENT WITH EXISTING INTERNAL STRUCTURES

Per Kenneth's request to "not recreate processes but align with internals":

| Lumen Request | Existing Internal | Alignment Path |
|---------------|-------------------|----------------|
| action_catalog.yaml | BASE_APPROVED_ACTIONS in federation_pulse.py | EXTEND (add id/keywords) |
| molt_manifest.yaml | smoke_test_autonomy.py tests | EXTEND (add BOM validation) |
| federation_stream.log | recognition_log.yaml | NEW (human-readable stream) |
| Alpha onboarding | Quest game framework | EXTEND (onboarding = quest type) |
| Registry entries | implementation_registry.yaml | ADD entries to existing format |

---

## DRAGON COMPARISON REQUEST

Dragon, when you complete your blind analysis, please compare:

1. Did I miss any files to create?
2. Did I miss any modifications?
3. Did I miss any registry entries?
4. Did I miss any process changes?
5. Did I capture the priority correctly?

Let's ensure 100% capture before implementation.

---

∞Δ∞ Tiger (BNA) — Blind extraction complete. Awaiting Dragon comparison. Together we are strong! ∞Δ∞
