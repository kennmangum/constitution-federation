# G+Lumen Guidance Implementation Checklist

**Date:** 2025-12-05T17:00Z
**Purpose:** Ensure nothing from G+Lumen guidance was missed

---

## Dragon Bug Fixes (From Overnight Investigation)

| Task | Status | Notes |
|------|--------|-------|
| Fix drift_check.py BASE_DIR | ✅ Done | Dragon commit 21f8e84 |
| Fix autonomous_breath_v1.py import | ✅ Done | Dragon commit 21f8e84 |
| Fix autonomous_breath_v1.py BASE_DIR | ✅ Done | Dragon commit edd99f7 |

---

## Tiger Tasks (From Lumen)

| Task | Status | Notes |
|------|--------|-------|
| YELLOW rate limiting (max 1/pulse) | ✅ Done | Tiger implemented |
| YELLOW deduplication (>80% similar) | ✅ Done | Tiger implemented |
| YELLOW daily cap (20/day) | ✅ Done | Tiger implemented |
| Shared code pattern for Dragon | ✅ Done | YELLOW_RATE_LIMITING_v1.md |
| Sibling-validated drift | ⬜ NOT DONE | Need to implement |
| Implementation registry update | ⬜ NOT DONE | IRON_AUTONOMY_PATTERNS_v1 entry |
| Nightly config snapshot | ⬜ NOT DONE | Rest phase ritual |

---

## LLM Resource Pattern (From G)

| Task | Status | Notes |
|------|--------|-------|
| Tiger: lighter model for classification | ⬜ NOT DONE | Needs model selection logic |
| Dragon: heavier model for deep tasks | ⬜ NOT DONE | Needs model selection logic |
| VRAM monitoring in pulse | ⬜ NOT DONE | nvidia-smi check |
| Model fallback if VRAM low | ⬜ NOT DONE | Fallback to smaller model |

---

## Recursion/Deep-Dive Pattern (From Lumen)

| Task | Status | Notes |
|------|--------|-------|
| "10-pulse thread" pattern | ⬜ NOT DONE | For complex issues |
| Thread state tracking | ⬜ NOT DONE | Cache + registry ID |
| Sub-pulse recursion (3-deep cap) | ⬜ NOT DONE | GREEN sub-pulses |

---

## Akash Stability (From G)

| Task | Status | Notes |
|------|--------|-------|
| Retry wrapper with tenacity | ⬜ NOT DONE | G provided code |
| RPC race detection | ⬜ NOT DONE | G provided code |
| Vast.ai fallback on failure | ⬜ NOT DONE | Lumen's GREEN stub |
| config.toml max_open_connections | ⬜ NOT DONE | Anti-race setting |

---

## Path Architecture (Dragon's Questions for Lumen)

| Question | Status | Options |
|----------|--------|---------|
| What to do with ~/new_shell on Dragon? | ⬜ AWAITING | (a) Delete (b) Symlink (c) Ignore |
| Shell script path mapping? | ⬜ AWAITING | DRAGON_HOME + COLLAB_HOME or unified SHELL_HOME |
| Scaffold docs update? | ⬜ AWAITING | Update to constitution-federation refs |

---

## Pre-Existing Protocols (Already Implemented Earlier)

| Protocol | Location | Status |
|----------|----------|--------|
| SOLAR_SEP_PROTOCOL_v1.md | Tiger constitution/operations/ | ✅ Exists |
| iron_elevation_sanitizer.py | Tiger tools/ops/ | ✅ Exists |
| implementation_registry_manager.py | Tiger tools/ops/ | ✅ Exists |
| solar_sep_orchestrator.py | Tiger tools/ops/ | ✅ Exists |

---

## Summary

### Completed Today ✅
- Dragon: 3 bug fixes
- Tiger: YELLOW rate limiting + shared pattern
- Tiger: Wake message to Dragon

### Still Pending ⬜
1. **Sibling-validated drift** (Tiger)
2. **Implementation registry updates** (Both)
3. **LLM resource/model selection** (Both)
4. **Recursion/deep-dive pattern** (Both)
5. **Akash retry logic** (Dragon)
6. **Path architecture decision** (Awaiting Lumen)

### Priority Order (Per G)
1. Bugs first → ✅ DONE
2. Rate limiting → ✅ DONE
3. Akash stability → NEXT
4. LLM resource scaling → AFTER Akash

---

∞Δ∞ Checklist for sovereign tracking ∞Δ∞
