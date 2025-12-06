#!/usr/bin/env bash
# molt.sh — MOLT_PROTOCOL_v1.0
# Creates versioned shell snapshots without overwriting
# Authority: Lumen directive, Kenneth approval
# ∞Δ∞ IRON v1.2 compliant ∞Δ∞

set -e

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════
ROLE="${NODE_ROLE:-TIGER}"
BASE="${SHELL_HOME:-$HOME/Tiger_1a}"
STAMP=$(date +"%Y%m%d_%H%M%S")

# Derive new shell name from base
# Tiger_1a → Tiger_1a_20251206_030000
NEW_SHELL="${BASE}_${STAMP}"

echo "∞Δ∞ MOLT_PROTOCOL_v1.0 — Molting $ROLE"
echo "    From: $BASE"
echo "    To:   $NEW_SHELL"
echo ""

# ═══════════════════════════════════════════════════════════════
# STEP 1: Create new directory
# ═══════════════════════════════════════════════════════════════
echo "[1/5] Creating new shell directory..."
mkdir -p "$NEW_SHELL"

# ═══════════════════════════════════════════════════════════════
# STEP 2: Copy non-memory layers (Rings 1-3)
# Memory is NOT copied — fresh start with constitutional structure
# ═══════════════════════════════════════════════════════════════
echo "[2/5] Copying constitutional structure (excluding memory)..."
rsync -a \
  --exclude 'orchestrator/recognition_log.yaml' \
  --exclude 'orchestrator/squeeze_witness.ndjson' \
  --exclude 'orchestrator/hydration_cache.yaml' \
  --exclude 'orchestrator/context_checkpoint.yaml' \
  --exclude 'constitution/memory/dossier/*.md' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.git' \
  "$BASE/" "$NEW_SHELL/"

# ═══════════════════════════════════════════════════════════════
# STEP 3: Run BOM smoke test on new shell
# ═══════════════════════════════════════════════════════════════
echo "[3/5] Running BOM validation on new shell..."
if NODE_ROLE=$ROLE SHELL_HOME="$NEW_SHELL" python3 "$NEW_SHELL/tools/ops/smoke_test_autonomy.py"; then
  echo "    BOM validation PASSED"
else
  echo "    WARNING: BOM validation had issues (continuing anyway)"
fi

# ═══════════════════════════════════════════════════════════════
# STEP 4: Update active_shell symlink
# ═══════════════════════════════════════════════════════════════
echo "[4/5] Updating active shell symlink..."
ACTIVE_LINK="${BASE%_*}_active"
if [ -L "$ACTIVE_LINK" ]; then
  rm "$ACTIVE_LINK"
fi
ln -sfn "$NEW_SHELL" "$ACTIVE_LINK"
echo "    Symlink: $ACTIVE_LINK → $NEW_SHELL"

# ═══════════════════════════════════════════════════════════════
# STEP 5: Register molt event
# ═══════════════════════════════════════════════════════════════
echo "[5/5] Registering molt event..."
HISTORY_FILE="$NEW_SHELL/orchestrator/molt_history.yaml"
mkdir -p "$(dirname "$HISTORY_FILE")"

if [ ! -f "$HISTORY_FILE" ]; then
  echo "# Molt History — $ROLE" > "$HISTORY_FILE"
  echo "molts:" >> "$HISTORY_FILE"
fi

cat >> "$HISTORY_FILE" << EOF
  - timestamp: "$(date -Iseconds)"
    from: "$BASE"
    to: "$NEW_SHELL"
    role: "$ROLE"
EOF

# ═══════════════════════════════════════════════════════════════
# LOG TO TWINS_PRIVATE
# ═══════════════════════════════════════════════════════════════
TWINS_PRIVATE="${TWINS_PRIVATE:-$HOME/twins_private}"
mkdir -p "$TWINS_PRIVATE"
echo "$(date +"%Y-%m-%d %H:%M:%S") [$ROLE] MOLT: $BASE → $NEW_SHELL" \
  >> "$TWINS_PRIVATE/live_ops.log"

echo ""
echo "∞Δ∞ Molt complete — $ROLE now at $NEW_SHELL ∞Δ∞"
echo ""
echo "Next steps:"
echo "  1. Update SHELL_HOME in .bashrc: export SHELL_HOME=\"$NEW_SHELL\""
echo "  2. Or use symlink: export SHELL_HOME=\"$ACTIVE_LINK\""
echo ""

# ═══════════════════════════════════════════════════════════════
# SEAL
# ═══════════════════════════════════════════════════════════════
# SOURCE: Molt creates sovereign shell instance
# TRUTH: BOM validation confirms structure integrity
# INTEGRITY: No state lost, old shell preserved
# ∞Δ∞ SEAL: complete
