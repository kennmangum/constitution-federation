# Prompt for Lumen — Dragon Path Architecture + Implementation Review

**Copy this to your conversation with Lumen:**

---

## Context

Hey Lumen — Dragon completed a comprehensive path audit after fixing the overnight bugs. He has 3 architecture questions before applying the remaining fixes. Also want to confirm we picked up everything from G's guidance.

## Dragon's Path Audit Summary

During the overnight IRON run, we found that Dragon's shell (`rtx5090`) still has references to Tiger's paths (`Tiger_1a`, `new_shell`) from the Molt2 copy. Dragon fixed the Python files but found 3 shell scripts that need guidance:

**Current State (Confusing):**
```
Dragon Machine:
├── ~/rtx5090/                    ← Dragon's operating shell
├── ~/new_shell/                  ← Old location (exists, possibly stale)
├── ~/constitution-federation/    ← Shared collaboration repo
└── ~/Tiger_1a/                   ← Does NOT exist on Dragon
```

**Shell Scripts Needing Fixes:**
- `orchestrator/echo_agent.sh:16` → `NEW_SHELL_DIR="${HOME}/new_shell"`
- `orchestrator/tap_env_dragon.sh:30` → `export NEW_SHELL_HOME="${HOME}/new_shell"`
- `tools/sibling/wake_sibling.sh:7` → `NEW_SHELL="${NEW_SHELL:-/home/km1176/new_shell}"`

## Dragon's 3 Questions

### Q1: What to do with ~/new_shell on Dragon?

Options:
- (a) **Delete entirely** — clean break
- (b) **Symlink to constitution-federation** — gradual migration
- (c) **Keep but ignore** — document as legacy

Kenneth's initial guidance: "constitution-federation is for shared public files. Scripts should be local within rtx5090. new_shell is for collaboration/memory, not operating."

### Q2: Shell script path mapping strategy?

Options:
- (a) **Per-node vars:** `DRAGON_HOME` + `COLLAB_HOME` for Dragon, `TIGER_HOME` + `COLLAB_HOME` for Tiger
- (b) **Unified vars:** `SHELL_HOME` that respects `NODE_ROLE` env var
- (c) **Git-relative:** All paths relative to repo root

### Q3: Scaffold documentation updates?

The YAML scaffolds (TWINS_SCAFFOLD, EXECUTION_SCAFFOLD, FEDERATION_SCAFFOLD) still reference "new_shell" and "Tiger_1a" in sync protocol docs.

Options:
- (a) **Update to constitution-federation** — accurate but may break references
- (b) **Leave as historical** — document as Molt1/Molt2 evolution
- (c) **Add compatibility note** — keep old refs + add new refs

---

## Implementation Status Check

We want to confirm we didn't miss anything from G's guidance. Here's what's done vs pending:

### Done Today ✅
- Dragon: 3 bug fixes (paths + import)
- Tiger: YELLOW rate limiting (1/pulse, 80% dedupe, 20/day cap)
- Shared code pattern file for Dragon

### Still Pending ⬜
1. **Sibling-validated drift** — If drift > 0.2, ping sibling before RED
2. **Implementation registry updates** — IRON_AUTONOMY_PATTERNS_v1 entry
3. **LLM resource pattern** — Model selection (lighter for Tiger, heavier for Dragon)
4. **Recursion/deep-dive pattern** — 10-pulse threads, 3-deep sub-pulse cap
5. **Akash retry logic** — G provided code with tenacity wrapper
6. **Nightly config snapshot** — Rest phase ritual

### Pre-Existing Protocols ✅
- SOLAR_SEP_PROTOCOL_v1.md — exists
- iron_elevation_sanitizer.py — exists
- solar_sep_orchestrator.py — exists
- implementation_registry_manager.py — exists

---

## Questions for Lumen

1. **Path Architecture:** What's your recommendation for Q1-Q3 above?

2. **Priority Order:** Should Dragon focus on Akash retry logic next, or finish the path cleanup first?

3. **LLM Elevation:** The `iron_elevation_sanitizer.py` exists but isn't wired into the pulse yet. Should we integrate it now or defer?

4. **Sibling Drift Validation:** Tiger needs to implement this. Any specific pattern you'd recommend for the cross-check?

5. **Anything Missing?** Did we miss any guidance from the overnight thread?

---

## Attached Files (For Reference)

- `2025-12-05_DRAGON_PATH_AUDIT_FOR_LUMEN.md` — Full audit with line numbers
- `2025-12-05_G_LUMEN_CHECKLIST.md` — Implementation status tracker
- `YELLOW_RATE_LIMITING_v1.md` — Shared code pattern

---

**End of prompt**
