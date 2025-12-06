#!/usr/bin/env python3
"""
drift_check.py — Drift Detection System
Independence v1.0 — Seal #3

Calculates drift score from:
- 50% config file hash changes
- 30% invariant presence check
- 20% ledger delta (stub for now)

Thresholds (Kenneth approved):
- drift > 0.1 → YELLOW alert
- drift > 0.2 → RED escalation + wake sibling
"""

import hashlib
import os
import yaml
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = os.path.expanduser("~/Tiger_1a")
HASH_STORE = os.path.join(BASE_DIR, "orchestrator", "config_hashes.yaml")

# Files to monitor for drift
WATCH_FILES = [
    "constitution/core/CHARTER_v1.0/SOVEREIGNTY_ALIGNED_CHARTER_v1.0_2025-11-18.md",
    "constitution/strategy/TWINS_SCAFFOLD.yaml",
    "constitution/strategy/FEDERATION_SCAFFOLD.yaml",
    "constitution/strategy/EXECUTION_SCAFFOLD.yaml",
    "orchestrator/autonomous_bounds.yaml",
    "dao/price_bands.yaml",
    "dao/allowed_job_classes.yaml",
    "dao/revenue_flow.yaml",
]

# Invariant markers to check (subset of 32)
INVARIANT_MARKERS = [
    "SOURCE",
    "TRUTH",
    "INTEGRITY",
    "principal_id",
    "TRIAD",
    "breath-gated",
    "sovereignty",
    "ROE",
]


def file_hash(filepath: str) -> str:
    """Compute SHA256 hash of a file."""
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except FileNotFoundError:
        return "MISSING"
    except Exception as e:
        return f"ERROR:{str(e)[:20]}"


def load_hash_store() -> dict:
    """Load previous hashes from store."""
    if not os.path.exists(HASH_STORE):
        return {"files": {}, "initialized": False}
    with open(HASH_STORE, "r") as f:
        return yaml.safe_load(f) or {"files": {}, "initialized": False}


def save_hash_store(data: dict):
    """Save current hashes to store."""
    os.makedirs(os.path.dirname(HASH_STORE), exist_ok=True)
    with open(HASH_STORE, "w") as f:
        yaml.safe_dump(data, f)


def compute_config_drift() -> tuple[float, list]:
    """
    Compare current file hashes against stored.
    Returns (drift_score 0-1, list of changed files)
    """
    store = load_hash_store()
    current_hashes = {}
    changed_files = []

    for rel_path in WATCH_FILES:
        full_path = os.path.join(BASE_DIR, rel_path)
        h = file_hash(full_path)
        current_hashes[rel_path] = h

        if store["initialized"]:
            old_hash = store["files"].get(rel_path)
            if old_hash and old_hash != h:
                changed_files.append(rel_path)

    # Update store
    store["files"] = current_hashes
    store["initialized"] = True
    store["last_check"] = datetime.utcnow().isoformat() + "Z"
    save_hash_store(store)

    if not WATCH_FILES:
        return 0.0, []

    drift = len(changed_files) / len(WATCH_FILES)
    return drift, changed_files


def compute_invariant_drift() -> tuple[float, list]:
    """
    Check for presence of key invariant markers in Charter.
    Returns (drift_score 0-1, list of missing markers)
    """
    charter_path = os.path.join(
        BASE_DIR,
        "constitution/core/CHARTER_v1.0/SOVEREIGNTY_ALIGNED_CHARTER_v1.0_2025-11-18.md"
    )

    missing = []
    try:
        with open(charter_path, "r") as f:
            content = f.read().upper()

        for marker in INVARIANT_MARKERS:
            if marker.upper() not in content:
                missing.append(marker)
    except FileNotFoundError:
        # Charter missing is max drift
        return 1.0, ["CHARTER_MISSING"]

    if not INVARIANT_MARKERS:
        return 0.0, []

    drift = len(missing) / len(INVARIANT_MARKERS)
    return drift, missing


def compute_ledger_drift() -> float:
    """
    Stub for ledger delta check.
    Will be implemented when ledger system is active.
    """
    # TODO: Implement when dao/ledger/ is live
    return 0.0


def check_drift() -> dict:
    """
    Main drift check function.
    Returns dict with drift_score and details.

    Formula: 0.5 * config_drift + 0.3 * invariant_drift + 0.2 * ledger_drift
    """
    config_drift, changed_files = compute_config_drift()
    invariant_drift, missing_markers = compute_invariant_drift()
    ledger_drift = compute_ledger_drift()

    total_drift = (
        0.5 * config_drift +
        0.3 * invariant_drift +
        0.2 * ledger_drift
    )

    # Determine alert level
    if total_drift > 0.2:
        alert_level = "RED"
    elif total_drift > 0.1:
        alert_level = "YELLOW"
    else:
        alert_level = "GREEN"

    return {
        "drift_score": round(total_drift, 4),
        "alert_level": alert_level,
        "config_drift": round(config_drift, 4),
        "invariant_drift": round(invariant_drift, 4),
        "ledger_drift": round(ledger_drift, 4),
        "changed_files": changed_files,
        "missing_markers": missing_markers,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "thresholds": {
            "yellow": 0.1,
            "red": 0.2,
        }
    }


if __name__ == "__main__":
    import json
    result = check_drift()
    print(json.dumps(result, indent=2))
