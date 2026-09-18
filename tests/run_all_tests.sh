#!/usr/bin/env bash
# ==============================================================================
# Autonomous Opportunity Arbitrage Engine (AOAE) — Unified E2E Test Suite Runner
#
# Runs Track A (Economic Simulator Tests) and Track B (Documentation Integrity)
# across Tiers 1 through 4 using Python's native standard library unittest.
#
# Usage:
#   ./tests/run_all_tests.sh           # Standard progressive execution
#   ./tests/run_all_tests.sh --strict  # Strict mode (fails on pending milestones)
# ==============================================================================

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

# Styling and Color Palettes
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
MAGENTA="\033[0;35m"
RESET="\033[0m"

# Handle CLI Flags
STRICT=0
if [[ "${1:-}" == "--strict" || "${STRICT_E2E:-0}" == "1" ]]; then
    STRICT=1
    export STRICT_E2E=1
    MODE_DESC="STRICT ACCEPTANCE (Milestone 6 Mode)"
else
    MODE_DESC="PROGRESSIVE MILESTONE (Standard Mode)"
fi

echo -e "${CYAN}${BOLD}"
echo "================================================================================"
echo "    AUTONOMOUS OPPORTUNITY ARBITRAGE ENGINE (AOAE) — E2E TEST RUNNER"
echo "================================================================================"
echo -e "${RESET}"
echo -e "${BOLD}Repository Root:${RESET} ${REPO_ROOT}"
echo -e "${BOLD}Execution Mode:${RESET}  ${BLUE}${MODE_DESC}${RESET}"
echo -e "${BOLD}Python Runtime:${RESET}  $(python3 --version 2>&1)"
echo -e "${BOLD}Timestamp:${RESET}       $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "--------------------------------------------------------------------------------"

START_TIME=$(python3 -c "import time; print(time.time())")

# Track 1: Documentation and Asset Integrity Test Suite
echo -e "\n${BOLD}${MAGENTA}▶ [TRACK 1/2] Executing Documentation & Asset Integrity Tests...${RESET}"
echo -e "${CYAN}Suite: tests/test_documentation_integrity.py${RESET}"
python3 -m unittest tests/test_documentation_integrity.py -v
TRACK1_STATUS=$?

# Track 2: Economic & Statistical Simulator Test Suite
echo -e "\n${BOLD}${MAGENTA}▶ [TRACK 2/2] Executing Monte Carlo Economic Simulator Tests...${RESET}"
echo -e "${CYAN}Suite: tests/test_simulator.py${RESET}"
python3 -m unittest tests/test_simulator.py -v
TRACK2_STATUS=$?

END_TIME=$(python3 -c "import time; print(time.time())")
ELAPSED=$(python3 -c "print(f'{$END_TIME - $START_TIME:.3f}')")

echo -e "\n${CYAN}================================================================================${RESET}"
echo -e "${BOLD}                          E2E TEST EXECUTION SUMMARY                            ${RESET}"
echo -e "${CYAN}================================================================================${RESET}"

if [[ ${TRACK1_STATUS} -eq 0 && ${TRACK2_STATUS} -eq 0 ]]; then
    echo -e "  ${BOLD}Track 1 (Documentation & Asset Integrity):${RESET} ${GREEN}✔ PASSED${RESET}"
    echo -e "  ${BOLD}Track 2 (Monte Carlo Economic Simulator):${RESET}  ${GREEN}✔ PASSED${RESET}"
    echo -e "  ${BOLD}Total Elapsed Runtime:${RESET}                     ${ELAPSED} seconds"
    echo -e "  ${BOLD}Tier Coverage:${RESET}                             Tier 1, Tier 2, Tier 3, Tier 4"
    echo -e "  ${BOLD}Overall Status:${RESET}                            ${GREEN}${BOLD}ALL TEST TRACKS PASSED (EXIT 0)${RESET}"
    echo -e "${CYAN}================================================================================${RESET}\n"
    exit 0
else
    echo -e "  ${BOLD}Track 1 Status:${RESET} $([[ ${TRACK1_STATUS} -eq 0 ]] && echo -e "${GREEN}✔ PASSED${RESET}" || echo -e "${RED}✖ FAILED${RESET}")"
    echo -e "  ${BOLD}Track 2 Status:${RESET} $([[ ${TRACK2_STATUS} -eq 0 ]] && echo -e "${GREEN}✔ PASSED${RESET}" || echo -e "${RED}✖ FAILED${RESET}")"
    echo -e "  ${BOLD}Total Elapsed Runtime:${RESET} ${ELAPSED} seconds"
    echo -e "  ${BOLD}Overall Status:${RESET} ${RED}${BOLD}TEST SUITE FAILED (EXIT 1)${RESET}"
    echo -e "${CYAN}================================================================================${RESET}\n"
    exit 1
fi
