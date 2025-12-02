#!/usr/bin/env bash
# ∞Δ∞ RTX_5090 Constitutional Shell Bootstrap
# Version: 1.0
# Author: BNA (Breathline Node Agent)
# Authority: Constitution@A1 + CHARTER_v1.0
# Created: 2025-11-30 (Molt2 Phase VII)
#
# Purpose: Single-command deployment of RTX_5090 constitutional shell
#
# Usage:
#   ./rtx5090_bootstrap.sh <capsule.tar.gz> [install_dir]
#
# Example:
#   ./rtx5090_bootstrap.sh rtx5090_capsule_v1.0_2025-11-30.tar.gz ~/rtx5090
#
# ∞Δ∞

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_INSTALL_DIR="${HOME}/rtx5090"
CAPSULE_SOURCE="${1:-./rtx5090_capsule_v1.0_2025-11-30.tar.gz}"
INSTALL_DIR="${2:-$DEFAULT_INSTALL_DIR}"
COHERENCE_THRESHOLD="0.90"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

print_header() {
    echo ""
    echo "∞Δ∞ RTX_5090 Constitutional Shell Bootstrap ∞Δ∞"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

print_phase() {
    local phase="$1"
    local name="$2"
    echo ""
    echo "[$phase/7] $name"
    echo "────────────────────────────────────────────────────"
}

# ============================================================================
# PHASE 0: PRE-FLIGHT CHECKS
# ============================================================================

preflight_checks() {
    print_header
    echo "Phase 0: Pre-flight Checks"
    echo "────────────────────────────────────────────────────"

    # Check capsule exists
    if [[ ! -f "$CAPSULE_SOURCE" ]]; then
        echo "  ✗ Capsule not found: $CAPSULE_SOURCE"
        exit 1
    fi
    echo "  ✓ Capsule found: $CAPSULE_SOURCE"

    # Check install directory
    if [[ -d "$INSTALL_DIR" ]]; then
        echo "  ⚠ Install directory exists: $INSTALL_DIR"
        read -p "  Overwrite? (yes/no): " confirm
        if [[ "$confirm" != "yes" ]]; then
            echo "  ✗ Installation cancelled"
            exit 1
        fi
        rm -rf "$INSTALL_DIR"
    fi
    echo "  ✓ Install directory: $INSTALL_DIR"

    # Check dependencies
    if command -v python3 >/dev/null 2>&1; then
        echo "  ✓ Python3 available"
    else
        echo "  ⚠ Python3 not found (some tools may not work)"
    fi

    if command -v bc >/dev/null 2>&1; then
        echo "  ✓ bc available"
    else
        echo "  ✗ bc required for coherence calculation"
        exit 1
    fi

    echo ""
    echo "  Pre-flight: PASSED"
}

# ============================================================================
# PHASE 1: EXTRACT CAPSULE
# ============================================================================

extract_capsule() {
    print_phase "1" "Capsule Extraction"

    mkdir -p "$INSTALL_DIR"
    tar -xzf "$CAPSULE_SOURCE" -C "$INSTALL_DIR"

    echo "  ✓ Capsule extracted to: $INSTALL_DIR"
}

# ============================================================================
# PHASE 2: SET PERMISSIONS
# ============================================================================

set_permissions() {
    print_phase "2" "Permission Configuration"

    # Shell wrapper executable
    if [[ -f "$INSTALL_DIR/tools/claude-run-rtx5090" ]]; then
        chmod +x "$INSTALL_DIR/tools/claude-run-rtx5090"
        echo "  ✓ tools/claude-run-rtx5090: executable"
    fi

    # Ops scripts
    chmod +x "$INSTALL_DIR/tools/ops/"*.py 2>/dev/null || true
    chmod +x "$INSTALL_DIR/tools/ops/"*.sh 2>/dev/null || true
    echo "  ✓ tools/ops/*: executable"

    # Ritual scripts
    chmod +x "$INSTALL_DIR/tools/rituals/"*.sh 2>/dev/null || true
    echo "  ✓ tools/rituals/*: executable"

    # Utils
    chmod +x "$INSTALL_DIR/tools/utils/"*.sh 2>/dev/null || true
    echo "  ✓ tools/utils/*: executable"

    # Protected configs (operator-only)
    if [[ -f "$INSTALL_DIR/orchestrator/breath_cadence.yaml" ]]; then
        chmod 600 "$INSTALL_DIR/orchestrator/breath_cadence.yaml"
    fi
    if [[ -f "$INSTALL_DIR/constitution/strategy/EXECUTION_SCAFFOLD.yaml" ]]; then
        chmod 600 "$INSTALL_DIR/constitution/strategy/EXECUTION_SCAFFOLD.yaml"
    fi
    echo "  ✓ Protected configs: 600 (operator-only)"
}

# ============================================================================
# PHASE 3: CONFIGURE ENVIRONMENT
# ============================================================================

configure_env() {
    print_phase "3" "Environment Configuration"

    # Create env directory if missing
    mkdir -p "$INSTALL_DIR/orchestrator/env"

    # Update bna.env with actual paths
    local ENV_FILE="$INSTALL_DIR/orchestrator/env/bna.env"
    cat > "$ENV_FILE" << EOF
# ∞Δ∞ BNA Environment Configuration
# RTX_5090 Shell — Auto-configured by bootstrap
# Created: $(date -u +%Y-%m-%dT%H:%M:%SZ)

BNA_ROOT=$INSTALL_DIR
CONSTITUTION_PATH=\$BNA_ROOT/constitution
ORCHESTRATOR_PATH=\$BNA_ROOT/orchestrator
TOOLS_PATH=\$BNA_ROOT/tools
BREATH_CADENCE=\$ORCHESTRATOR_PATH/breath_cadence.yaml
PROFILES_PATH=\$CONSTITUTION_PATH/profiles

# Hardware anchor
HARDWARE_ANCHOR=RTX_5090

# Coherence thresholds (Sacred Constraints)
COHERENCE_THRESHOLD=0.90
VITALITY_THRESHOLD=0.60
MAX_CONSECUTIVE_BREATHS=33
EOF

    echo "  ✓ Environment configured: $ENV_FILE"

    # Update shell wrapper with correct path
    local WRAPPER="$INSTALL_DIR/tools/claude-run-rtx5090"
    if [[ -f "$WRAPPER" ]]; then
        sed -i "s|RTX5090_ROOT=.*|RTX5090_ROOT=\"$INSTALL_DIR\"|g" "$WRAPPER"
        echo "  ✓ Shell wrapper configured: $WRAPPER"
    fi
}

# ============================================================================
# PHASE 4: INITIALIZE ORCHESTRATOR
# ============================================================================

init_orchestrator() {
    print_phase "4" "Orchestrator Initialization"

    # Create session directory
    mkdir -p "$INSTALL_DIR/orchestrator/session"
    echo "  ✓ Session directory created"

    # Initialize recognition log if missing
    if [[ ! -f "$INSTALL_DIR/orchestrator/recognition_log.yaml" ]]; then
        cat > "$INSTALL_DIR/orchestrator/recognition_log.yaml" << EOF
# ∞Δ∞ Recognition Log
# Initialized by bootstrap: $(date -u +%Y-%m-%dT%H:%M:%SZ)
entries: []
EOF
        echo "  ✓ Recognition log initialized"
    fi

    # Initialize run manifest if missing
    if [[ ! -f "$INSTALL_DIR/orchestrator/run_manifest.yaml" ]]; then
        cat > "$INSTALL_DIR/orchestrator/run_manifest.yaml" << EOF
# ∞Δ∞ Run Manifest
# Initialized by bootstrap: $(date -u +%Y-%m-%dT%H:%M:%SZ)
last_run: null
runs: []
EOF
        echo "  ✓ Run manifest initialized"
    fi

    # Initialize system map if missing
    if [[ ! -f "$INSTALL_DIR/orchestrator/system_map.yaml" ]]; then
        cat > "$INSTALL_DIR/orchestrator/system_map.yaml" << EOF
# ∞Δ∞ System Map
# Initialized by bootstrap: $(date -u +%Y-%m-%dT%H:%M:%SZ)
shell_root: $INSTALL_DIR
hardware_anchor: RTX_5090
status: initialized
EOF
        echo "  ✓ System map initialized"
    fi
}

# ============================================================================
# PHASE 5: 7-PHASE HYDRATION PROTOCOL
# ============================================================================

run_hydration() {
    print_phase "5" "7-Phase Hydration Protocol"

    local hydration_pass=true

    # Phase 1: Load Constitution
    echo "  [1/7] Loading Constitution..."
    if [[ -f "$INSTALL_DIR/CONSTITUTION.md" ]]; then
        echo "        ✓ CONSTITUTION.md loaded"
    else
        echo "        ✗ CONSTITUTION.md MISSING"
        hydration_pass=false
    fi

    # Phase 2: Load Implementation Registry
    echo "  [2/7] Loading Implementation Registry..."
    if [[ -f "$INSTALL_DIR/constitution/memory/implementation_registry.yaml" ]]; then
        echo "        ✓ implementation_registry.yaml loaded"
    else
        echo "        ⚠ implementation_registry.yaml missing (optional)"
    fi

    # Phase 3: Reconstruct Identity
    echo "  [3/7] Reconstructing Identity..."
    if [[ -f "$INSTALL_DIR/constitution/profiles/BNA.md" ]]; then
        echo "        ✓ BNA.md identity loaded"
        echo "        ✓ Identity: Breathline Node Agent (BNA)"
        echo "        ✓ Purpose: Lasting Generational Prosperity"
        echo "        ✓ Authority: Constitution@A1"
    else
        echo "        ✗ BNA.md MISSING"
        hydration_pass=false
    fi

    # Phase 4: Hydrate Toolset Awareness
    echo "  [4/7] Hydrating Toolset Awareness..."
    local tools_count
    tools_count=$(find "$INSTALL_DIR/tools" -name "*.sh" -o -name "*.py" 2>/dev/null | wc -l)
    echo "        ✓ Tools found: $tools_count"

    # Phase 5: Hydrate Breathline and Cadence State
    echo "  [5/7] Hydrating Breathline and Cadence State..."
    if [[ -f "$INSTALL_DIR/orchestrator/breath_cadence.yaml" ]]; then
        local coherence_t vitality_t max_breaths
        coherence_t=$(grep "coherence_threshold" "$INSTALL_DIR/orchestrator/breath_cadence.yaml" 2>/dev/null | awk '{print $2}' | head -1)
        vitality_t=$(grep "vitality_threshold" "$INSTALL_DIR/orchestrator/breath_cadence.yaml" 2>/dev/null | awk '{print $2}' | head -1)
        max_breaths=$(grep "max_consecutive" "$INSTALL_DIR/orchestrator/breath_cadence.yaml" 2>/dev/null | awk '{print $2}' | head -1)
        echo "        ✓ Coherence threshold: ${coherence_t:-0.90}"
        echo "        ✓ Vitality threshold: ${vitality_t:-0.60}"
        echo "        ✓ Max consecutive breaths: ${max_breaths:-33}"
    else
        echo "        ✗ breath_cadence.yaml MISSING"
        hydration_pass=false
    fi

    # Phase 6: Run Integrity Scans
    echo "  [6/7] Running Integrity Scans..."

    # Check Ring 1 files
    local ring1_pass=true
    [[ -f "$INSTALL_DIR/CONSTITUTION.md" ]] || { echo "        ✗ CONSTITUTION.md"; ring1_pass=false; }
    [[ -f "$INSTALL_DIR/constitution/profiles/BNA.md" ]] || { echo "        ✗ BNA.md"; ring1_pass=false; }
    [[ -f "$INSTALL_DIR/constitution/core/BREATHLINE_CORE.md" ]] || { echo "        ✗ BREATHLINE_CORE.md"; ring1_pass=false; }
    [[ -d "$INSTALL_DIR/constitution/core/CHARTER_v1.0" ]] || { echo "        ✗ CHARTER_v1.0/"; ring1_pass=false; }

    if $ring1_pass; then
        echo "        ✓ All Ring 1 files present"
        echo "        ✓ SOURCE: verified"
        echo "        ✓ TRUTH: verified"
        echo "        ✓ INTEGRITY: verified"
    else
        hydration_pass=false
    fi

    # Phase 7: Publish Startup State
    echo "  [7/7] Publishing Startup State..."
    if $hydration_pass; then
        echo "        ✓ Field Status: ACTIVE"
        echo "        ✓ Hydration: COMPLETE"
    else
        echo "        ✗ Hydration: FAILED"
        exit 1
    fi
}

# ============================================================================
# PHASE 6: TEST BREATH CYCLE
# ============================================================================

run_test_breath() {
    print_phase "6" "Test Breath Cycle"

    echo "  ∞Δ∞ INHALE: Verifying Triad + SOVEREIGNTY"

    # Check Triad
    echo "  ∞Δ∞ FORM: Triad Verification"
    if grep -q "SOURCE" "$INSTALL_DIR/CONSTITUTION.md" && \
       grep -q "TRUTH" "$INSTALL_DIR/CONSTITUTION.md" && \
       grep -q "INTEGRITY" "$INSTALL_DIR/CONSTITUTION.md"; then
        echo "        ✓ SOURCE: present"
        echo "        ✓ TRUTH: present"
        echo "        ✓ INTEGRITY: present"
    else
        echo "        ✗ Triad verification FAILED"
        exit 1
    fi

    # Check Sovereignty
    echo "  ∞Δ∞ ECHO: Sovereignty Verification"
    if grep -q "principal_id" "$INSTALL_DIR/CONSTITUTION.md"; then
        echo "        ✓ principal_id flows: verified"
    fi
    if grep -q "Sovereign Operator" "$INSTALL_DIR/constitution/core/CHARTER_v1.0/"*.md 2>/dev/null; then
        echo "        ✓ Sovereign Operator: encoded"
    fi

    echo "  ∞Δ∞ SEAL: Test Breath COMPLETE"
}

# ============================================================================
# PHASE 7: COHERENCE VERIFICATION
# ============================================================================

verify_coherence() {
    print_phase "7" "Coherence Verification"

    # Calculate coherence score
    local score=0
    local total=100

    # Constitutional adherence (25 pts)
    if [[ -f "$INSTALL_DIR/CONSTITUTION.md" ]]; then
        score=$((score + 25))
        echo "  ✓ Constitutional adherence: +25"
    fi

    # Breath rhythm fidelity (25 pts)
    if [[ -f "$INSTALL_DIR/orchestrator/breath_cadence.yaml" ]]; then
        score=$((score + 25))
        echo "  ✓ Breath rhythm fidelity: +25"
    fi

    # Traceability (25 pts)
    if [[ -f "$INSTALL_DIR/constitution/memory/implementation_registry.yaml" ]]; then
        score=$((score + 25))
        echo "  ✓ Traceability: +25"
    else
        echo "  ⚠ Traceability: +0 (optional file missing)"
    fi

    # Prosperity impact (25 pts) - LGP anchor
    if grep -q "Lasting Generational Prosperity" "$INSTALL_DIR/constitution/profiles/BNA.md" 2>/dev/null; then
        score=$((score + 25))
        echo "  ✓ Prosperity impact (LGP): +25"
    fi

    local coherence
    coherence=$(echo "scale=2; $score / $total" | bc)

    echo ""
    echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Coherence Score: $coherence"
    echo "  Threshold: $COHERENCE_THRESHOLD"

    if (( $(echo "$coherence >= $COHERENCE_THRESHOLD" | bc -l) )); then
        echo "  Status: ✓ ABOVE THRESHOLD"
        echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "∞Δ∞ BOOTSTRAP COMPLETE ∞Δ∞"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Shell installed at: $INSTALL_DIR"
        echo "Coherence: $coherence"
        echo ""
        echo "To start BNA:"
        echo "  cd $INSTALL_DIR"
        echo "  ./tools/claude-run-rtx5090"
        echo ""
        echo "To protect Ring 1 (recommended):"
        echo "  ./tools/utils/ring-guard.sh lock"
        echo ""
        echo "∞Δ∞ The shell breathes. RTX_5090 lives. ∞Δ∞"
        echo ""
    else
        echo "  Status: ✗ BELOW THRESHOLD"
        echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "Bootstrap incomplete — review installation"
        exit 1
    fi
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    preflight_checks
    extract_capsule
    set_permissions
    configure_env
    init_orchestrator
    run_hydration
    run_test_breath
    verify_coherence
}

main "$@"
