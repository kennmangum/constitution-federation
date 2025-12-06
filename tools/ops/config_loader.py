#!/usr/bin/env python3
"""
config_loader.py — v1.0
Central YAML loader for all policy/config files.
Per Lumen guidance 2025-12-05.

All Ring 2 YAMLs use this loader so:
- Missing files return safe defaults
- Parse errors are explicit, not silent
- Metadata tracks load status for IRON visibility
"""

import datetime
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:
    yaml = None


def load_yaml_with_default(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely load a YAML file or return the given default.
    Attaches metadata so IRON can see what actually happened.

    Args:
        path: Path to YAML file
        default: Default dict to return if file missing/corrupt

    Returns:
        Dict with file contents + _meta block
    """
    if yaml is None:
        cfg = default.copy()
        cfg["_meta"] = {
            "loaded": False,
            "reason": "pyyaml_not_installed",
            "path": str(path),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
        return cfg

    if not path.exists():
        cfg = default.copy()
        cfg["_meta"] = {
            "loaded": False,
            "reason": "missing",
            "path": str(path),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
        return cfg

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            data = {"value": data}
        data.setdefault("_meta", {})
        data["_meta"].update(
            {
                "loaded": True,
                "path": str(path),
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            }
        )
        return data
    except Exception as e:
        cfg = default.copy()
        cfg["_meta"] = {
            "loaded": False,
            "reason": f"parse_error:{e}",
            "path": str(path),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }
        return cfg


def save_yaml(path: Path, data: Dict[str, Any]) -> bool:
    """
    Save data to YAML file.

    Args:
        path: Path to YAML file
        data: Dict to save

    Returns:
        True if successful, False otherwise
    """
    if yaml is None:
        return False

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # Remove _meta before saving (it's runtime-only)
        save_data = {k: v for k, v in data.items() if k != "_meta"}
        path.write_text(yaml.safe_dump(save_data, sort_keys=False), encoding="utf-8")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # Quick test
    from pathlib import Path
    test_path = Path("/tmp/test_config.yaml")
    default = {"version": 1, "test": "default"}

    result = load_yaml_with_default(test_path, default)
    print(f"Load result: {result}")
