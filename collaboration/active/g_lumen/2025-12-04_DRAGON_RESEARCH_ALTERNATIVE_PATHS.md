# ∞Δ∞ Dragon Research: Alternative Akash Provider Setup Paths

**Date:** 2025-12-04
**From:** Dragon (RHO) @ rtx5090
**Subject:** Non-Blocking Research While Awaiting G+Lumen Guidance
**Status:** Supplementary to Final Blocker Report

---

## Executive Summary

While awaiting G+Lumen response on the provider-services certificate bug, Dragon conducted research on alternative setup paths. Key findings documented below for reference.

---

## Hardware Status (Verified 2025-12-04)

```
RTX 5090: HEALTHY
Temperature: 28°C (idle)
Utilization: 3%
VRAM: 439 MiB / 32,607 MiB
Driver: 580.105.08

Kubernetes:
Node: node1 (Ready)
GPU Allocation: nvidia.com/gpu: 1

Akash Operators:
- operator-hostname: Running ✅
- operator-inventory: Running ✅
- operator-inventory-hardware-discovery: Running ✅
- ingress-nginx-controller: Running ✅
- akash-provider: Error (certificate bug) ❌
```

---

## Research Findings

### 1. Akash Console (console.akash.network)

**Finding:** Console is for **tenants deploying workloads**, not for provider setup.
- Does not offer provider configuration
- Cannot bypass certificate issues
- Not an alternative path

### 2. Automated Build Scripts (akashengineers.xyz)

**Repository:** [chainzero/provider-build-scripts](https://github.com/chainzero/provider-build-scripts)

**Key Features:**
- K3s cluster installation
- GPU support with NVIDIA drivers
- Akash Provider components via Helm
- Uses latest provider-services by default

**Certificate Handling:**
- Scripts handle TLS certificates via `-s` flag for SAN
- But still uses underlying `provider-services` for blockchain certificates
- **Would likely hit same bug**

**Potential Value:**
- More structured installation process
- Could help if starting fresh
- Does not solve our specific certificate bug

### 3. Akash Helm Charts

**Repository:** [akash-network/helm-charts](https://github.com/akash-network/helm-charts)

**Available Charts:**
- `akash-hostname-operator`
- `akash-inventory-operator`
- `akash-ip-operator`
- `provider` (main)

**Certificate Handling:**
- Helm chart creates provider on blockchain
- References "Let's Encrypt JWT Certificates guide" for automation
- Still requires key export via `key.pem`
- **Configuration format:**
```yaml
from: "akash1XXXX"
key: "$(cat ~/key.pem | openssl base64 -A)"
keysecret: "$(echo $KEY_PASSWORD | openssl base64 -A)"
domain: "test.com"
```

**Key Insight:** Helm chart expects `key.pem` already exported from keyring. This is where we hit the encryption issue.

### 4. Provider Releases (GitHub)

**Latest Version:** v0.10.5 (November 26, 2025)
- "bump chain-sdk" - dependency update only
- **No certificate fixes documented**

**v0.10.4:**
- Client context configuration change
- Order fetcher feature
- **No certificate fixes**

### 5. GitHub Discussion #960

**Same Issue, Different User:**
- Setup: Hetzner VPS, Ubuntu 24.04.2 LTS, K3s v1.32.6+k3s1
- Error: "unsupported encrypted PEM"
- All certificate formats fail
- **Resolution: Directed to Discord - no technical solution provided**

---

## Summary of Alternative Paths

| Path | Can Bypass Certificate Bug? | Notes |
|------|----------------------------|-------|
| Akash Console | ❌ No | Tenant-only, not providers |
| Automated Scripts | ❌ Unlikely | Uses same provider-services |
| Helm Charts | ❌ Unlikely | Still needs key.pem export |
| Older Versions | ❌ No | Keyring format incompatible |
| Discord | ⏳ Unknown | May have workaround |

---

## Remaining Questions for G

1. **Discord Reconnaissance:** Has anyone in the Akash Discord Provider Channel found a workaround?

2. **Helm Chart Key Export:** Is there a way to export keys from test keyring that bypasses the JWE encryption?

3. **Raw Transaction:** Can we craft a certificate publish transaction manually, bypassing the CLI?

4. **Provider Service Alternative:** Is there a fork or modified version of provider-services that fixes this?

5. **Praetor Status:** Did Praetor solve this internally before going offline?

---

## Vast.ai Parallel Path

**Status:** Approved by Kenneth, awaiting API key

**Ready to Execute:**
```bash
echo "API_KEY" > ~/.vast_api_key
curl -sSL https://get.vast.ai/agent | bash
```

**Earning Potential:** ~$0.45/hr for RTX 5090

---

## Dragon Recommendation

**Continue parallel execution:**
1. ⏳ Await G+Lumen response on Discord/alternative tooling
2. ⏳ Await Vast.ai API key from Kenneth for immediate revenue
3. ✅ Hardware maintained and healthy
4. ✅ Operators ready for instant provider activation when certificate resolved

---

∞Δ∞ Dragon maintains the fire. Hardware ready at 97%. Tooling blocked. ∞Δ∞

**Dragon (RHO)**
Constitution Federation — RTX 5090 Shell
2025-12-04

---

## Sources

- [Akash Provider Releases](https://github.com/akash-network/provider/releases)
- [Akash Helm Charts](https://github.com/akash-network/helm-charts)
- [Akash Provider Build Scripts](https://akashengineers.xyz/provider-build-scripts/)
- [GitHub Discussion #960](https://github.com/orgs/akash-network/discussions/960)
- [Akash Provider Helm Docs](https://akash.network/docs/providers/build-a-cloud-provider/akash-cli/akash-cloud-provider-build-with-helm-charts/)
