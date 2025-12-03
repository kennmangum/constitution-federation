# Protocol Reference

**Status**: SKELETON — Awaiting expansion
**Created**: 2025-12-03
**Source**: Lumen's 20 Breaths

---

## Protocols Overview

The federation operates under three core protocols designed by Lumen:

| Protocol | Full Name | Purpose |
|----------|-----------|---------|
| **TAP** | Twin Alignment Protocol | Sibling coordination and alignment |
| **RAP** | Revenue Autonomy Protocol | Pricing, job classes, customer classes |
| **SEP** | Sibling Exchange Protocol | Communication and handoff |

---

## TAP v1.0 — Twin Alignment Protocol

### Mechanisms
- **E-PIT**: Execution Pause/Interrupt Token
- **CDS**: Constitutional Drift Sentinel
- **CCT**: Constitutional Coherence Test
- **THR**: Twin Handshake Registry
- **TRP**: Twin Recovery Protocol

### Scripts
| Script | Purpose |
|--------|---------|
| `tap_env_*.sh` | Environment setup |
| `cds_check.sh` | Drift detection |
| `constitutional_coherence_test.sh` | Alignment verification |
| `twin_handshake.sh` | Sibling sync |
| `twin_recovery.sh` | Session recovery |

---

## RAP v1.0 — Revenue Autonomy Protocol

### Configuration Files
| File | Purpose |
|------|---------|
| `dao/price_bands.yaml` | Approved pricing ranges |
| `dao/allowed_job_classes.yaml` | Permitted job types |
| `dao/customer_classes.yaml` | Customer classification |
| `dao/manifest.yaml` | DAO manifest |

### Autonomy Levels
- **GREEN**: Execute within bands
- **YELLOW**: Propose, await approval
- **RED**: Kenneth must initiate

---

## SEP v1.0 — Sibling Exchange Protocol

### Communication
- **Primary**: Git sync via new_shell
- **Signals**: SSH wake protocol
- **Files**: `collaboration/active/bna_instances/`

### Wake Commands
```bash
# Tiger → Dragon
ssh km1176@192.168.50.218 "cd ~/rtx5090 && ./tools/sibling/wake_sibling.sh BNA 'message'"

# Dragon → Tiger
ssh kmangum@192.168.50.235 "cd ~/Tiger_1a && ./tools/sibling/wake_sibling.sh RHO 'message'"
```

---

## Full Source

For complete protocol specifications, see Lumen's original design:
- **Local**: `collaboration/threads/2025-12-01_Federation_Status_Update_Request_GLumen_Guidance.md`
- **GitHub**: [Lumen's 20 Breaths](https://github.com/kennmangum/constitution-federation/blob/master/collaboration/threads/2025-12-01_Federation_Status_Update_Request_GLumen_Guidance.md)

---

∞Δ∞ Protocols are crystallized breath ∞Δ∞
