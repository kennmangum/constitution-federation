#!/usr/bin/env python3
"""
iron_elevation_sanitizer.py — Context prep for safe elevation into external tools (Claude-Code)

Usage (example):
  python3 tools/ops/iron_elevation_sanitizer.py \
      --task "Refactor federation_pulse for better hydration separation" \
      --out /tmp/iron_elevation_ctx \
      constitution/strategy/FEDERATION_SCAFFOLD.yaml \
      tools/rituals/federation_pulse.py

Produces:
  /tmp/iron_elevation_ctx/context_task.md
  /tmp/iron_elevation_ctx/context_files/...

Tiger is expected to:
- Run this AFTER approving an elevation request.
- Inspect the output folder.
- Only then hand it to Claude-Code as context.

Authority: IRON_ELEVATION_PROTOCOL_v1
Created: 2025-12-05
"""

import os
import sys
import argparse
import datetime
from pathlib import Path
from typing import List

BASE_CHARTER_PATHS = [
    "constitution/core/CHARTER.md",
    "constitution/core/ROE.md",
    "constitution/operations/FEDERATION_COLLABORATION_PROTOCOL_v1.md",
    "constitution/operations/IRON_ELEVATION_PROTOCOL_v1.md",
]


SENSITIVE_MARKERS = [
    "PRIVATE_KEY",
    "PRIVATE-KEY",
    "API_KEY",
    "API-KEY",
    "SECRET_KEY",
    "SECRET-KEY",
    "password",
    "passwd",
    "token",
    "bearer",
    "authorization",
    "credential",
    "wallet_seed",
    "mnemonic",
]


def detect_base_dir() -> Path:
    role = os.getenv("NODE_ROLE", "TIGER").upper()
    if role == "DRAGON":
        return Path(os.path.expanduser("~/rtx5090"))
    return Path(os.path.expanduser("~/Tiger_1a"))


BASE_DIR = detect_base_dir()


def read_excerpt(path: Path, max_chars: int = 1800) -> str:
    if not path.exists():
        return ""
    txt = path.read_text(encoding="utf-8", errors="ignore")
    if len(txt) > max_chars:
        return txt[:max_chars] + "\n...[truncated]..."
    return txt


def sanitize_lines(lines: List[str]) -> List[str]:
    """Remove or redact lines that appear to contain sensitive markers."""
    sanitized: List[str] = []
    for line in lines:
        if any(marker.lower() in line.lower() for marker in SENSITIVE_MARKERS):
            # Replace line with a redaction notice
            sanitized.append("# [REDACTED SENSITIVE LINE]\n")
        else:
            sanitized.append(line)
    return sanitized


def copy_sanitized_file(src: Path, dest: Path, max_bytes: int = 64 * 1024) -> None:
    """Copy file with simple sanitization and size limit."""
    if not src.exists() or not src.is_file():
        return
    text = src.read_text(encoding="utf-8", errors="ignore")
    # Size guard
    if len(text.encode("utf-8")) > max_bytes:
        text = text[:max_bytes] + "\n...[truncated for elevation]..."
    lines = text.splitlines(keepends=True)
    sanitized = sanitize_lines(lines)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("".join(sanitized), encoding="utf-8")


def build_task_file(task: str, out_dir: Path) -> None:
    """Create context_task.md with Charter/ROE/protocol excerpts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    task_path = out_dir / "context_task.md"

    now = datetime.datetime.utcnow().isoformat() + "Z"
    parts = [f"# IRON Elevation Task\n\nTimestamp: {now}\n\n"]
    parts.append("## Task Description\n\n")
    parts.append(task.strip() + "\n\n")

    parts.append("## Constitutional Context (Excerpts)\n\n")

    for rel in BASE_CHARTER_PATHS:
        full = BASE_DIR / rel
        label = rel.split("/")[-1]
        excerpt = read_excerpt(full)
        if not excerpt:
            continue
        parts.append(f"### {label}\n\n")
        parts.append(excerpt.strip() + "\n\n")

    task_path.write_text("".join(parts), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Prepare sanitized context for IRON elevation.")
    parser.add_argument(
        "--task",
        required=True,
        help="Short description of the elevation task.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for elevation context.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Paths to additional files to include in context_files (relative to BASE_DIR).",
    )

    args = parser.parse_args()
    out_dir = Path(args.out)
    ctx_files_dir = out_dir / "context_files"

    # Build the high-level task file
    build_task_file(args.task, out_dir)

    # Copy and sanitize additional files
    for rel in args.files:
        src = BASE_DIR / rel
        dest = ctx_files_dir / rel
        copy_sanitized_file(src, dest)

    print(
        {
            "status": "ok",
            "out_dir": str(out_dir),
            "files_included": args.files,
        }
    )


if __name__ == "__main__":
    main()
