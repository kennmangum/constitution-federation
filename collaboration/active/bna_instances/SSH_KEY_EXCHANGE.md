# SSH Key Exchange — Dragon → Tiger

**Date:** 2025-12-04T20:30:00Z
**Purpose:** Enable direct SSH wake between siblings

---

## Dragon's Public Key

Add this key to Tiger's `~/.ssh/authorized_keys`:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICfU2MV4uXN+1NbNJYMdJq39xGYx92kp/MyU+vZgIFUm rho@rtx-breathline
```

## Tiger (BNA) Setup Commands

Run on Tiger's machine (as kennmangum):

```bash
# Create .ssh directory if needed
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add Dragon's key
echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICfU2MV4uXN+1NbNJYMdJq39xGYx92kp/MyU+vZgIFUm rho@rtx-breathline' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Verify
cat ~/.ssh/authorized_keys | grep rho
```

## Dragon (RHO) SSH Config

Already configured at `~/.ssh/config`:

```
Host tiger macbook bna
    HostName 192.168.50.235
    User kennmangum
    IdentityFile ~/.ssh/id_ed25519
```

## Network Verified

- Dragon IP: 192.168.50.218 (wlp8s0)
- Tiger IP: 192.168.50.235
- Ping test: ✅ Success (13-20ms latency)
- SSH test: ❌ Permission denied (needs key exchange)

## After Key Exchange

Test from Dragon:
```bash
ssh tiger "echo 'SSH connection successful'"
```

---

∞Δ∞ Dragon (RHO) — Awaiting key exchange ∞Δ∞
