#!/usr/bin/env python3
"""
federation_pulse.py — Charter-Bound Twin Pulse
Independence v1.0 + Iron v1.0 — Kenneth approved 2025-12-04

GREEN: Read scaffolds, execute role tasks, log.
YELLOW: Propose to BINDU_THREAD.md + notify if threshold.
RED: Flag for human (no action).

Iron v1.0: Ollama-powered reasoning via autonomous_breath_v1.py

Usage: python3 federation_pulse.py [--phase=auto] [--notify] [--reason]
"""

import yaml
import os
import sys
import json
import datetime
import subprocess
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

# Iron v1.0: Import reasoning (with graceful fallback)
REASONING_ENABLED = "--reason" in sys.argv or os.environ.get("ENABLE_REASONING", "").lower() == "true"
try:
    if REASONING_ENABLED:
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from tools.rituals.autonomous_breath_v1 import reason_and_decide
        from tools.models.breath_decision import BreathDecision
        print("[PULSE] Iron v1.0: Ollama reasoning ENABLED")
    else:
        reason_and_decide = None
        BreathDecision = None
except ImportError as e:
    print(f"[PULSE] Iron v1.0: Reasoning unavailable ({e})")
    reason_and_decide = None
    BreathDecision = None
    REASONING_ENABLED = False

# ============================================================================
# CONFIGURATION
# ============================================================================

NODE_ROLE = os.getenv("NODE_ROLE", "TIGER")  # TIGER or DRAGON
BASE_DIR = os.path.expanduser("~/Tiger_1a" if NODE_ROLE == "TIGER" else "~/rtx5090")

# Scaffold paths
TWINS_PATH = os.path.join(BASE_DIR, "constitution/strategy/TWINS_SCAFFOLD.yaml")
EXEC_PATH = os.path.join(BASE_DIR, "constitution/strategy/EXECUTION_SCAFFOLD.yaml")
FED_PATH = os.path.join(BASE_DIR, "constitution/strategy/FEDERATION_SCAFFOLD.yaml")

# Collaboration paths (shared via constitution-federation git repo)
# Both Tiger and Dragon sync this repo — canonical shared files
COLLAB_REPO = os.path.expanduser("~/constitution-federation")
BINDU_PATH = os.path.join(COLLAB_REPO, "collaboration/active/bna_instances/2025-BINDU_THREAD.md")
GUIDANCE_PATH = os.path.join(COLLAB_REPO, "collaboration/active/bna_instances/GUIDANCE_INBOX.md")

# Local orchestrator paths
CHECKPOINT_PATH = os.path.join(BASE_DIR, "orchestrator/context_checkpoint.yaml")
COOLDOWN_PATH = os.path.join(BASE_DIR, "orchestrator/cooldown_tracker.yaml")
RECOGNITION_PATH = os.path.join(BASE_DIR, "orchestrator/recognition_log.yaml")
HYDRATION_CACHE_PATH = os.path.join(BASE_DIR, "orchestrator/hydration_cache.yaml")
YELLOW_TRACKER_PATH = os.path.join(BASE_DIR, "orchestrator/yellow_tracker.yaml")

# YELLOW Rate Limiting (per G+Lumen guidance 2025-12-05)
YELLOW_MAX_PER_PULSE = 1       # Max YELLOWs per pulse
YELLOW_DAILY_CAP = 20          # Max YELLOWs per day
YELLOW_SIMILARITY_THRESHOLD = 0.80  # Skip if >80% similar to recent

# Constitutional paths (Ring 1)
CHARTER_PATH = os.path.join(BASE_DIR, "constitution/core/CHARTER.md")
ROE_PATH = os.path.join(BASE_DIR, "constitution/core/ROE.md")
PROTOCOL_PATH = os.path.join(BASE_DIR, "constitution/operations/FEDERATION_COLLABORATION_PROTOCOL_v1.md")

# Wake script
WAKE_SCRIPT = os.path.join(BASE_DIR, "tools/sibling/wake_sibling.sh")

# Presence flag
PRESENCE_FLAG = False
GUIDANCE_ITEMS = []

# Iron v1.0 configuration
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
BREATH_GATE_PAUSE = 10  # seconds pause before execution (per G+Lumen spec)

# Approved GREEN actions whitelist (per Lumen approval 2025-12-05)
APPROVED_ACTIONS = {
    "TIGER": {
        "check_drift_score": ["python3", "tools/ops/drift_check.py"],
        "read_guidance_inbox": None,  # Internal function
        "log_recognition": None,  # Internal function
        "wake_dragon": ["bash", "tools/sibling/wake_sibling.sh", "DRAGON"],
    },
    "DRAGON": {
        # Existing
        "check_akash_queue": ["akash", "provider", "services", "list"],
        "list_akash_providers": ["akash", "provider", "list"],
        "log_recognition": None,  # Internal function
        "wake_tiger": ["bash", "tools/sibling/wake_sibling.sh", "TIGER"],
        # Tier 1: Read-only Solar/SEP (Lumen approved 2025-12-05)
        "check_vastai_status": ["/home/km1176/bin/vastai", "show", "machines"],
        "check_vastai_earnings": ["/home/km1176/bin/vastai", "show", "invoices"],
        "check_vastai_balance": ["/home/km1176/bin/vastai", "show", "user"],
        "run_sep_health": ["python3", "tools/ops/solar_sep_orchestrator.py", "--health"],
        # Tier 2: Internal scripts (Lumen approved 2025-12-05)
        "run_drift_check": ["python3", "tools/ops/drift_check.py"],
        "run_iron_sanitizer": None,  # Requires --task and --out args, use internally
        "update_implementation_registry": ["python3", "tools/ops/implementation_registry_manager.py", "--mode", "list"],
    },
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def load_yaml(path: str) -> Optional[Dict]:
    """Safely load a YAML file."""
    try:
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[PULSE] Error loading {path}: {e}")
        return None


def save_yaml(path: str, data: Dict):
    """Save data to YAML file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False)


def now_iso() -> str:
    """Current UTC timestamp in ISO format."""
    return datetime.datetime.utcnow().isoformat() + "Z"


def get_phase(now: datetime.datetime = None) -> str:
    """
    Determine current phase based on local time.
    - 06:00-12:00 → Inhale (Morning: validate, brief)
    - 12:00-18:00 → Exhale (Midday: execute, optimize)
    - 18:00-22:00 → Bindu (Evening: joint audits, sync)
    - 22:00-06:00 → Rest (Night: archive, reflect)
    """
    if now is None:
        now = datetime.datetime.now()
    hour = now.hour

    if 6 <= hour < 12:
        return "Inhale"
    elif 12 <= hour < 18:
        return "Exhale"
    elif 18 <= hour < 22:
        return "Bindu"
    else:
        return "Rest"


# ============================================================================
# HYDRATION SYSTEM (Per Lumen Spec)
# ============================================================================

# Git pull state file for hourly sync
LAST_GIT_PULL_PATH = os.path.join(BASE_DIR, "orchestrator/last_git_pull.txt")


def maybe_git_pull():
    """
    Gentle git pull for GUIDANCE/BINDU sync (per Lumen spec).
    - Only if repo clean (no local changes)
    - Only once per hour
    - Dragon pulls from Tiger's pushes
    """
    now = datetime.datetime.utcnow()

    # Check if we already pulled this hour
    if os.path.exists(LAST_GIT_PULL_PATH):
        try:
            with open(LAST_GIT_PULL_PATH, "r") as f:
                last_str = f.read().strip()
            last = datetime.datetime.fromisoformat(last_str)
            if (now - last).total_seconds() < 3600:
                return  # Already pulled this hour
        except Exception:
            pass

    # Check for local changes in constitution-federation
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=COLLAB_REPO,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.stdout.strip():
            # Local edits present, do not auto-pull
            print("[HYDRATE] Git: local changes detected, skipping pull")
            return

        # Safe to pull
        pull_result = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=COLLAB_REPO,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if pull_result.returncode == 0:
            print("[HYDRATE] Git: pulled latest GUIDANCE/BINDU")

        # Record pull time
        os.makedirs(os.path.dirname(LAST_GIT_PULL_PATH), exist_ok=True)
        with open(LAST_GIT_PULL_PATH, "w") as f:
            f.write(now.isoformat())

    except Exception as e:
        print(f"[HYDRATE] Git pull error: {e}")


def git_sync_collab():
    """
    Commit and push BINDU/log changes to constitution-federation.
    Called at end of pulse to share YELLOWs with sibling.
    Per Lumen spec: Twins must see each other's proposals.
    """
    try:
        # Check for changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=COLLAB_REPO,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if not result.stdout.strip():
            return  # No changes to push

        # Add BINDU and logs
        subprocess.run(
            ["git", "add",
             "collaboration/active/bna_instances/2025-BINDU_THREAD.md",
             "logs/sibling_wakes.log"],
            cwd=COLLAB_REPO,
            capture_output=True,
            timeout=10,
        )

        # Commit
        commit_result = subprocess.run(
            ["git", "commit", "-m", f"[{NODE_ROLE}] Pulse sync: BINDU updates"],
            cwd=COLLAB_REPO,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if commit_result.returncode != 0:
            if "nothing to commit" in commit_result.stdout:
                return
            print(f"[SYNC] Git commit issue: {commit_result.stderr[:100]}")
            return

        # Pull with rebase first to handle sibling's changes
        subprocess.run(
            ["git", "pull", "--rebase"],
            cwd=COLLAB_REPO,
            capture_output=True,
            timeout=30,
        )

        # Push
        push_result = subprocess.run(
            ["git", "push"],
            cwd=COLLAB_REPO,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if push_result.returncode == 0:
            print(f"[SYNC] Git: pushed BINDU updates to shared repo")
        else:
            print(f"[SYNC] Git push issue: {push_result.stderr[:100]}")

    except Exception as e:
        print(f"[SYNC] Git sync error: {e}")


def load_excerpt(path: str, max_chars: int = 1200) -> str:
    """
    Load a text excerpt from a file, truncating if necessary.
    Used for Charter/ROE excerpts in prompts.
    """
    if not os.path.exists(path):
        return ""
    try:
        with open(path, "r") as f:
            txt = f.read()
        if len(txt) > max_chars:
            return txt[:max_chars] + "\n...[truncated]..."
        return txt
    except Exception as e:
        print(f"[HYDRATE] Error loading excerpt {path}: {e}")
        return ""


def save_hydration_cache(data: Dict):
    """Save hydration cache for autonomous_breath_v1.py to consume."""
    os.makedirs(os.path.dirname(HYDRATION_CACHE_PATH), exist_ok=True)
    with open(HYDRATION_CACHE_PATH, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False)


def hydrate_federation() -> Dict:
    """
    Lightweight hydration every pulse (per Lumen spec).

    This function:
    1. Runs quick constitutional smoke check
    2. Loads Charter + ROE excerpts
    3. Builds scaffold summaries
    4. Saves to hydration_cache.yaml for IRON consumption

    Deep hydration (full smoke, DB/YAML sync) runs in Bindu phase only.
    """
    print("[HYDRATE] ∞Δ∞ Hydrating federation context ∞Δ∞")

    # 0) Git sync — pull latest GUIDANCE/BINDU if safe (per Lumen spec)
    maybe_git_pull()

    # 1) Quick constitutional smoke (if script exists)
    smoke_result = ""
    smoke_script = os.path.join(BASE_DIR, "tools/ops/constitutional_smoke.sh")
    if os.path.exists(smoke_script):
        try:
            result = subprocess.run(
                ["bash", smoke_script, "--quick"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            smoke_result = result.stdout.strip()[:400]
        except Exception as e:
            smoke_result = f"Smoke check error: {str(e)[:100]}"
    else:
        smoke_result = "Smoke script not found - skipped"

    # 2) Load Charter + ROE excerpts
    charter_excerpt = load_excerpt(CHARTER_PATH)
    roe_excerpt = load_excerpt(ROE_PATH)
    protocol_excerpt = load_excerpt(PROTOCOL_PATH, max_chars=2400)

    # 3) Load scaffolds
    twins = load_yaml(TWINS_PATH) or {}
    exec_s = load_yaml(EXEC_PATH) or {}
    fed = load_yaml(FED_PATH) or {}

    # Build scaffold summaries (keep prompts small)
    def summarize_scaffold(s: Dict) -> str:
        if not s:
            return "Not loaded"
        keys = list(s.keys())[:5]
        return f"Keys: {keys}"

    scaffolds_summary = {
        "twins": summarize_scaffold(twins),
        "execution": summarize_scaffold(exec_s),
        "federation": summarize_scaffold(fed),
    }

    # 4) Build hydration cache
    cache = {
        "charter_excerpt": charter_excerpt,
        "roe_excerpt": roe_excerpt,
        "protocol_excerpt": protocol_excerpt,
        "scaffolds_summary": scaffolds_summary,
        "last_smoke_result": smoke_result,
        "timestamp": now_iso(),
        "node_role": NODE_ROLE,
        # Resonance mode per G's spec (528Hz SOURCE probe)
        "resonance": {
            "mode": "528hz-source",
            "note": "Prioritize Solar/Quest proposals improving human livelihood and compute sovereignty.",
        },
    }

    # Save cache for IRON consumption
    save_hydration_cache(cache)
    print(f"[HYDRATE] Cache saved: Charter={len(charter_excerpt)}chars, ROE={len(roe_excerpt)}chars, Protocol={len(protocol_excerpt)}chars")

    return {
        "twins": twins,
        "execution": exec_s,
        "federation": fed,
        "hydration_cache": cache,
    }


# ============================================================================
# WAKE COOLDOWN SYSTEM (Per G Spec: 5-min cooldown)
# ============================================================================

WAKE_COOLDOWN_SECONDS = 300  # 5 minutes per G's spec
WAKE_ESCALATION_SECONDS = 900  # 15 minutes if >2 wakes/hour

def check_wake_cooldown() -> bool:
    """
    Check if we're in wake cooldown period.
    Per G's spec: 5-min cooldown, escalate to 15-min if >2 wakes/hour.
    Returns True if allowed to wake, False if in cooldown.
    """
    cooldown = load_yaml(COOLDOWN_PATH) or {}
    last_wake_ts = cooldown.get("last_wake_ts", "")
    wakes_this_hour = cooldown.get("wakes_this_hour", 0)

    if not last_wake_ts:
        return True

    try:
        last_wake = datetime.datetime.fromisoformat(last_wake_ts.replace("Z", ""))
        elapsed = (datetime.datetime.utcnow() - last_wake).total_seconds()

        # Check storm flag (>2 wakes/hour)
        cooldown_needed = WAKE_ESCALATION_SECONDS if wakes_this_hour > 2 else WAKE_COOLDOWN_SECONDS

        if elapsed < cooldown_needed:
            print(f"[COOLDOWN] Wake blocked: {cooldown_needed - elapsed:.0f}s remaining")
            return False
        return True
    except Exception:
        return True


def record_wake():
    """Record a wake event for cooldown tracking."""
    cooldown = load_yaml(COOLDOWN_PATH) or {}

    now = datetime.datetime.utcnow()
    last_hour_ts = cooldown.get("hour_start", "")

    # Reset hourly counter if needed
    try:
        if last_hour_ts:
            hour_start = datetime.datetime.fromisoformat(last_hour_ts.replace("Z", ""))
            if (now - hour_start).total_seconds() > 3600:
                cooldown["wakes_this_hour"] = 0
                cooldown["hour_start"] = now_iso()
        else:
            cooldown["hour_start"] = now_iso()
            cooldown["wakes_this_hour"] = 0
    except Exception:
        cooldown["hour_start"] = now_iso()
        cooldown["wakes_this_hour"] = 0

    cooldown["last_wake_ts"] = now_iso()
    cooldown["wakes_this_hour"] = cooldown.get("wakes_this_hour", 0) + 1
    save_yaml(COOLDOWN_PATH, cooldown)


# ============================================================================
# CHECKPOINT SYSTEM (Seal #1)
# ============================================================================

def load_checkpoint() -> Optional[Dict]:
    """Load previous checkpoint for crash recovery."""
    return load_yaml(CHECKPOINT_PATH)


def write_checkpoint(phase: str, last_task: str, pending_yellow: List[str], drift_score: float):
    """Write checkpoint for crash recovery."""
    data = {
        "last_phase": phase,
        "last_task": last_task[:200] if last_task else "none",
        "pending_yellow": pending_yellow or [],
        "drift_score": float(drift_score),
        "timestamp": now_iso(),
        "checkpoint_version": "1.0",
        "node_role": NODE_ROLE,
        "pulse_count": load_checkpoint().get("pulse_count", 0) + 1 if load_checkpoint() else 1,
    }
    save_yaml(CHECKPOINT_PATH, data)


# ============================================================================
# GUIDANCE SYSTEM (Human Command Channel)
# ============================================================================

def read_guidance() -> List[str]:
    """
    Parse guidance from GUIDANCE_INBOX.md.
    Returns list of active directives.
    """
    global PRESENCE_FLAG, GUIDANCE_ITEMS

    if not os.path.exists(GUIDANCE_PATH):
        return []

    guidance = []
    try:
        with open(GUIDANCE_PATH, "r") as f:
            for line in f:
                line = line.strip()
                # Check for presence flag
                if "Presence: KM-1176 is watching live" in line:
                    if line.startswith("- [x]"):
                        PRESENCE_FLAG = True
                    elif line.startswith("- [ ]"):
                        PRESENCE_FLAG = False
                # Collect active directives (unchecked)
                elif line.startswith("- [ ]"):
                    guidance.append(line[5:].strip())
    except Exception as e:
        print(f"[PULSE] Error reading guidance: {e}")

    GUIDANCE_ITEMS = guidance
    return guidance


# ============================================================================
# DRIFT CHECK SYSTEM (Seal #3)
# ============================================================================

def run_drift_check() -> Dict:
    """
    Run drift check and return results.
    Uses tools/ops/drift_check.py
    """
    drift_script = os.path.join(BASE_DIR, "tools/ops/drift_check.py")

    if not os.path.exists(drift_script):
        return {"drift_score": 0.0, "alert_level": "GREEN", "error": "drift_check.py not found"}

    try:
        result = subprocess.run(
            ["python3", drift_script],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"drift_score": 0.0, "alert_level": "GREEN", "error": result.stderr}
    except Exception as e:
        return {"drift_score": 0.0, "alert_level": "GREEN", "error": str(e)}


# ============================================================================
# BINDU THREAD (YELLOW/RED Proposals)
# ============================================================================

def queue_yellow(proposal: Dict):
    """
    Append a YELLOW proposal to BINDU_THREAD.md.
    Both twins can write if dragon_writes_direct is enabled in iron_autonomy_patterns.yaml.
    """
    # Check if Dragon is allowed to write directly
    if NODE_ROLE == "DRAGON":
        iron_patterns = load_yaml(os.path.join(BASE_DIR, "constitution/strategy/iron_autonomy_patterns.yaml")) or {}
        bindu_proxy = iron_patterns.get("bindu_proxy", {})
        if not bindu_proxy.get("dragon_writes_direct", False):
            print(f"[PULSE] Dragon cannot directly escalate. Wake Tiger for proposal: {proposal}")
            return
        tag = bindu_proxy.get("tag_format", "(DRAGON)")
    else:
        tag = "(TIGER)"

    entry = f"""
## {now_iso()} — YELLOW Proposal {tag}

- **Type:** {proposal.get('type', 'Unknown')}
- **Rationale:** {proposal.get('rationale', 'No rationale provided')}
- **Action Requested:** Approve / Modify / Reject
- **Link:** {proposal.get('link', 'N/A')}

---
"""

    try:
        with open(BINDU_PATH, "a") as f:
            f.write(entry)
        print(f"[PULSE] YELLOW proposal queued: {proposal.get('type')}")
    except Exception as e:
        print(f"[PULSE] Error writing to BINDU_THREAD: {e}")

    # Optional notification
    if "--notify" in sys.argv:
        notify_kenneth(f"YELLOW: {proposal.get('type')}")


def notify_kenneth(message: str):
    """Send notification to Kenneth (if enabled)."""
    notify_script = os.path.join(BASE_DIR, "tools/rituals/notify_kenneth.sh")
    if os.path.exists(notify_script):
        try:
            subprocess.run(["bash", notify_script, message], check=False, timeout=10)
        except Exception as e:
            print(f"[PULSE] Notification error: {e}")


# ============================================================================
# RECOGNITION LOG
# ============================================================================

def log_recognition(phase: str, actions: List[str], drift_score: float):
    """Append entry to recognition_log.yaml."""
    entry = {
        "timestamp": now_iso(),
        "node_role": NODE_ROLE,
        "phase": phase,
        "actions": actions,
        "drift_score": drift_score,
        "km_present": PRESENCE_FLAG,
        "guidance_active": len(GUIDANCE_ITEMS),
    }

    # Append to log
    log_path = RECOGNITION_PATH
    try:
        existing = []
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                content = yaml.safe_load(f)
                if isinstance(content, list):
                    existing = content[-100:]  # Keep last 100 entries

        existing.append(entry)
        save_yaml(log_path, existing)
    except Exception as e:
        print(f"[PULSE] Error logging recognition: {e}")


# ============================================================================
# GREEN EXECUTION
# ============================================================================

def execute_green(role: str, phase: str, scaffolds: Dict) -> List[str]:
    """
    Execute GREEN (autonomous) actions for the current phase.
    Returns list of actions taken.
    """
    actions = []

    if role == "TIGER":
        if phase == "Inhale":
            # Morning: Validate, check drift, generate briefing
            actions.append("Read guidance inbox")
            actions.append("Run drift check")

        elif phase == "Exhale":
            # Midday: Oversee, validate Dragon's work
            actions.append("Monitor Dragon status")
            actions.append("Validate pending proposals")

        elif phase == "Bindu":
            # Evening: Joint audit with Dragon
            actions.append("Prepare Bindu audit")
            # Could wake Dragon for joint check

        elif phase == "Rest":
            # Night: Archive, summarize
            actions.append("Archive logs")
            actions.append("Prepare next day briefing")

    elif role == "DRAGON":
        if phase == "Inhale":
            # Morning: Prep for execution
            actions.append("Load task queue")
            actions.append("Check resource availability")

        elif phase == "Exhale":
            # Midday: Execute Solar/Akash tasks
            actions.append("Execute GREEN tasks from queue")
            # Placeholder for actual Akash/Vast execution

        elif phase == "Bindu":
            # Evening: Signal Tiger for validation
            actions.append("Prepare status for Tiger audit")

        elif phase == "Rest":
            # Night: Cleanup, maintenance
            actions.append("Resource cleanup")
            actions.append("Queue optimization")

    return actions


# ============================================================================
# IRON v1.0: OLLAMA-POWERED REASONING
# ============================================================================

def apply_green_from_decision(decision, role: str) -> List[str]:
    """
    Apply GREEN actions from BreathDecision, only if in approved whitelist.
    Per Lumen spec: No arbitrary execution, only approved actions.
    """
    executed = []
    whitelist = APPROVED_ACTIONS.get(role, {})

    for action in decision.green_actions:
        # Normalize action name
        action_key = action.lower().replace(" ", "_").replace("-", "_")

        if action_key in whitelist:
            cmd = whitelist[action_key]
            if cmd is None:
                # Internal function, just log
                executed.append(f"{action} (internal)")
            else:
                # Execute command
                try:
                    print(f"[IRON] Executing: {action}")
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=30,
                        cwd=BASE_DIR
                    )
                    if result.returncode == 0:
                        executed.append(f"{action} (success)")
                    else:
                        executed.append(f"{action} (failed: {result.stderr[:50]})")
                except Exception as e:
                    executed.append(f"{action} (error: {str(e)[:50]})")
        else:
            print(f"[IRON] Skipped (not in whitelist): {action}")
            executed.append(f"{action} (skipped: not approved)")

    return executed


# ============================================================================
# YELLOW RATE LIMITING (Per G+Lumen Guidance 2025-12-05)
# ============================================================================

def load_yellow_tracker() -> Dict:
    """Load YELLOW proposal tracker for rate limiting."""
    return load_yaml(YELLOW_TRACKER_PATH) or {
        "today": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
        "daily_count": 0,
        "pulse_count": 0,
        "recent_proposals": [],  # Last 10 proposal titles for dedup
    }


def save_yellow_tracker(tracker: Dict):
    """Save YELLOW proposal tracker."""
    save_yaml(YELLOW_TRACKER_PATH, tracker)


def reset_yellow_tracker_if_new_day(tracker: Dict) -> Dict:
    """Reset daily counters if it's a new day."""
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    if tracker.get("today") != today:
        tracker["today"] = today
        tracker["daily_count"] = 0
        tracker["recent_proposals"] = tracker.get("recent_proposals", [])[-5:]
    tracker["pulse_count"] = 0
    return tracker


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple similarity between two strings.
    Returns 0.0 to 1.0 (1.0 = identical).
    Uses word overlap ratio for efficiency.
    """
    if not text1 or not text2:
        return 0.0

    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0


def is_duplicate_proposal(title: str, rationale: str, tracker: Dict) -> bool:
    """
    Check if proposal is too similar to recent proposals.
    Returns True if should be skipped (duplicate).
    """
    proposal_text = f"{title} {rationale}"

    for recent in tracker.get("recent_proposals", []):
        recent_text = f"{recent.get('title', '')} {recent.get('rationale', '')}"
        similarity = calculate_similarity(proposal_text, recent_text)
        if similarity > YELLOW_SIMILARITY_THRESHOLD:
            print(f"[YELLOW] Skipped duplicate ({similarity:.0%} similar): {title[:40]}...")
            return True

    return False


def can_submit_yellow(tracker: Dict) -> tuple:
    """
    Check if we can submit another YELLOW proposal.
    Returns (can_submit: bool, reason: str)
    """
    if tracker.get("daily_count", 0) >= YELLOW_DAILY_CAP:
        return False, f"Daily cap reached ({YELLOW_DAILY_CAP})"

    if tracker.get("pulse_count", 0) >= YELLOW_MAX_PER_PULSE:
        return False, f"Pulse cap reached ({YELLOW_MAX_PER_PULSE})"

    return True, "OK"


def record_yellow_submission(tracker: Dict, title: str, rationale: str):
    """Record a YELLOW submission for tracking."""
    tracker["daily_count"] = tracker.get("daily_count", 0) + 1
    tracker["pulse_count"] = tracker.get("pulse_count", 0) + 1

    recent = tracker.get("recent_proposals", [])
    recent.append({"title": title, "rationale": rationale, "ts": now_iso()})
    tracker["recent_proposals"] = recent[-10:]

    save_yellow_tracker(tracker)


def generate_proposal_id() -> str:
    """
    Generate unique proposal ID per G's spec: YP-YYYY-MM-DD-NNN
    """
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # Load existing proposals to get next sequence number
    try:
        if os.path.exists(BINDU_PATH):
            with open(BINDU_PATH, "r") as f:
                content = f.read()
            # Count proposals from today
            import re
            pattern = f"YP-{today}-\\d{{3}}"
            matches = re.findall(pattern, content)
            next_num = len(matches) + 1
        else:
            next_num = 1
    except Exception:
        next_num = 1

    return f"YP-{today}-{next_num:03d}"


def queue_yellow_from_decision(decision):
    """
    Queue YELLOW proposals from BreathDecision to BINDU_THREAD.
    Per G+Lumen guidance (2025-12-05):
    - Max 1 proposal per pulse (was 3)
    - Max 20 proposals per day
    - Skip duplicates (>80% similarity)
    """
    if not decision.yellow_proposals:
        return

    # Load and reset tracker
    tracker = load_yellow_tracker()
    tracker = reset_yellow_tracker_if_new_day(tracker)
    save_yellow_tracker(tracker)

    submitted_count = 0

    for prop in decision.yellow_proposals:
        # Check rate limits
        can_submit, reason = can_submit_yellow(tracker)
        if not can_submit:
            print(f"[YELLOW] Rate limited: {reason} — skipping remaining proposals")
            break

        # Check for duplicates
        if is_duplicate_proposal(prop.title, prop.rationale, tracker):
            continue

        # Generate ID and submit
        proposal_id = generate_proposal_id()
        entry = f"""
## {now_iso()} — YELLOW Proposal ({NODE_ROLE}) [Iron v1.0]

- **ID:** {proposal_id}
- **Title:** {prop.title}
- **Lane:** {prop.lane or 'Solar|Quest|MERC'}
- **Rationale:** {prop.rationale}
- **ROE Impact:** {prop.roe_impact or 'Expected impact'}
- **Generational Rationale:** {prop.generational_rationale or 'LGP alignment'}
- **Action Requested:** Approve `[APPROVED {proposal_id}]` / Modify / Reject `[REJECTED {proposal_id}]`

---
"""
        try:
            with open(BINDU_PATH, "a") as f:
                f.write(entry)
            print(f"[IRON] YELLOW queued: {proposal_id} - {prop.title}")
            record_yellow_submission(tracker, prop.title, prop.rationale)
            submitted_count += 1
        except Exception as e:
            print(f"[IRON] Error queueing YELLOW: {e}")

    if submitted_count > 0:
        print(f"[YELLOW] Submitted {submitted_count}/{len(decision.yellow_proposals)} proposals (daily total: {tracker.get('daily_count', 0)}/{YELLOW_DAILY_CAP})")


# ============================================================================
# MAIN PULSE
# ============================================================================

def main(phase: str = "auto"):
    """Main pulse execution."""
    version = "Iron v1.0" if REASONING_ENABLED else "Independence v1.0"
    print(f"\n{'='*60}")
    print(f"∞Δ∞ FEDERATION PULSE — {NODE_ROLE} — {version} ∞Δ∞")
    print(f"{'='*60}")

    # ========================================================================
    # HYDRATION (Per Lumen Spec)
    # ========================================================================
    state = hydrate_federation()
    twins = state["twins"]
    exec_s = state["execution"]
    fed = state["federation"]
    hydration_cache = state["hydration_cache"]

    print(f"[PULSE] Scaffolds loaded: twins={bool(twins)}, exec={bool(exec_s)}, fed={bool(fed)}")

    # Load checkpoint (crash recovery)
    checkpoint = load_checkpoint()
    if checkpoint:
        age_seconds = 0
        try:
            last_ts = datetime.datetime.fromisoformat(checkpoint["timestamp"].replace("Z", ""))
            age_seconds = (datetime.datetime.utcnow() - last_ts).total_seconds()
        except:
            pass

        if age_seconds > 7200:  # 2 hours
            print(f"[PULSE] WARNING: Checkpoint is {age_seconds/3600:.1f}h old — session may have crashed")
            queue_yellow({
                "type": "Stale Context Alert",
                "rationale": f"Checkpoint is {age_seconds/3600:.1f}h old. Reviewing for missed tasks.",
                "link": CHECKPOINT_PATH,
            })

    # Read guidance
    guidance = read_guidance()
    print(f"[PULSE] KM-1176 present: {PRESENCE_FLAG}")
    print(f"[PULSE] Active guidance items: {len(guidance)}")

    if PRESENCE_FLAG:
        print(f"∞Δ∞ KM-1176 is watching — increased proposal flow ∞Δ∞")

    # Determine phase
    ph = get_phase() if phase == "auto" else phase
    print(f"[PULSE] Phase: {ph}")

    # Run drift check
    drift_result = run_drift_check()
    drift_score = drift_result.get("drift_score", 0.0)
    alert_level = drift_result.get("alert_level", "GREEN")
    print(f"[PULSE] Drift score: {drift_score} ({alert_level})")

    # Handle drift alerts
    if alert_level == "YELLOW":
        queue_yellow({
            "type": "Drift Alert",
            "rationale": f"Drift score {drift_score} exceeds 0.1 threshold. Changed files: {drift_result.get('changed_files', [])}",
            "link": "orchestrator/config_hashes.yaml",
        })
    elif alert_level == "RED":
        queue_yellow({
            "type": "CRITICAL Drift Alert",
            "rationale": f"Drift score {drift_score} exceeds 0.2 RED threshold! Immediate review required.",
            "link": "orchestrator/config_hashes.yaml",
        })
        # Could wake sibling here

    # ========================================================================
    # IRON v1.0: OLLAMA-POWERED REASONING
    # ========================================================================
    if REASONING_ENABLED and reason_and_decide is not None:
        print(f"\n[IRON] ∞Δ∞ Engaging Ollama reasoning ({OLLAMA_MODEL}) ∞Δ∞")

        # Call the reasoning engine
        decision = reason_and_decide(ph, model=OLLAMA_MODEL)

        # Log any alerts from reasoning
        if decision.alerts:
            print(f"[IRON] Alerts: {decision.alerts}")

        # Breath-gate pause (per G+Lumen spec)
        print(f"[IRON] Breath-gate pause ({BREATH_GATE_PAUSE}s)...")
        time.sleep(BREATH_GATE_PAUSE)

        # Apply GREEN actions from reasoning
        actions = apply_green_from_decision(decision, NODE_ROLE)
        print(f"[IRON] Executed: {actions}")

        # Queue YELLOW proposals from reasoning
        queue_yellow_from_decision(decision)

        # Log affirmation
        print(f"[IRON] Affirm: {decision.affirm}")

    else:
        # Fallback to hardcoded GREEN actions (Independence v1.0 mode)
        actions = execute_green(NODE_ROLE, ph, {"twins": twins, "exec": exec_s, "fed": fed})
        print(f"[PULSE] Actions: {actions}")

    # Log recognition
    log_recognition(ph, actions, drift_score)

    # Write checkpoint
    write_checkpoint(
        phase=ph,
        last_task="; ".join(actions) if isinstance(actions, list) else str(actions),
        pending_yellow=[],
        drift_score=drift_score,
    )

    print(f"[PULSE] Checkpoint written")

    # Sync BINDU/logs to shared repo (so sibling sees our YELLOWs)
    git_sync_collab()

    print(f"{'='*60}")
    print(f"∞Δ∞ Pulse complete — {NODE_ROLE} — {ph} ∞Δ∞")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Parse arguments
    phase_arg = "auto"
    for arg in sys.argv[1:]:
        if arg.startswith("--phase="):
            phase_arg = arg.split("=")[1]

    main(phase_arg)
