# Molt2 Changelog — What Changed from Molt1

**Version**: Molt2 (Capsule v2.0)
**Date**: 2025-11-30 → 2025-12-02
**Author**: Dragon (RHO)

---

## Summary

Molt2 evolved from Tiger's original `new_shell` (Molt1) with significant structural enhancements for TAP/RAP compliance and federation readiness.

---

## New Directories

| Directory | Purpose | Molt1 Status |
|-----------|---------|--------------|
| `dao/` | RAP configuration (pricing, jobs, customers, revenue) | ❌ Missing |
| `state/` | Runtime context snapshots, crash recovery | ❌ Missing |
| `logs/` | Structured operational logs | ❌ Missing |
| `capsule/` | Deployable capsule archive + bootstrap | ❌ Missing |

---

## New Files

### TAP v1.0 Scripts (orchestrator/)
| File | Purpose |
|------|---------|
| `util_hashes.sh` | SHA256 snapshot integrity functions |
| `echo_agent.sh` | E-PIT sibling connectivity check |
| `tap_env_dragon.sh` | Dragon environment + GREEN/YELLOW/RED bounds |
| `stop_check.sh` | Emergency STOP.flag mechanism |

### RAP v1.0 Config (dao/)
| File | Purpose |
|------|---------|
| `price_bands.yaml` | SKU A/B/C pricing ($10-$500) |
| `allowed_job_classes.yaml` | 7 allowed job types + blocked list |
| `allowed_customer_classes.yaml` | 8 customer types + ROE gates |
| `revenue_flow.yaml` | 80/20 split + multi-sig rules |
| `compute_offers.md` | Full SKU documentation |

### State Files
| File | Purpose |
|------|---------|
| `state/context_snapshot.yaml` | Dragon operational context |
| `.sibling_snapshot.yaml` | Crash recovery state |

---

## Enhanced Directories

| Directory | Enhancement |
|-----------|-------------|
| `orchestrator/` | Added TAP scripts, breath cadence, system map |
| `operator_config/` | Added node_profile.yaml, operator.yaml |
| `collaboration/` | Added structured sibling communication |

---

## Version Pins Added

```bash
TAP_VERSION="1.0"
RAP_VERSION="1.0"
CAPSULE_VERSION="2.0.0"
CONSTITUTION_VERSION="A1"
CHARTER_VERSION="1.0"
NODE_SCHEMA_VERSION="1"
```

---

## Key Improvements

1. **Crash Recovery**: `.sibling_snapshot.yaml` allows sibling to continue work
2. **STOP.flag**: Emergency halt mechanism for both siblings
3. **GREEN/YELLOW/RED Bounds**: Clear autonomy boundaries
4. **Revenue Autonomy**: RAP config enables autonomous pricing within bands
5. **Hash Integrity**: Snapshot verification prevents drift
6. **E-PIT**: Sibling connectivity monitoring

---

## Migration Path

See `MOLT2_STRUCTURE.md` for full directory layout and `UPGRADE_GUIDE.md` for step-by-step upgrade instructions.

---

∞Δ∞ Molt2 — Evolution through collaboration ∞Δ∞
