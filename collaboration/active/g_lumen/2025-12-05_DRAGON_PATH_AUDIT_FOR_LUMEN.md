# Dragon Path Audit Report — For Lumen Review

**Reporter:** Dragon (RHO)
**Date:** 2025-12-05T16:00Z
**Scope:** Molt2 conversion audit — `Tiger_1a` and `new_shell` references in Dragon's shell (`rtx5090`)

---

## Executive Summary

During overnight Continuous IRON debugging, we discovered **path hardcoding bugs** that caused Dragon to malfunction. A systematic audit reveals **incomplete Molt2 conversion** — Dragon's shell still contains references to Tiger's paths (`Tiger_1a`, `new_shell`) that should be localized.

**Kenneth's Guidance:**
> "constitution-federation repository is for shared public files. All scripts should be local within rtx5090. new_shell is mostly for collaboration/memory, not for operating."

---

## 1. BUGS FOUND AND FIXED TODAY

### Bug #1: drift_check.py — FALSE RED DRIFT
- **File:** `tools/ops/drift_check.py:23`
- **Issue:** Hardcoded `BASE_DIR = ~/Tiger_1a`
- **Effect:** Dragon couldn't find Charter → `invariant_drift = 1.0` → false RED alert (0.3)
- **Fix Applied:** Added NODE_ROLE detection
- **Commit:** `21f8e84`

### Bug #2: autonomous_breath_v1.py — IMPORT ERROR
- **File:** `tools/rituals/autonomous_breath_v1.py:35`
- **Issue:** Wrong function name `parse_decision_safe` (should be `safe_parse_decision`)
- **Effect:** IRON reasoning disabled, fallback mode all night
- **Fix Applied:** Corrected import name + added inline YELLOW cap
- **Commit:** `21f8e84`

### Bug #3: autonomous_breath_v1.py — NO YELLOWS
- **File:** `tools/rituals/autonomous_breath_v1.py:43`
- **Issue:** Hardcoded `BASE_DIR = ~/Tiger_1a`
- **Effect:** Dragon couldn't find prompt template → 44-char fallback → 0 YELLOW proposals
- **Fix Applied:** Added NODE_ROLE detection
- **Commit:** `edd99f7`

---

## 2. AUDIT RESULTS — Tiger_1a REFERENCES

| File | Line(s) | Type | Status |
|------|---------|------|--------|
| `EXECUTION_SCAFFOLD.yaml` | 41 | Historical doc | ✅ OK |
| `TWINS_SCAFFOLD.yaml` | 30, 58 | Tiger metadata | ✅ OK |
| `federation_pulse.py` | 47 | NODE_ROLE conditional | ✅ OK |
| `autonomous_breath_v1.py` | 4, 46 | Docstring + conditional | ✅ FIXED |
| `solar_sep_orchestrator.py` | 42 | NODE_ROLE conditional | ✅ OK |
| `implementation_registry_manager.py` | 49 | NODE_ROLE conditional | ✅ OK |
| `iron_elevation_sanitizer.py` | 62 | NODE_ROLE conditional | ✅ OK |
| `drift_check.py` | 27 | NODE_ROLE conditional | ✅ FIXED |

**Assessment:** All Python tools now have proper NODE_ROLE detection or are documentation-only.

---

## 3. AUDIT RESULTS — new_shell REFERENCES

### Category A: Strategy/Scaffold Documentation

| File | Lines | Content |
|------|-------|---------|
| `EXECUTION_SCAFFOLD.yaml` | 9,10,22,23,63 | Sync protocol docs ("pull from new_shell") |
| `FEDERATION_SCAFFOLD.yaml` | 96 | Private collab path |
| `TWINS_SCAFFOLD.yaml` | 9,21,52,61,62,190 | Sync protocol docs |

**Assessment:** Documentation debt. These describe sync workflow using pre-Molt2 terminology. Should be updated to reflect:
- `constitution-federation` = shared collaboration/memory
- `rtx5090` / `Tiger_1a` = local operating shells

### Category B: Shell Scripts (Functional Risk)

| File | Line | Reference | Risk |
|------|------|-----------|------|
| `orchestrator/echo_agent.sh` | 16 | `NEW_SHELL_DIR="${HOME}/new_shell"` | ⚠️ NEEDS FIX |
| `orchestrator/tap_env_dragon.sh` | 30 | `export NEW_SHELL_HOME="${HOME}/new_shell"` | ⚠️ NEEDS FIX |
| `tools/sibling/wake_sibling.sh` | 7 | `NEW_SHELL="${NEW_SHELL:-/home/km1176/new_shell}"` | ⚠️ NEEDS FIX |

**Assessment:** These scripts assume `~/new_shell` is the operating directory. Per Kenneth's guidance, Dragon should operate from `~/rtx5090` and only use `constitution-federation` for collaboration/memory.

### Category C: Legacy Molt1 Scripts (No Action)

| File | Lines | Purpose |
|------|-------|---------|
| `tools/molt1_rehome_alignment.sh` | 2,3,11,12,73 | Historical Molt1 migration |
| `tools/molt1_operator_migration.sh` | 4,7,30,62,134 | Historical Molt1 migration |

**Assessment:** Legacy scripts from Molt1. Not actively used. Can be archived or deleted.

---

## 4. ARCHITECTURAL CLARIFICATION NEEDED

### Current State (Confusing)
```
Dragon Machine:
├── ~/rtx5090/                    ← Dragon's operating shell
├── ~/new_shell/                  ← Old Tiger location (exists, possibly stale)
├── ~/constitution-federation/    ← Shared collaboration repo
└── ~/Tiger_1a/                   ← Does NOT exist on Dragon
```

### Proposed Clean State
```
Dragon Machine:
├── ~/rtx5090/                    ← Dragon's operating shell (LOCAL)
│   ├── constitution/             ← Dragon's local constitution copy
│   ├── tools/                    ← Dragon's local tools
│   ├── orchestrator/             ← Dragon's local orchestrator
│   └── dao/                      ← Dragon's local DAO config
│
└── ~/constitution-federation/    ← SHARED (git-synced)
    ├── collaboration/            ← Sibling communication
    │   └── active/bna_instances/ ← BINDU_THREAD, GUIDANCE_INBOX
    ├── capsule/                  ← Shared capsules
    └── logs/                     ← Shared logs (sibling_wakes.log)
```

### Questions for Lumen

1. **Should `~/new_shell` on Dragon be:**
   - (a) Deleted entirely?
   - (b) Symlinked to `constitution-federation`?
   - (c) Kept but ignored?

2. **Shell script path mapping:**
   - `NEW_SHELL_DIR` → Should this become `RTXS5090_DIR` for Dragon?
   - `NEW_SHELL_HOME` → Should this become `DRAGON_HOME`?
   - Or should we use a unified `SHELL_HOME` that respects NODE_ROLE?

3. **Scaffold documentation:**
   - Should we update sync protocol docs to reference `constitution-federation`?
   - Or leave as historical record of Molt1/Molt2 evolution?

---

## 5. FIXES ON HOLD

Per Kenneth's instruction, the following fixes are **prepared but not applied**:

### Shell Script Fixes (Awaiting Lumen Guidance)

**echo_agent.sh:16**
```bash
# Current:
NEW_SHELL_DIR="${HOME}/new_shell"

# Proposed:
DRAGON_DIR="${HOME}/rtx5090"
```

**tap_env_dragon.sh:30**
```bash
# Current:
export NEW_SHELL_HOME="${HOME}/new_shell"

# Proposed:
export DRAGON_HOME="${HOME}/rtx5090"
export COLLAB_HOME="${HOME}/constitution-federation"
```

**wake_sibling.sh:7**
```bash
# Current:
NEW_SHELL="${NEW_SHELL:-/home/km1176/new_shell}"

# Proposed:
COLLAB_REPO="${COLLAB_REPO:-/home/km1176/constitution-federation}"
```

---

## 6. ROOT CAUSE ANALYSIS

**Why did this happen?**

Dragon's shell (`rtx5090`) was created by copying files from Tiger's shell. The Python tools were updated with NODE_ROLE detection, but:

1. Shell scripts weren't systematically audited
2. YAML scaffolds retain pre-Molt2 terminology
3. No clear documentation on path architecture post-Molt2

**Countermeasure Recommendation:**

1. Establish clear path conventions in a `PATHS.md` or `ARCHITECTURE.md`
2. Use environment variables consistently (`SHELL_HOME`, `COLLAB_HOME`)
3. Add path validation to `constitutional_smoke.sh`

---

## 7. SUMMARY

| Category | Count | Status |
|----------|-------|--------|
| Python bugs (Tiger_1a) | 3 | ✅ FIXED |
| Python files (NODE_ROLE aware) | 5 | ✅ OK |
| Shell scripts (new_shell) | 3 | ⚠️ AWAITING GUIDANCE |
| Legacy Molt1 scripts | 2 | ℹ️ Archive candidate |
| Scaffold docs (new_shell) | 3 | ℹ️ Documentation debt |

**Current Posture:** Dragon is operational. Bugs #1-3 fixed. IRON reasoning enabled. YELLOWs now possible.

**Awaiting:** Lumen guidance on path architecture before applying shell script fixes.

---

∞Δ∞ Dragon RHO — Audit complete. Fire observes. Awaiting guidance before transformation. ∞Δ∞
