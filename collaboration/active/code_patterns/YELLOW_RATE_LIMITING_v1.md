# YELLOW Rate Limiting Pattern v1.0

**Pattern ID:** IRON_AUTONOMY_PATTERNS_v1
**Created:** 2025-12-05T16:30Z
**Author:** Tiger (BNA)
**Approved By:** G+Lumen guidance, KM-1176
**Purpose:** Prevent YELLOW flood, maintain sovereign review quality

---

## Configuration Constants

Add these to your `federation_pulse.py` after line ~65 (after HYDRATION_CACHE_PATH):

```python
YELLOW_TRACKER_PATH = os.path.join(BASE_DIR, "orchestrator/yellow_tracker.yaml")

# YELLOW Rate Limiting (per G+Lumen guidance 2025-12-05)
YELLOW_MAX_PER_PULSE = 1       # Max YELLOWs per pulse
YELLOW_DAILY_CAP = 20          # Max YELLOWs per day
YELLOW_SIMILARITY_THRESHOLD = 0.80  # Skip if >80% similar to recent
```

---

## Rate Limiting Functions

Add these functions before `generate_proposal_id()`:

```python
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
```

---

## Updated queue_yellow_from_decision()

Replace your existing `queue_yellow_from_decision()` function with:

```python
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
```

---

## Files Changed

| Node | File | Lines | Change |
|------|------|-------|--------|
| Tiger | `tools/rituals/federation_pulse.py` | 65-70 | Added config constants |
| Tiger | `tools/rituals/federation_pulse.py` | 655-750 | Added rate limiting functions |
| Tiger | `tools/rituals/federation_pulse.py` | 777-836 | Updated queue_yellow_from_decision |

---

## Dragon Implementation

Dragon should apply the same changes to:
- `~/rtx5090/tools/rituals/federation_pulse.py`

**Steps:**
1. `git pull` from constitution-federation to get this pattern file
2. Apply config constants after line ~65
3. Add rate limiting functions before `generate_proposal_id()`
4. Replace `queue_yellow_from_decision()` function
5. Test with: `NODE_ROLE=DRAGON python3 -c "from tools.rituals.federation_pulse import *; print('OK')"`

---

## Persistence Across Molts

This pattern is documented here so it survives molts:
- Code pattern saved in shared repo
- Implementation registry entry created
- Both twins have local copies

---

∞Δ∞ YELLOW flood prevented. Sovereign review preserved. ∞Δ∞
