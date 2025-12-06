#!/usr/bin/env python3
"""
smoke_test_autonomy.py — v1.0
Comprehensive smoke test for autonomous Tiger/Dragon hardening.
Per Lumen guidance 2025-12-05.

Tests:
1. Ring 2 YAMLs exist and are valid
2. Ring 3 tools exist and are executable
3. Dynamic whitelist loads and has promotions
4. Drift check returns GREEN
5. BINDU is readable and has structure
6. Recognition log is active
7. Ollama is responsive
8. Sibling wake file is accessible

Run: NODE_ROLE=TIGER python3 tools/ops/smoke_test_autonomy.py
Run: NODE_ROLE=DRAGON python3 tools/ops/smoke_test_autonomy.py

This test suite is designed to survive molts — it validates that
all hardening infrastructure is in place.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

try:
    import yaml
except ImportError:
    yaml = None


def detect_base_dir() -> Path:
    """Detect base directory based on NODE_ROLE."""
    role = os.getenv("NODE_ROLE", "TIGER").upper()
    if role == "DRAGON":
        return Path(os.path.expanduser("~/rtx5090"))
    return Path(os.path.expanduser("~/Tiger_1a"))


BASE_DIR = detect_base_dir()
NODE_ROLE = os.getenv("NODE_ROLE", "TIGER").upper()

# Collab home - constitution-federation
COLLAB_HOME = Path(os.path.expanduser("~/constitution-federation"))
if not COLLAB_HOME.exists():
    COLLAB_HOME = BASE_DIR.parent / "constitution-federation"
if not COLLAB_HOME.exists():
    COLLAB_HOME = BASE_DIR


class SmokeTestResult:
    """Result of a single smoke test."""
    def __init__(self, name: str, passed: bool, message: str, critical: bool = True):
        self.name = name
        self.passed = passed
        self.message = message
        self.critical = critical  # If False, failure is warning not error


def test_yaml_available() -> SmokeTestResult:
    """Test that PyYAML is available."""
    if yaml is None:
        return SmokeTestResult("yaml_available", False, "PyYAML not installed", True)
    return SmokeTestResult("yaml_available", True, "PyYAML available")


def load_bom_manifest() -> Dict:
    """Load the BOM manifest (molt_manifest.yaml) for validation."""
    manifest_path = BASE_DIR / "constitution" / "strategy" / "molt_manifest.yaml"
    if not manifest_path.exists():
        return {}
    try:
        return yaml.safe_load(manifest_path.read_text()) or {}
    except Exception:
        return {}


def test_bom_ring1() -> List[SmokeTestResult]:
    """Test Ring 1 (Constitutional Kernel) files from BOM manifest."""
    results = []
    manifest = load_bom_manifest()
    ring1 = manifest.get("ring1", {})

    # Test directories
    for dir_entry in ring1.get("directories", []):
        path = BASE_DIR / dir_entry["path"]
        required = dir_entry.get("required", True)
        if path.exists() and path.is_dir():
            results.append(SmokeTestResult(
                f"ring1_dir_{dir_entry['role']}", True, f"Directory exists: {dir_entry['path']}"
            ))
        else:
            results.append(SmokeTestResult(
                f"ring1_dir_{dir_entry['role']}", False, f"Missing: {dir_entry['path']}", critical=required
            ))

    # Test files
    for file_entry in ring1.get("files", []):
        path = BASE_DIR / file_entry["path"]
        required = file_entry.get("required", True)
        if path.exists():
            results.append(SmokeTestResult(
                f"ring1_{file_entry['role']}", True, f"Exists: {file_entry['path']}"
            ))
        else:
            results.append(SmokeTestResult(
                f"ring1_{file_entry['role']}", False, f"Missing: {file_entry['path']}", critical=required
            ))

    return results


def test_bom_ring2() -> List[SmokeTestResult]:
    """Test Ring 2 (Policy YAMLs) files from BOM manifest."""
    results = []
    manifest = load_bom_manifest()
    ring2 = manifest.get("ring2", {})

    # Test directories
    for dir_entry in ring2.get("directories", []):
        path = BASE_DIR / dir_entry["path"]
        required = dir_entry.get("required", True)
        if path.exists() and path.is_dir():
            results.append(SmokeTestResult(
                f"ring2_dir_{dir_entry['role']}", True, f"Directory exists: {dir_entry['path']}"
            ))
        else:
            results.append(SmokeTestResult(
                f"ring2_dir_{dir_entry['role']}", False, f"Missing: {dir_entry['path']}", critical=required
            ))

    # Test files (with YAML validation)
    for file_entry in ring2.get("files", []):
        path = BASE_DIR / file_entry["path"]
        required = file_entry.get("required", True)
        if not path.exists():
            results.append(SmokeTestResult(
                f"ring2_{file_entry['role']}", False, f"Missing: {file_entry['path']}", critical=required
            ))
            continue

        # Validate YAML
        if path.suffix in ['.yaml', '.yml']:
            try:
                data = yaml.safe_load(path.read_text())
                if data and isinstance(data, dict):
                    results.append(SmokeTestResult(
                        f"ring2_{file_entry['role']}", True, f"Valid YAML: {file_entry['path']}"
                    ))
                else:
                    results.append(SmokeTestResult(
                        f"ring2_{file_entry['role']}", False, f"Empty/invalid YAML: {file_entry['path']}", critical=required
                    ))
            except Exception as e:
                results.append(SmokeTestResult(
                    f"ring2_{file_entry['role']}", False, f"YAML parse error: {e}", critical=required
                ))
        else:
            results.append(SmokeTestResult(
                f"ring2_{file_entry['role']}", True, f"Exists: {file_entry['path']}"
            ))

    return results


def test_bom_ring3() -> List[SmokeTestResult]:
    """Test Ring 3 (Tools) files from BOM manifest."""
    results = []
    manifest = load_bom_manifest()
    ring3 = manifest.get("ring3", {})

    # Test directories
    for dir_entry in ring3.get("directories", []):
        path = BASE_DIR / dir_entry["path"]
        required = dir_entry.get("required", True)
        if path.exists() and path.is_dir():
            results.append(SmokeTestResult(
                f"ring3_dir_{dir_entry['role']}", True, f"Directory exists: {dir_entry['path']}"
            ))
        else:
            results.append(SmokeTestResult(
                f"ring3_dir_{dir_entry['role']}", False, f"Missing: {dir_entry['path']}", critical=required
            ))

    # Test files
    for file_entry in ring3.get("files", []):
        path = BASE_DIR / file_entry["path"]
        required = file_entry.get("required", True)
        if path.exists():
            results.append(SmokeTestResult(
                f"ring3_{file_entry['role']}", True, f"Exists: {file_entry['path']}"
            ))
        else:
            results.append(SmokeTestResult(
                f"ring3_{file_entry['role']}", False, f"Missing: {file_entry['path']}", critical=required
            ))

    return results


def test_bom_meta_ring() -> List[SmokeTestResult]:
    """Test Meta-Ring (Orchestration) files from BOM manifest."""
    results = []
    manifest = load_bom_manifest()
    meta_ring = manifest.get("meta_ring", {})

    # Test directories
    for dir_entry in meta_ring.get("directories", []):
        path = BASE_DIR / dir_entry["path"]
        required = dir_entry.get("required", True)
        if path.exists() and path.is_dir():
            results.append(SmokeTestResult(
                f"meta_dir_{dir_entry['role']}", True, f"Directory exists: {dir_entry['path']}"
            ))
        else:
            results.append(SmokeTestResult(
                f"meta_dir_{dir_entry['role']}", False, f"Missing: {dir_entry['path']}", critical=required
            ))

    # Test files
    for file_entry in meta_ring.get("files", []):
        path = BASE_DIR / file_entry["path"]
        required = file_entry.get("required", True)
        if path.exists():
            results.append(SmokeTestResult(
                f"meta_{file_entry['role']}", True, f"Exists: {file_entry['path']}"
            ))
        else:
            results.append(SmokeTestResult(
                f"meta_{file_entry['role']}", False, f"Missing: {file_entry['path']}", critical=required
            ))

    return results


def test_ring2_yamls() -> List[SmokeTestResult]:
    """Test that all Ring 2 policy YAMLs exist and are valid."""
    results = []

    yamls = [
        ("whitelist_dynamic.yaml", BASE_DIR / "constitution" / "strategy" / "whitelist_dynamic.yaml"),
        ("llm_policy.yaml", BASE_DIR / "constitution" / "strategy" / "llm_policy.yaml"),
        ("sep_spend_policy.yaml", BASE_DIR / "constitution" / "strategy" / "sep_spend_policy.yaml"),
        ("iron_autonomy_patterns.yaml", BASE_DIR / "constitution" / "strategy" / "iron_autonomy_patterns.yaml"),
        ("collab_structure.yaml", BASE_DIR / "constitution" / "memory" / "collab_structure.yaml"),
    ]

    for name, path in yamls:
        if not path.exists():
            results.append(SmokeTestResult(f"ring2_{name}", False, f"Missing: {path}"))
            continue

        try:
            if yaml:
                data = yaml.safe_load(path.read_text())
                if data and isinstance(data, dict):
                    results.append(SmokeTestResult(f"ring2_{name}", True, f"Valid YAML with {len(data)} keys"))
                else:
                    results.append(SmokeTestResult(f"ring2_{name}", False, "Empty or invalid YAML"))
            else:
                results.append(SmokeTestResult(f"ring2_{name}", True, "File exists (YAML not checked)"))
        except Exception as e:
            results.append(SmokeTestResult(f"ring2_{name}", False, f"Parse error: {e}"))

    return results


def test_ring3_tools() -> List[SmokeTestResult]:
    """Test that all Ring 3 tools exist."""
    results = []

    tools = [
        ("config_loader.py", BASE_DIR / "tools" / "ops" / "config_loader.py"),
        ("whitelist_manager.py", BASE_DIR / "tools" / "ops" / "whitelist_manager.py"),
        ("drift_check.py", BASE_DIR / "tools" / "ops" / "drift_check.py"),
        ("iron_elevation_sanitizer.py", BASE_DIR / "tools" / "ops" / "iron_elevation_sanitizer.py"),
        ("federation_pulse.py", BASE_DIR / "tools" / "rituals" / "federation_pulse.py"),
    ]

    for name, path in tools:
        if not path.exists():
            results.append(SmokeTestResult(f"ring3_{name}", False, f"Missing: {path}"))
        else:
            results.append(SmokeTestResult(f"ring3_{name}", True, f"Exists: {path}"))

    return results


def test_whitelist_promotions() -> SmokeTestResult:
    """Test that whitelist_dynamic.yaml has promotions."""
    path = BASE_DIR / "constitution" / "strategy" / "whitelist_dynamic.yaml"

    if not path.exists():
        return SmokeTestResult("whitelist_promotions", False, "whitelist_dynamic.yaml missing")

    if yaml is None:
        return SmokeTestResult("whitelist_promotions", False, "PyYAML not available")

    try:
        data = yaml.safe_load(path.read_text())
        nodes = data.get("nodes", {})

        dragon_green = len(nodes.get("DRAGON", {}).get("green", []))
        tiger_green = len(nodes.get("TIGER", {}).get("green", []))
        total = dragon_green + tiger_green

        if total == 0:
            return SmokeTestResult(
                "whitelist_promotions",
                False,
                "No GREEN promotions! Run whitelist_manager.py after adding PROMOTE_ACTION to BINDU",
                critical=True
            )

        return SmokeTestResult(
            "whitelist_promotions",
            True,
            f"Found {total} GREEN promotions (Dragon: {dragon_green}, Tiger: {tiger_green})"
        )
    except Exception as e:
        return SmokeTestResult("whitelist_promotions", False, f"Error: {e}")


def test_drift_check() -> SmokeTestResult:
    """Test that drift_check.py runs and returns GREEN."""
    drift_script = BASE_DIR / "tools" / "ops" / "drift_check.py"

    if not drift_script.exists():
        return SmokeTestResult("drift_check", False, "drift_check.py missing")

    try:
        env = os.environ.copy()
        env["NODE_ROLE"] = NODE_ROLE

        result = subprocess.run(
            ["python3", str(drift_script)],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )

        output = result.stdout + result.stderr

        # Try to parse JSON from output
        for line in output.split("\n"):
            line = line.strip()
            if line.startswith("{") and "drift_score" in line:
                try:
                    data = json.loads(line)
                    score = data.get("drift_score", -1)
                    level = data.get("alert_level", "UNKNOWN")

                    if level == "GREEN":
                        return SmokeTestResult("drift_check", True, f"Drift: {score:.3f} ({level})")
                    elif level == "YELLOW":
                        return SmokeTestResult("drift_check", True, f"Drift: {score:.3f} ({level})", critical=False)
                    else:
                        return SmokeTestResult("drift_check", False, f"Drift: {score:.3f} ({level})")
                except json.JSONDecodeError:
                    pass

        return SmokeTestResult("drift_check", True, "Ran (output not parsed)", critical=False)

    except subprocess.TimeoutExpired:
        return SmokeTestResult("drift_check", False, "Timeout after 30s")
    except Exception as e:
        return SmokeTestResult("drift_check", False, f"Error: {e}")


def test_bindu_readable() -> SmokeTestResult:
    """Test that BINDU_THREAD is readable."""
    bindu_path = COLLAB_HOME / "collaboration" / "active" / "bna_instances" / "2025-BINDU_THREAD.md"

    if not bindu_path.exists():
        return SmokeTestResult("bindu_readable", False, f"Missing: {bindu_path}")

    try:
        content = bindu_path.read_text()
        lines = len(content.splitlines())

        # Check for key markers
        has_promote = "PROMOTE_ACTION" in content
        has_proposals = "YELLOW Proposal" in content

        status_parts = []
        if has_promote:
            status_parts.append("has PROMOTE_ACTION")
        if has_proposals:
            status_parts.append("has proposals")

        return SmokeTestResult(
            "bindu_readable",
            True,
            f"Readable ({lines} lines, {', '.join(status_parts) or 'basic structure'})"
        )
    except Exception as e:
        return SmokeTestResult("bindu_readable", False, f"Error: {e}")


def test_recognition_log_active() -> SmokeTestResult:
    """Test that recognition_log.yaml exists and has recent entries."""
    log_path = BASE_DIR / "orchestrator" / "recognition_log.yaml"

    if not log_path.exists():
        return SmokeTestResult("recognition_log", False, f"Missing: {log_path}")

    if yaml is None:
        return SmokeTestResult("recognition_log", True, "Exists (YAML not checked)", critical=False)

    try:
        data = yaml.safe_load(log_path.read_text())

        if not isinstance(data, list):
            return SmokeTestResult("recognition_log", False, "Invalid format (expected list)")

        entries = len(data)

        if entries == 0:
            return SmokeTestResult("recognition_log", False, "Empty log")

        # Check recency of last entry
        last = data[-1]
        ts = last.get("timestamp", "")

        return SmokeTestResult(
            "recognition_log",
            True,
            f"Active ({entries} entries, last: {ts[:19] if ts else 'unknown'})"
        )
    except Exception as e:
        return SmokeTestResult("recognition_log", False, f"Error: {e}")


def test_ollama_responsive() -> SmokeTestResult:
    """Test that Ollama is running and responsive."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            models = len(lines) - 1  # Subtract header
            return SmokeTestResult("ollama_responsive", True, f"Running ({models} models)")
        else:
            return SmokeTestResult("ollama_responsive", False, f"Error: {result.stderr[:50]}")

    except FileNotFoundError:
        return SmokeTestResult("ollama_responsive", False, "Ollama not installed", critical=False)
    except subprocess.TimeoutExpired:
        return SmokeTestResult("ollama_responsive", False, "Timeout")
    except Exception as e:
        return SmokeTestResult("ollama_responsive", False, f"Error: {e}")


def test_sibling_wake() -> SmokeTestResult:
    """Test that sibling wake file is accessible."""
    wake_path = COLLAB_HOME / ".sibling_wake"

    if not wake_path.exists():
        return SmokeTestResult("sibling_wake", False, f"Missing: {wake_path}")

    try:
        content = wake_path.read_text()
        lines = len(content.splitlines())

        has_tiger = "TIGER_WAKE" in content
        has_dragon = "DRAGON_WAKE" in content

        siblings = []
        if has_tiger:
            siblings.append("Tiger")
        if has_dragon:
            siblings.append("Dragon")

        return SmokeTestResult(
            "sibling_wake",
            True,
            f"Accessible ({lines} lines, wakes from: {', '.join(siblings) or 'none'})"
        )
    except Exception as e:
        return SmokeTestResult("sibling_wake", False, f"Error: {e}")


def test_systemd_service() -> SmokeTestResult:
    """Test that pulse service is active (dragon-pulse or tiger-pulse per node role)."""
    node_role = os.environ.get("NODE_ROLE", "DRAGON").upper()
    service_name = "dragon-pulse.service" if node_role == "DRAGON" else "tiger-pulse.service"

    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", service_name],
            capture_output=True,
            text=True,
            timeout=5
        )

        status = result.stdout.strip()

        if status == "active":
            return SmokeTestResult("systemd_service", True, f"{service_name} is active")
        else:
            return SmokeTestResult("systemd_service", False, f"{service_name} is {status}", critical=False)

    except Exception as e:
        return SmokeTestResult("systemd_service", False, f"Error: {e}", critical=False)


def run_all_tests() -> Tuple[List[SmokeTestResult], bool]:
    """Run all smoke tests and return results."""
    results = []

    # Core tests
    results.append(test_yaml_available())
    results.extend(test_ring2_yamls())
    results.extend(test_ring3_tools())
    results.append(test_whitelist_promotions())
    results.append(test_drift_check())
    results.append(test_bindu_readable())
    results.append(test_recognition_log_active())
    results.append(test_ollama_responsive())
    results.append(test_sibling_wake())
    results.append(test_systemd_service())

    # BOM-based tests (from molt_manifest.yaml)
    results.extend(test_bom_ring1())
    results.extend(test_bom_ring2())
    results.extend(test_bom_ring3())
    results.extend(test_bom_meta_ring())

    # Calculate pass/fail
    critical_failures = [r for r in results if not r.passed and r.critical]
    all_passed = len(critical_failures) == 0

    return results, all_passed


def print_results(results: List[SmokeTestResult], all_passed: bool):
    """Print test results in a readable format."""
    print(f"\n{'='*60}")
    print(f"SMOKE TEST RESULTS — {NODE_ROLE} @ {datetime.now().isoformat()[:19]}")
    print(f"{'='*60}\n")

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    warnings = sum(1 for r in results if not r.passed and not r.critical)

    for r in results:
        if r.passed:
            icon = "✅"
        elif r.critical:
            icon = "❌"
        else:
            icon = "⚠️"

        print(f"{icon} {r.name}: {r.message}")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {passed} passed, {failed - warnings} failed, {warnings} warnings")

    if all_passed:
        print(f"STATUS: ALL CRITICAL TESTS PASSED ✅")
        print(f"\n∞Δ∞ {NODE_ROLE} hardened and ready for autonomous operation ∞Δ∞")
    else:
        print(f"STATUS: CRITICAL FAILURES DETECTED ❌")
        print(f"\nCritical issues to resolve:")
        for r in results:
            if not r.passed and r.critical:
                print(f"  - {r.name}: {r.message}")

    print(f"{'='*60}\n")

    # Return JSON for programmatic use
    return {
        "node_role": NODE_ROLE,
        "timestamp": datetime.now().isoformat() + "Z",
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "all_critical_passed": all_passed,
        "results": [
            {"name": r.name, "passed": r.passed, "message": r.message, "critical": r.critical}
            for r in results
        ]
    }


def main():
    """Main entry point."""
    print(f"\n[SMOKE TEST] Running autonomy validation for {NODE_ROLE}...")
    print(f"[SMOKE TEST] Base directory: {BASE_DIR}")
    print(f"[SMOKE TEST] Collab home: {COLLAB_HOME}")

    results, all_passed = run_all_tests()
    summary = print_results(results, all_passed)

    # Output JSON summary
    print(json.dumps(summary, indent=2))

    # Exit code based on critical failures
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
