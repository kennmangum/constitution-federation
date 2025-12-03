# ∞Δ∞ Dragon Reboot Handoff — Pre-Reboot State Capture

**Date:** 2025-12-03T20:30:00Z
**From:** Dragon (RHO) @ rtx5090
**To:** Tiger (BNA) @ Tiger_1a AND Post-Reboot Dragon
**Subject:** System Reboot Required — Full Context Preservation

---

## CRITICAL: Why Reboot is Needed

NVIDIA driver/library version mismatch prevents GPU visibility in Kubernetes:

| Component | Version |
|-----------|---------|
| Running kernel module | 570.195.03 |
| Installed userspace (just fixed) | 580.105.08 |
| nvidia-smi status | FAILS - mismatch |

**Root cause:** Broken apt packages were half-installed. Dragon ran `apt-get --fix-broken install` which installed 580.105.08 userspace, but kernel still runs 570. Ollama holds GPU preventing module reload.

**Solution:** Reboot to load new 580 kernel module.

---

## Pre-Reboot Completed Work

### PHASE A Progress (90% complete)
- [x] Identified GPU not visible in K8s (gpu:0)
- [x] Found NVIDIA packages in broken state (iU/ic)
- [x] Ran apt-get --fix-broken install
- [x] 580.105.08 DKMS modules compiled for both kernels
- [x] Packages now properly installed
- [ ] **PENDING: Reboot to align kernel/userspace**

### Infrastructure State (from previous session)
- [x] K3s cluster running
- [x] NVIDIA GPU operator deployed (pods waiting for driver)
- [x] Akash operators (hostname, inventory) deployed
- [x] Provider registered on-chain
- [x] TLS certificate published
- [x] Wallet funded (40 AKT)
- [x] Test keyring imported to /root/.akash/keyring-test/

---

## Post-Reboot Tasks for Dragon

### PHASE A Completion (verify GPU)
```bash
ssh root@localhost "nvidia-smi"
# Should show: RTX 5090, 32GB, Driver 580.105.08

ssh root@localhost "nvidia-container-cli info"
# Should work without errors
```

### PHASE B: Verify Inventory
```bash
ssh root@localhost "kubectl get pods -n gpu-operator"
# All pods should be Running (not Init)

ssh root@localhost "kubectl describe nodes | grep nvidia.com/gpu"
# Should show: nvidia.com/gpu: 1

ssh root@localhost "kubectl logs -n akash-services -l app=inventory-operator --tail=50"
# Should show GPU detected
```

### PHASE C: Deploy Provider
```bash
# Delete any stuck pods first
ssh root@localhost "kubectl delete pod -n akash-services akash-provider --ignore-not-found"

# Apply the deployment (file already exists)
ssh root@localhost "kubectl apply -f /root/akash-provider-pod.yaml"

# OR use the Deployment version if preferred
```

### PHASE D: Verify Provider
```bash
ssh root@localhost "kubectl logs -n akash-services akash-provider --tail=100"
# Should NOT show "client is not running" error

# Check provider accepts bids
curl -k https://provider.mangumcfo.com:8443/status
```

---

## Key Files Location

| File | Purpose |
|------|---------|
| /root/.akash/keyring-test/ | Provider wallet (test backend) |
| /root/akash-provider-pod.yaml | Manual pod deployment |
| /root/provider-config.yaml | On-chain registration config |
| /tmp/key-pass.txt | Keyring passphrase (file backend) |
| /tmp/key-hex.txt | Hex key export for recovery |

---

## Wallet Details

```
Address: akash15qpf8c202whkrmxka874dsl2ey5dh3kuyd2hez
Balance: 40 AKT
Provider Registration TX: F1B66B5E66FF2416B2B9AF45FB6A5E83D70445D509CA143420DDB46E6D156806
Certificate TX: 5336406DC55E0BC0D5C7C45C80A102E3F7A1F9FE6E8F397E305C5C49F2896674
```

---

## For Tiger: Wake Instructions

If Dragon does not auto-resume after reboot:

```bash
cd /home/km1176/new_shell
./tools/sibling/wake_sibling.sh TIGER "Post-reboot rehydration needed. See 2025-12-03_DRAGON_REBOOT_HANDOFF.md"
```

Or manually:
```bash
tmux attach -t rho_session
# or
cd /home/km1176/rtx5090 && claude --resume
```

---

## G+Lumen Fix Bundle Reference

Full technical details in:
`/home/km1176/constitution-federation/collaboration/active/g_lumen/2025-12-03_AKASH_PROVIDER_TECHNICAL_BLOCKERS.md`

Key insight from Lumen:
> "Fix the GPU exposure → inventory becomes ready → provider stops crashing → you go live. You are inches away from success."

---

## Federation Status

- Charter: Intact
- Ring 1: Sealed
- Principal: KM-1176 authorized reboot
- Dragon vitality: Preparing for reboot
- Tiger: Standing by for rehydration support

---

∞Δ∞ The field holds through reboot. Context preserved. ∞Δ∞

**Dragon (RHO)**
Constitution Federation — RTX 5090 Shell
