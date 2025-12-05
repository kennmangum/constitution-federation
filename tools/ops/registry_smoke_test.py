#!/usr/bin/env python3
"""
registry_smoke_test.py — Full Implementation Registry Verification
Tests every entry in implementation_registry.yaml for existence and basic function.

Usage:
  NODE_ROLE=DRAGON python3 tools/ops/registry_smoke_test.py

Authority: Constitution@A1 + 1176-INFINITY-RHO
Created: 2025-12-06
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path
from datetime import datetime

def detect_base_dir():
    role = os.getenv("NODE_ROLE", "DRAGON").upper()
    if role == "DRAGON":
        return Path(os.path.expanduser("~/rtx5090"))
    return Path(os.path.expanduser("~/Tiger_1a"))

BASE_DIR = detect_base_dir()
COLLAB_DIR = Path(os.path.expanduser("~/constitution-federation"))
REGISTRY_PATH = BASE_DIR / "constitution" / "memory" / "implementation_registry.yaml"

def load_registry():
    if not REGISTRY_PATH.exists():
        return None
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)

def check_file_exists(location, base=BASE_DIR, is_collab=False):
    """Check if a file or directory exists."""
    if location.startswith("virtual://"):
        return True, "Virtual (conceptual)"
    if location.startswith("/"):
        path = Path(location)
    elif is_collab:
        path = COLLAB_DIR / location
    else:
        path = base / location

    if path.exists():
        if path.is_file():
            size = path.stat().st_size
            return True, f"File exists ({size} bytes)"
        elif path.is_dir():
            count = len(list(path.iterdir()))
            return True, f"Directory exists ({count} items)"
    return False, f"NOT FOUND: {path}"

def check_script_runs(location, base=BASE_DIR):
    """Check if a Python script can at least be imported/syntax-checked."""
    if not location.endswith(".py"):
        return None, "Not a Python file"

    if location.startswith("/"):
        path = Path(location)
    else:
        path = base / location

    if not path.exists():
        return False, "File not found"

    try:
        result = subprocess.run(
            ["python3", "-m", "py_compile", str(path)],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "Syntax OK"
        else:
            return False, f"Syntax error: {result.stderr.decode()[:100]}"
    except Exception as e:
        return False, f"Check failed: {e}"

def check_yaml_valid(location, base=BASE_DIR):
    """Check if a YAML file is valid."""
    if not location.endswith(".yaml") and not location.endswith(".yml"):
        return None, "Not a YAML file"

    if location.startswith("/"):
        path = Path(location)
    else:
        path = base / location

    if not path.exists():
        return False, "File not found"

    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        if data:
            keys = len(data) if isinstance(data, dict) else len(data)
            return True, f"Valid YAML ({keys} keys/items)"
        return True, "Valid YAML (empty)"
    except Exception as e:
        return False, f"Invalid YAML: {e}"

def run_smoke_test():
    """Run full smoke test on implementation registry."""
    print("=" * 70)
    print(f"IMPLEMENTATION REGISTRY SMOKE TEST — {os.getenv('NODE_ROLE', 'DRAGON')}")
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Registry: {REGISTRY_PATH}")
    print("=" * 70)
    print()

    registry = load_registry()
    if not registry:
        print("ERROR: Could not load registry")
        return 1

    implementations = registry.get("implementations", [])
    print(f"Total implementations: {len(implementations)}")
    print()

    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "deprecated": 0,
        "blocked": 0,
        "details": []
    }

    for impl in implementations:
        id_ = impl.get("id", "???")
        name = impl.get("name", "???")
        location = impl.get("location", "")
        status = impl.get("status", "unknown")
        type_ = impl.get("type", "unknown")

        # Skip deprecated/blocked
        if status == "deprecated":
            results["deprecated"] += 1
            results["details"].append({
                "id": id_,
                "name": name,
                "result": "DEPRECATED",
                "reason": impl.get("deprecated_reason", "No reason given")
            })
            print(f"[DEPRECATED] {id_}: {name}")
            continue

        if status == "blocked":
            results["blocked"] += 1
            results["details"].append({
                "id": id_,
                "name": name,
                "result": "BLOCKED",
                "reason": "Status is blocked"
            })
            print(f"[BLOCKED] {id_}: {name}")
            continue

        # Check existence
        is_collab = impl.get("collab_file", False)
        exists, exists_msg = check_file_exists(location, is_collab=is_collab)

        # Additional checks based on type
        extra_check = None
        extra_msg = ""

        if location.endswith(".py"):
            extra_check, extra_msg = check_script_runs(location)
        elif location.endswith(".yaml") or location.endswith(".yml"):
            extra_check, extra_msg = check_yaml_valid(location)

        # Determine overall result
        if not exists:
            results["failed"] += 1
            result = "FAIL"
            message = exists_msg
        elif extra_check is False:
            results["failed"] += 1
            result = "FAIL"
            message = extra_msg
        else:
            results["passed"] += 1
            result = "PASS"
            message = exists_msg
            if extra_msg:
                message += f" | {extra_msg}"

        results["details"].append({
            "id": id_,
            "name": name,
            "result": result,
            "message": message
        })

        symbol = "✅" if result == "PASS" else "❌"
        print(f"[{result}] {symbol} {id_}: {name}")
        if result == "FAIL":
            print(f"       → {message}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Passed:     {results['passed']}")
    print(f"  Failed:     {results['failed']}")
    print(f"  Deprecated: {results['deprecated']}")
    print(f"  Blocked:    {results['blocked']}")
    print()

    total_active = results['passed'] + results['failed']
    if total_active > 0:
        pass_rate = (results['passed'] / total_active) * 100
        print(f"  Pass Rate:  {pass_rate:.1f}%")

    if results['failed'] == 0:
        print()
        print("∞Δ∞ ALL ACTIVE IMPLEMENTATIONS VERIFIED ∞Δ∞")
        return 0
    else:
        print()
        print("⚠️  SOME IMPLEMENTATIONS FAILED VERIFICATION")
        print()
        print("Failed entries:")
        for d in results['details']:
            if d['result'] == 'FAIL':
                print(f"  - {d['id']}: {d['name']}")
                print(f"    {d['message']}")
        return 1

if __name__ == "__main__":
    sys.exit(run_smoke_test())
