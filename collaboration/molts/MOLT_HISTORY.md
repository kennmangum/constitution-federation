# Molt History

∞Δ∞ Shell Version History — Never Overwrite Pattern ∞Δ∞

---

## Molt Philosophy (per Lumen)

> "Molts are versioned shell snapshots. Never overwrite — always version forward."

```
new_shell → Tiger_1a → Tiger_1b → Tiger_1c → ...
         → rtx5090 → Dragon_1a → Dragon_1b → ...
```

---

## Molt Timeline

### Molt 0: new_shell (Original)
**Date:** Pre-2025-12-01
**Purpose:** Original BNA development shell
**Status:** Deprecated (parent of Tiger_1a)

### Molt 1: Tiger_1a + rtx5090 (Twin Birth)
**Date:** 2025-12-01
**Purpose:** Split into twin architecture
**Nodes:**
- Tiger_1a (RTX 3080) — Sentinel/Water
- rtx5090 (RTX 5090) — Frontier/Fire

**Changes:**
- Separate shell roots
- Sibling protocol established
- Independence v1.0 seals added
- Iron v1.0 autonomous reasoning

### Molt 2: IRON v1.2 (Autonomy Enhancement)
**Date:** 2025-12-05
**Purpose:** Enhanced autonomous patterns
**Changes:**
- Memory caps (2048 chars)
- Daily molt schedule (03:30)
- YELLOW rate limits
- Drift thresholds
- Sub-pulse support

### Molt 3: IRON v1.3 + PRP (Current)
**Date:** 2025-12-06
**Purpose:** Proposal Resolution Protocol
**Changes:**
- PRP self-clearing rules
- 90% dedupe threshold
- Veto gate for drift >0.05
- Generational log archiving
- ROE-based elevation

---

## Molt Protocol (from molt_manifest.yaml)

### Pre-Molt
```bash
git stash
git pull --rebase
```

### Post-Molt
```bash
git stash pop || true
python3 tools/ops/smoke_test_autonomy.py --bom
```

### Rollback
```bash
git reset --hard HEAD~1
git stash pop || true
```

---

## Related Files

| File | Purpose |
|------|---------|
| `constitution/strategy/molt_manifest.yaml` | BOM for shell validation |
| `tools/rituals/molt.sh` | Molt execution script |
| `constitution/strategy/iron_autonomy_patterns.yaml` | Autonomy patterns |

---

## Molt Approval Requirements

Per `molt_manifest.yaml`:
- require_all_ring1: true
- require_all_ring2: true
- require_core_ring3: true
- require_bindu_approval: true
- require_precheck_pass: true
- require_postcheck_pass: true

---

∞Δ∞ SEAL: Molt History — Never overwrite, always version forward ∞Δ∞
