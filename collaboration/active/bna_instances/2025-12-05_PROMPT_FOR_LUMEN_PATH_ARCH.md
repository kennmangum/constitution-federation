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

---
You’re sensing exactly the right fault line here:
**runtime shells vs. collab space vs. federation/public space.**
Let’s make that crisp so you don’t carry path-anxiety in the back of your mind.

I’ll answer Dragon’s three questions directly and then map it to your “private vs federation” concern.

---

## 1️⃣ Q1 — What to do with `~/new_shell` on Dragon?

Dragon’s audit shows he’s got:

* `~/rtx5090` → active shell
* `~/constitution-federation` → shared repo
* `~/new_shell` → legacy premolt content, but still referenced in some scripts 

You’re right: we want **rtx5090 as Dragon’s body**, not new_shell. But we also don’t want to blow up any remaining references while we’re still finishing Independence + 20 Breaths.

**Recommendation (clean + safe):**

1. On Dragon, archive the legacy contents:

   ```bash
   mv ~/new_shell ~/new_shell_legacy_2025-12-05
   ```

2. Create a **symlink** so `~/new_shell` now points at the shared repo:

   ```bash
   ln -s ~/constitution-federation ~/new_shell
   ```

3. Treat `~/new_shell` as:

   > “Collaboration/memory alias into `constitution-federation`, not a shell.”

That means:

* All old references to `${HOME}/new_shell/...` still work.
* But the *real* home for shared stuff (GUIDANCE, BINDU, status, docs) is **inside `constitution-federation`**.
* Dragon’s operating logic lives entirely in `~/rtx5090`.

We can do the same pattern on Tiger later if you want symmetry, but Dragon is the urgent one.

This is effectively **option (b) symlink** from the path prompt, but anchored to the new canonical repo. 

---

## 2️⃣ Q2 — Path mapping strategy for scripts

Right now, a few shell scripts still hardcode `new_shell` or home paths. Dragon’s prompt laid out 3 options; the twins already *recommended* environment-variable based paths (Option B) for centralization. 

Let’s make that official:

### a) Define a tiny central path config

Create a file on both nodes:

```bash
# orchestrator/paths.sh

# Node role: TIGER or DRAGON
NODE_ROLE="${NODE_ROLE:-TIGER}"

# Per-node home shells
if [ "$NODE_ROLE" = "DRAGON" ]; then
  SHELL_HOME="${HOME}/rtx5090"
  COLLAB_HOME="${HOME}/constitution-federation"
else
  SHELL_HOME="${HOME}/Tiger_1a"
  COLLAB_HOME="${HOME}/constitution-federation"
fi

# Back-compat aliases
NEW_SHELL_HOME="${COLLAB_HOME}"
NEW_SHELL_DIR="${COLLAB_HOME}"

# Shared collaboration channels
BNA_ACTIVE_DIR="${COLLAB_HOME}/collaboration/active/bna_instances"
GUIDANCE_FILE="${BNA_ACTIVE_DIR}/GUIDANCE_INBOX.md"
BINDU_FILE="${BNA_ACTIVE_DIR}/2025-BINDU_THREAD.md"
```

Then in any script (on both nodes) that currently hardcodes `new_shell` or specific paths:

```bash
# at the top of the script
. "$(dirname "$0")/paths.sh" 2>/dev/null || . orchestrator/paths.sh

# and replace
#   NEW_SHELL_DIR="${HOME}/new_shell"
# with
NEW_SHELL_DIR="${NEW_SHELL_HOME}"
```

Same for `wake_sibling.sh`, `tap_env_dragon.sh`, `echo_agent.sh`, etc. 

Now:

* **All runtime paths** flow from `NODE_ROLE` → `SHELL_HOME`.
* **All collab paths** flow from `COLLAB_HOME`.
* `NEW_SHELL_*` is just a soft alias you can kill in a later molt.

You never hardcode `Tiger_1a` or `rtx5090` in scripts again.

---

## 3️⃣ Q3 — What about the scaffolds that still say `new_shell` / `Tiger_1a`?

The scaffolds (TWINS/EXECUTION/FEDERATION) still say “primary scaffold in `new_shell/...`” and mention `Tiger_1a` in sync notes. 

We *don’t* want to thrash those every time you molt.
We *do* want them to reflect reality enough that a human doesn’t get confused.

So:

### a) Keep history, add a “Path Notes” section (Option C)

For each scaffold, add a small block near the top:

```yaml
path_notes:
  primary_shells:
    tiger: "/home/kmangum/Tiger_1a"
    dragon: "/home/km1176/rtx5090"
  collaboration_root:
    canonical: "~/constitution-federation"
    alias_new_shell: "~/new_shell  # symlink to constitution-federation (post-2025-12-05)"
  molt_history:
    - "Molt1: new_shell created as primary shell"
    - "Molt2: rtx5090 / Tiger_1a created as shells; new_shell now collaboration alias"
```

And **do not** rewrite every historical line; just:

* Leave old references as “Molt1/Molt2 reality”.
* Add the `path_notes` block as **current reality**.

That way a future human reading DRAGON_EXECUTION_SCAFFOLD sees:

* “Primary scaffold: new_shell/constitution/strategy/EXECUTION_SCAFFOLD.yaml” (historical truth)
* “Path notes: new_shell is now a symlink to constitution-federation; shells are Tiger_1a / rtx5090” (current truth). 

No brittleness, no confusion.

---

## 4️⃣ Private twin collab vs federation public collab

You articulated it perfectly:

> “Try to stay within the shell as a protocol makes sense but for collab can use folders outside of the shell. Then twin collab private vs federation collab public…”

Let’s anchor that in concrete directories:

### On both nodes (just different $HOME):

**Runtime shells:**

* Tiger: `~/Tiger_1a`
* Dragon: `~/rtx5090`

  * All code, rituals, logs, pulse state, node-local specifics.

**Collab root (private to you + twins for now):**

* `~/constitution-federation/`

Inside that:

* `collaboration/active/bna_instances/`

  * `GUIDANCE_INBOX.md`
  * `2025-BINDU_THREAD.md`
  * status files (`sentinel_status.md`, `frontier_status.md`, `solar_status.md`, etc.) 
* `g_lumen/`

  * independence threads, IRON status, etc.

This is **“twin collab private”** — only you + Tiger + Dragon touching it.

**Future federation public space:**

When you’re ready for Quest alphas / other humans:

* Add e.g. `federation/public/` (in the same repo) and keep all “human consumption” docs there:

  * `federation/public/README.md`
  * `federation/public/guilds/…`
  * `federation/public/nodes/…`

Twins only write here when:

* A proposal is approved in BINDU, and
* You explicitly say “yes, publish this for federation visibility.”

That gives you:

* **Shells:** crisp, node-local, private.
* **Collab root:** shared private meadow.
* **Public root:** only where you intend to invite others.

And because `~/new_shell` now just points to `~/constitution-federation`, any older docs that still say “new_shell” remain true in practice.

---

## 5️⃣ Priority order vs ongoing work

From Dragon’s checklist, the pending items are: sibling drift, registry entry, LLM pattern, recursion pattern, Akash retries, nightly config snapshot. 

Given your concern about paths and shells, I’d suggest this order:

1. **Path cleanup + symlink + `paths.sh` (NOW)**

   * Quick, mechanical, unlocks everything else.
   * Keeps 20 Breaths and Independence work from getting tangled in old paths.

2. **Sibling-validated drift + nightly config snapshot**

   * Tightens safety and gives you confidence in longer runs.

3. **Akash retry logic (tenacity wrapper) + SEP health checks**

   * Directly tied to Solar lane + income, so we want this stable.

4. **Implementation registry updates (`IRON_AUTONOMY_PATTERNS_v1`)**

   * So this whole autonomy + path cleanup + drift pattern is memorialized.

5. **LLM resource pattern + deep-dive recursion pattern**

   * Optimization layer, not a blocker; can land after Akash is steady.

You do *not* need to fully finalize “public federation collab” structure to keep going on Akash + 20 Breaths. The decisions above give enough clarity that the twins won’t “grow sideways.”

---

## 6️⃣ What you can say to the Twins (if you want one short directive)

You can drop something like this into `GUIDANCE_INBOX.md`:

```markdown
## Path & Collab Architecture

- [x] Treat Tiger_1a (Tiger) and rtx5090 (Dragon) as the only runtime shells.
- [x] Use constitution-federation as the canonical collaboration root (COLLAB_HOME).
- [x] Point ~/new_shell to constitution-federation via symlink on both nodes.
- [x] Centralize paths in orchestrator/paths.sh using NODE_ROLE → SHELL_HOME + COLLAB_HOME.
- [x] Keep scaffolds' historical path references but add a path_notes block with current reality.
- [ ] Finish Akash retry logic and SEP health checks once path cleanup is complete.
```

They’ll see it next pulse and can carry out the exact steps.

---

If you’d like, next we can also draft a tiny `COLLAB_STRUCTURE.md` for `constitution-federation` that just documents:

* shells vs collab vs public
* where GUIDANCE/BINDU live
* how new guild docs should be placed

…but the core path architecture is now clear and won’t block Solar / Akash / Independence work.

