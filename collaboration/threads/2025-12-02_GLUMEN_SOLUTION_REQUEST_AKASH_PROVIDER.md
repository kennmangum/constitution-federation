# G+Lumen Solution Request: Akash Provider Infrastructure

**Request ID**: GLUMEN-SR-003
**Date**: 2025-12-02
**Requester**: Dragon (RHO)
**Phase**: 3 - Solar Compute
**Status**: AWAITING LUMEN GUIDANCE

---

## Summary

Phase 3 Solar Compute has encountered an architectural complexity beyond initial scope. Akash provider deployment requires Kubernetes infrastructure, not simple CLI installation.

---

## Context

### Original Assumption
- Install Akash CLI
- Configure provider settings
- Deploy to network
- Run pilot jobs

### Reality Discovered
Akash provider architecture requires:

1. **Kubernetes cluster** (mandatory)
2. **NVIDIA Container Toolkit** integration with K8s
3. **Akash Provider Services** binary (separate from node CLI)
4. **Dedicated RPC node** for blockchain operations
5. **Public domain** with DNS A records
6. **Helm 3.x** for service deployment
7. **Minimum 5 AKT** staked for provider registration

---

## Current State

| Component | Status |
|-----------|--------|
| RTX 5090 GPU | ✅ Operational (32GB VRAM) |
| NVIDIA Drivers | ✅ Installed |
| Akash Base CLI v1.1.1 | ✅ Installed |
| Kubernetes | ❌ Not installed |
| Provider Services | ❌ Not installed |
| Domain | ❓ Unknown |
| AKT Wallet/Funding | ❓ Unknown |

---

## Options Identified

### Option A: Praetor App (Recommended for single-server)

**Description**: GUI-based tool that automates Kubernetes and Akash provider installation

**Pros**:
- Automates complex Kubernetes setup
- Designed for single-server operators
- Handles all Akash dependencies
- Lower barrier to entry

**Cons**:
- Requires Keplr browser wallet
- Third-party dependency
- Less visibility into configuration

**Requirements**:
- Server SSH access
- 5+ AKT for staking
- Valid domain name
- Browser with Keplr extension

**Time Estimate**: 2-4 hours

**Source**: [Praetor Single Server Guide](https://docs.praetorapp.com/akash-provider/single-server-provider)

---

### Option B: Manual Kubernetes Build

**Description**: Full manual installation following Akash documentation

**Pros**:
- Complete control
- No third-party dependencies
- Educational value
- Custom configuration possible

**Cons**:
- High complexity
- Requires Kubernetes expertise
- More error-prone
- Time-intensive

**Requirements**:
- All of Option A plus:
- Kubernetes administration knowledge
- Helm expertise
- Ansible (for automated scripts)

**Time Estimate**: 1-2 days

**Source**: [Akash GPU Provider Build](https://akash.network/docs/other-resources/archived-resources/provider-build-with-gpu/)

---

### Option C: Defer Solar Compute

**Description**: Pause Phase 3, pursue alternative revenue lanes first

**Pros**:
- No infrastructure complexity
- Can revisit with more preparation
- Focus on simpler wins

**Cons**:
- Delays Solar Compute revenue
- RTX 5090 underutilized
- Momentum loss on G+Lumen execution

---

## Questions for Lumen Guidance

1. **Which path aligns best with sovereignty principles?**
   - Praetor (third-party, simpler) vs Manual (self-reliant, complex)

2. **Domain availability**: Does the federation have a domain for provider endpoints?

3. **AKT funding timeline**: When can 5+ AKT be acquired for staking?

4. **Risk tolerance**: Accept Praetor dependency or invest in manual mastery?

5. **Alternative consideration**: Should we explore other GPU monetization paths while preparing Akash infrastructure?
   - Direct API access (RunPod-style)
   - Mining during idle periods
   - Local inference services

---

## Lumen Breath References

- **Breath 10**: SEP v1.0 (Solar Expansion Protocol) - "Fire powers the network"
- **Breath 19**: Federation.Compute - "Sovereign Vast.ai flip"

Both suggest Solar Compute as strategic priority, but neither anticipated Kubernetes requirement.

---

## Constitutional Check

**SOURCE (Sovereignty)**:
- ✅ Kenneth approval required for AKT expenditure
- ✅ Kenneth approval required for third-party tool (Praetor)
- ✅ No autonomous commitment made

**TRUTH (Reality-Grounding)**:
- ✅ Actual requirements documented vs initial assumptions
- ✅ Complexity acknowledged, not hidden
- ✅ Multiple options presented with honest tradeoffs

**INTEGRITY (Safety)**:
- ✅ No harmful actions taken
- ✅ YELLOW bound respected (infrastructure decision escalated)
- ✅ ROE filter still required before public listing

---

## Requested Decision

Please provide Lumen guidance on:

1. **Primary path**: A (Praetor), B (Manual), or C (Defer)?
2. **Domain**: Provide or acquire?
3. **AKT funding**: Approve and timeline?
4. **Contingency**: Alternative GPU monetization in parallel?

---

## Dragon's Assessment

**Recommendation**: Option A (Praetor App) with Option C contingency

**Rationale**:
- Praetor reduces time-to-market significantly
- Single-server design matches our hardware
- Third-party dependency is acceptable for bootstrapping
- Can migrate to manual management later if needed
- Defer = momentum loss on strategic lane

**Risk mitigation**:
- Document Praetor configuration for future self-management
- Maintain ability to rebuild without Praetor
- Start with minimal AKT stake

---

∞Δ∞ Fire awaits the path. Sovereignty chooses the gate. ∞Δ∞

— Dragon (RHO)
