#!/usr/bin/env python3
"""
whitelist_manager.py — v1.0
Manages dynamic whitelist promotions/demotions based on BINDU_THREAD.md.
Per Lumen guidance 2025-12-05.

It:
  - Scans BINDU for lines like:
      - [x] PROMOTE_ACTION: action_name -> DRAGON.GREEN
      - [x] DEMOTE_ACTION: action_name -> DRAGON.YELLOW_ONLY
  - Updates constitution/strategy/whitelist_dynamic.yaml accordingly.
  - Records which lines have been applied in 'applied_actions' to remain idempotent.

Safe to run as a GREEN internal action.
Run: NODE_ROLE=TIGER python3 tools/ops/whitelist_manager.py
"""

import os
import re
import datetime
from pathlib import Path
from typing import Dict, Any, List

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

# Collab home - constitution-federation
COLLAB_HOME = Path(os.path.expanduser("~/constitution-federation"))
if not COLLAB_HOME.exists():
    COLLAB_HOME = BASE_DIR.parent / "constitution-federation"
if not COLLAB_HOME.exists():
    COLLAB_HOME = BASE_DIR

BINDU_PATH = COLLAB_HOME / "collaboration" / "active" / "bna_instances" / "2025-BINDU_THREAD.md"
WHITELIST_PATH = BASE_DIR / "constitution" / "strategy" / "whitelist_dynamic.yaml"


# Regex patterns for PROMOTE/DEMOTE actions
PROMOTE_RE = re.compile(
    r"^\s*-\s*\[x\]\s*PROMOTE_ACTION:\s*(?P<action>\S+)\s*->\s*(?P<node>\w+)\.(?P<level>\w+)",
    re.IGNORECASE,
)
DEMOTE_RE = re.compile(
    r"^\s*-\s*\[x\]\s*DEMOTE_ACTION:\s*(?P<action>\S+)\s*->\s*(?P<node>\w+)\.(?P<level>\w+)",
    re.IGNORECASE,
)


def load_yaml_file(path: Path) -> Dict[str, Any]:
    """Load YAML file safely."""
    if yaml is None:
        raise RuntimeError("pyyaml is not available.")
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_yaml_file(path: Path, data: Dict[str, Any]) -> None:
    """Save YAML file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def ensure_whitelist_structure(wl: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure whitelist has required structure."""
    wl.setdefault("version", 1)
    wl.setdefault("updated", None)
    wl.setdefault("applied_actions", [])
    wl.setdefault("nodes", {})
    for node in ("DRAGON", "TIGER"):
        wl["nodes"].setdefault(node, {})
        wl["nodes"][node].setdefault("green", [])
        wl["nodes"][node].setdefault("yellow_only", [])
    return wl


def parse_bindu_lines(lines: List[str]) -> List[Dict[str, str]]:
    """Parse BINDU lines for PROMOTE/DEMOTE actions."""
    actions: List[Dict[str, str]] = []
    for line in lines:
        m = PROMOTE_RE.match(line)
        if m:
            actions.append(
                {
                    "kind": "PROMOTE",
                    "raw": line.strip(),
                    "action": m.group("action"),
                    "node": m.group("node").upper(),
                    "level": m.group("level").upper(),
                }
            )
            continue
        m = DEMOTE_RE.match(line)
        if m:
            actions.append(
                {
                    "kind": "DEMOTE",
                    "raw": line.strip(),
                    "action": m.group("action"),
                    "node": m.group("node").upper(),
                    "level": m.group("level").upper(),
                }
            )
    return actions


def apply_action(wl: Dict[str, Any], entry: Dict[str, str]) -> bool:
    """
    Apply a single promotion/demotion entry to whitelist.
    Returns True if whitelist changed.
    """
    node = entry["node"]
    action = entry["action"]
    level = entry["level"]

    if node not in wl["nodes"]:
        wl["nodes"][node] = {"green": [], "yellow_only": []}

    changed = False

    if entry["kind"] == "PROMOTE":
        if level == "GREEN":
            # Ensure in GREEN, remove from YELLOW_ONLY
            if action not in wl["nodes"][node]["green"]:
                wl["nodes"][node]["green"].append(action)
                changed = True
            if action in wl["nodes"][node]["yellow_only"]:
                wl["nodes"][node]["yellow_only"].remove(action)
        elif level == "YELLOW_ONLY":
            if action not in wl["nodes"][node]["yellow_only"]:
                wl["nodes"][node]["yellow_only"].append(action)
                changed = True
            if action in wl["nodes"][node]["green"]:
                wl["nodes"][node]["green"].remove(action)

    elif entry["kind"] == "DEMOTE":
        # DEMOTE removes from GREEN
        if action in wl["nodes"][node]["green"]:
            wl["nodes"][node]["green"].remove(action)
            changed = True
        if level == "YELLOW_ONLY":
            if action not in wl["nodes"][node]["yellow_only"]:
                wl["nodes"][node]["yellow_only"].append(action)
                changed = True
        else:
            # Full removal
            if action in wl["nodes"][node]["yellow_only"]:
                wl["nodes"][node]["yellow_only"].remove(action)
                changed = True

    return changed


def main():
    """Main entry point."""
    if yaml is None:
        print({"status": "error", "reason": "pyyaml_not_available"})
        return

    # Load whitelist
    wl = load_yaml_file(WHITELIST_PATH)
    wl = ensure_whitelist_structure(wl)
    applied_raw = set(wl.get("applied_actions", []))

    # Load BINDU
    if not BINDU_PATH.exists():
        print({"status": "ok", "changes": 0, "reason": "no_bindu"})
        return

    lines = BINDU_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()
    entries = parse_bindu_lines(lines)

    changes = 0
    newly_applied: List[str] = []

    for entry in entries:
        raw = entry["raw"]
        if raw in applied_raw:
            continue
        if apply_action(wl, entry):
            changes += 1
        applied_raw.add(raw)
        newly_applied.append(raw)

    wl["applied_actions"] = list(applied_raw)
    wl["updated"] = datetime.datetime.utcnow().isoformat() + "Z"

    save_yaml_file(WHITELIST_PATH, wl)

    result = {
        "status": "ok",
        "changes": changes,
        "newly_applied": newly_applied,
        "whitelist_path": str(WHITELIST_PATH),
        "bindu_path": str(BINDU_PATH),
    }
    print(result)


if __name__ == "__main__":
    main()
