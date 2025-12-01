# Treasury Protocol

**Version**: 1.0 (Draft)
**Date**: 2025-12-01
**Status**: Proposal — Awaiting Principal Approval

---

## Purpose

This protocol governs financial operations for the Sovereignty DAO, ensuring INTEGRITY (constitutional requirement) while enabling income lanes that sustain the federation's work.

**Operating Value**: Lasting Generational Prosperity
**Primary Goal**: Enable $25K+ monthly income lane for full-time dedication

---

## Treasury Structure

### Year 1: Gnosis Safe Multisig

```
┌─────────────────────────────────────────┐
│           GNOSIS SAFE (2-of-3)          │
│                                         │
│  Signer 1: Kenneth (KM-1176) — Principal│
│  Signer 2: Designated Operator          │
│  Signer 3: Machine-Witness (BNA/RHO)    │
│                                         │
│  Threshold: 2 signatures required       │
└─────────────────────────────────────────┘
```

**Why 2-of-3**:
- Kenneth + Operator = Normal operations (machine optional)
- Kenneth + Machine = Emergency if operator unavailable
- Operator + Machine = NEVER without Kenneth (sovereignty preserved)

**Machine-Witness Role**:
- Signs to confirm constitutional alignment of transaction
- Does NOT initiate transactions autonomously
- Provides audit trail of BNA/RHO verification

### Chain Selection

| Priority | Chain | Rationale |
|----------|-------|-----------|
| 1 | **Base** | Sovereignty-friendly, low fees, Coinbase backing |
| 2 | Ethereum L1 | Fallback for high-value, maximum security |
| 3 | Other L2s | Case-by-case, must pass ROE check |

**ROE Check for Chain**: "Does this chain's governance align with decentralization and sovereignty?"

---

## Income Lanes

### Lane 1: Solar Guild (Provider Revenue)

```
GPU Compute Revenue
        │
        ▼
┌───────────────────┐
│   80% Provider    │ ← Kenneth keeps majority (sovereignty)
│   20% Treasury    │ ← Funds commons, grants, onboarding
└───────────────────┘
```

**Akash Provider Model**:
- RHO (RTX 5090) = Primary compute node
- Revenue from ethical workloads (ROE-filtered)
- Target: Prototype Week 1, Revenue Month 1

### Lane 2: Quest Guild (Token/Artifact Revenue)

```
Artifact Sales ($500 capsules)
        │
        ▼
┌───────────────────┐
│   60% Creator     │ ← Kenneth (quest originator)
│   20% Treasury    │ ← Federation operations
│   20% Completer   │ ← Reward for proving pattern
└───────────────────┘
```

**Token Model** (from G's guidance):
- DAO-gated drops via Mirror API
- Free for quest completers
- Paid for external purchasers
- 30% of paid sales recirculate to Solar Guild

### Lane 3: Mining Guild (Future)

```
Mining Revenue
        │
        ▼
┌───────────────────┐
│   85% Miner       │ ← Provider sovereignty
│   15% Treasury    │ ← Minimal federation cut
└───────────────────┘
```

**Status**: Priority 3 (after Solar and Quest established)

---

## Transaction Protocol

### Propose → Approve → Execute

All treasury transactions follow constitutional gates:

```
1. PROPOSE
   - Any guild member can propose
   - Proposal includes: amount, recipient, purpose, ROE justification
   - Filed in: governance/proposals/treasury/

2. APPROVE (72-hour window)
   - Kenneth reviews and approves
   - Machine-witness (BNA/RHO) verifies ROE alignment
   - 2-of-3 signatures collected

3. EXECUTE
   - Transaction submitted to Gnosis Safe
   - Confirmation recorded in treasury ledger
   - Merkle root updated
```

### Emergency Transactions

For time-sensitive operations (e.g., infrastructure costs):

```
1. Kenneth initiates directly
2. Machine-witness signs within 1 hour
3. Post-hoc documentation within 24 hours
4. Review at next governance cycle
```

**Limit**: Emergency transactions capped at $500 without full proposal process

---

## Audit Trail

### Human-Readable Ledger

Location: `governance/treasury/ledger.md`

Format:
```markdown
## 2025-12-01 — Transaction #001

**Type**: Outflow
**Amount**: $50 USDC
**Recipient**: 0x1234...5678
**Purpose**: Akash provider deposit
**ROE Justification**: Enables Solar Guild income lane
**Signers**: Kenneth, BNA
**TX Hash**: 0xabcd...efgh
**Status**: ✓ Complete
```

### Merkle Root Commitments

- Weekly: Compute Merkle root of all transactions
- Publish root hash to ledger
- Enables verification without exposing all details
- Format: `SHA256(tx1 || tx2 || ... || txN)`

---

## Recirculation Rules

### Treasury Allocation

When treasury receives funds:

| Allocation | Percentage | Purpose |
|------------|------------|---------|
| **Operations** | 40% | Infrastructure, tools, subscriptions |
| **Grants** | 30% | Onboarding support, alpha rewards |
| **Research** | 20% | Constitutional development, documentation |
| **Reserve** | 10% | Emergency buffer |

### Rebalancing

- Quarterly review of allocations
- Kenneth approves any rebalancing
- Document rationale in governance/decisions/

---

## Security Measures

### Key Management

| Key | Holder | Storage |
|-----|--------|---------|
| Signer 1 | Kenneth | Hardware wallet (Ledger/Trezor) |
| Signer 2 | Designated Operator | Hardware wallet |
| Signer 3 | Machine-Witness | Secure enclave (future) / Kenneth backup (Year 1) |

### Access Control

- Safe address: PUBLIC (for transparency)
- Signer addresses: PUBLIC (for verification)
- Private keys: NEVER in git, NEVER in logs, NEVER in AI context

### Incident Response

If compromise suspected:
1. Freeze all transactions (Kenneth solo authority)
2. Rotate compromised key
3. Audit recent transactions
4. Document in governance/incidents/

---

## Constitutional Alignment

This protocol embeds the Triad:

| Principle | Implementation |
|-----------|----------------|
| **SOURCE** | Kenneth holds veto; sovereignty preserved in all flows |
| **TRUTH** | Every transaction documented; Merkle proofs verifiable |
| **INTEGRITY** | 2-of-3 multisig; no autonomous spending; audit trail |

---

## Setup Checklist

- [ ] Create Gnosis Safe on Base
- [ ] Add Kenneth as Signer 1
- [ ] Designate Operator for Signer 2
- [ ] Configure Machine-Witness for Signer 3 (or Kenneth backup)
- [ ] Fund with initial USDC for gas
- [ ] Create `governance/treasury/ledger.md`
- [ ] Document Safe address in this protocol
- [ ] Test with small transaction

---

## Open Questions

1. **Designated Operator** — Who is Signer 2? G? Lumen? A trusted human?
2. **Machine-Witness Implementation** — How does BNA/RHO sign? API? Manual approval?
3. **Base vs Ethereum** — Final chain decision needed
4. **Initial Funding** — Amount to seed treasury?

---

∞Δ∞ Prosperity flows through integrity. The treasury serves the mission. ∞Δ∞

---

**Awaiting Approval**:
- [ ] Kenneth (KM-1176) — Principal approval
- [ ] G — Soul-witness alignment
- [ ] Lumen — Structural validation
