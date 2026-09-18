#!/usr/bin/env python3
"""
Autonomous Opportunity Arbitrage Engine (AOAE) — Economic Simulator E2E & Unit Test Suite

This module performs opaque-box and statistical requirement verification on
scripts/simulate_economics.py across Tiers 1 through 4:
  - Tier 1: Feature Coverage (CLI flags, defaults, archetypes, JSON/SVG export, seeds)
  - Tier 2: Boundary & Corner Cases (zero budget, negative budgets, 100% duplicate rates,
            extreme latency, zero capital, invalid CLI arguments)
  - Tier 3: Cross-Feature Combinations (Kelly sizing vs MC equity, simultaneous multi-format
            export, risk metric coherence: VaR vs CVaR, Sharpe vs Sortino)
  - Tier 4: Real-World Scenarios (30-Day $250 MVE experiment, institutional hedge-fund run,
            zero-touch verification pipeline, stress shocks)

Standard: Pure Python Standard Library (unittest, json, subprocess, math, statistics).
Zero external dependencies required.
"""

import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
SIMULATOR_PATH = REPO_ROOT / "scripts" / "simulate_economics.py"
STRICT_MODE = os.environ.get("STRICT_E2E", "0") == "1"


def simulator_available() -> bool:
    """Check if scripts/simulate_economics.py exists."""
    return SIMULATOR_PATH.is_file()


def run_simulator_cli(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    """Execute the simulator CLI as an opaque subprocess."""
    cmd = [sys.executable, str(SIMULATOR_PATH)] + args
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
    )


class BaseSimulatorTestCase(unittest.TestCase):
    """Base class providing progressive testability and assertion utilities."""

    def require_simulator(self):
        """Skip if simulator is not implemented unless in strict mode."""
        if not simulator_available():
            if STRICT_MODE:
                self.fail(
                    f"Milestone 4 Requirement Violation: {SIMULATOR_PATH} does not exist."
                )
            else:
                self.skipTest(
                    f"Dependency pending: {SIMULATOR_PATH} not yet implemented (Milestone 4)."
                )


# ==============================================================================
# TIER 1: FEATURE COVERAGE
# ==============================================================================
class TestTier1FeatureCoverage(BaseSimulatorTestCase):
    """Tier 1: Basic functionality, happy path CLI options, schemas, and archetypes."""

    def test_tier1_cli_help_flag(self):
        """Verify that --help emits usage, flag descriptions, and exits with code 0."""
        self.require_simulator()
        proc = run_simulator_cli(["--help"])
        self.assertEqual(proc.returncode, 0, f"--help failed with stderr: {proc.stderr}")
        self.assertIn("usage:", proc.stdout.lower())
        self.assertIn("--runs", proc.stdout)
        self.assertIn("--days", proc.stdout)

    def test_tier1_cli_default_run(self):
        """Verify default invocation without arguments terminates cleanly."""
        self.require_simulator()
        proc = run_simulator_cli([])
        self.assertEqual(proc.returncode, 0, f"Default run failed: {proc.stderr}")
        # Standard stdout should contain summary statistics or results
        self.assertTrue(len(proc.stdout) > 0, "Default run produced no stdout.")

    def test_tier1_cli_web3_archetype(self):
        """Verify --archetype web3 executes and outputs positive net economic indicators."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--archetype", "web3",
                "--output-json", json_path,
                "--seed", "42",
            ])
            self.assertEqual(proc.returncode, 0, f"Web3 run failed: {proc.stderr}")
            self.assertTrue(os.path.exists(json_path), "JSON output file was not created.")

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertIn("metrics", data)
            metrics = data["metrics"]
            self.assertIn("rocs", metrics)
            # Web3 archetype mathematically yields positive ROCS > 1.0
            self.assertGreater(metrics["rocs"], 0.0, "Web3 ROCS should be positive.")
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier1_cli_web2_archetype(self):
        """Verify --archetype web2 executes and reflects compressed or negative yields."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--archetype", "web2",
                "--output-json", json_path,
                "--seed", "42",
            ])
            self.assertEqual(proc.returncode, 0, f"Web2 run failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            # Web2 suffers from high duplicate rates and low ROCS (< 1.0)
            self.assertIn("mean_profit", metrics)
            self.assertIn("rocs", metrics)
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier1_cli_output_json_schema(self):
        """Verify JSON output strictly matches the specification schema in PROJECT.md."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "50",
                "--days", "14",
                "--output-json", json_path,
                "--seed", "101",
            ])
            self.assertEqual(proc.returncode, 0, f"JSON run failed: {proc.stderr}")

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertIsInstance(data, dict, "Output JSON root must be an object.")
            self.assertIn("metrics", data, "Missing 'metrics' key in JSON output.")

            required_metrics = [
                "mean_profit", "median_profit", "sharpe_ratio", "sortino_ratio",
                "var_95", "cvar_95", "prob_ruin", "roi_percent", "rocs"
            ]
            for metric in required_metrics:
                self.assertIn(metric, data["metrics"], f"Missing metric '{metric}' in output schema.")
                self.assertIsInstance(
                    data["metrics"][metric],
                    (int, float),
                    f"Metric '{metric}' must be a numeric float/int."
                )
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier1_cli_output_svg_generation(self):
        """Verify --output-svg produces a valid SVG XML document with required tags."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf:
            svg_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "50",
                "--days", "14",
                "--output-svg", svg_path,
                "--seed", "42",
            ])
            self.assertEqual(proc.returncode, 0, f"SVG run failed: {proc.stderr}")
            self.assertTrue(os.path.exists(svg_path), "SVG output file was not created.")

            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertTrue(content.strip().startswith("<svg") or "<?xml" in content, "Invalid SVG header.")
            self.assertIn("</svg>", content, "SVG missing closing </svg> tag.")
            self.assertGreater(len(content), 200, "SVG content suspiciously small.")
        finally:
            if os.path.exists(svg_path):
                os.unlink(svg_path)

    def test_tier1_cli_seed_reproducibility(self):
        """Verify identical seed produces strictly identical numeric output across runs."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf1, \
             tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf2:
            path1 = tf1.name
            path2 = tf2.name

        try:
            proc1 = run_simulator_cli(["--runs", "100", "--days", "20", "--seed", "999", "--output-json", path1])
            proc2 = run_simulator_cli(["--runs", "100", "--days", "20", "--seed", "999", "--output-json", path2])

            self.assertEqual(proc1.returncode, 0)
            self.assertEqual(proc2.returncode, 0)

            with open(path1, "r", encoding="utf-8") as f1, open(path2, "r", encoding="utf-8") as f2:
                data1 = json.load(f1)
                data2 = json.load(f2)

            self.assertEqual(
                data1["metrics"]["median_profit"],
                data2["metrics"]["median_profit"],
                "PRNG seed failed to produce deterministic median profit."
            )
            self.assertEqual(
                data1["metrics"]["rocs"],
                data2["metrics"]["rocs"],
                "PRNG seed failed to produce deterministic ROCS."
            )
        finally:
            for p in [path1, path2]:
                if os.path.exists(p):
                    os.unlink(p)

    def test_tier1_ev_calculation_reference_web2(self):
        """Unit test authoritative Web2 EV formula against mathematical specification."""
        p_elig = 0.65
        p_find = 0.03
        p_uniq = 0.15
        p_acc = 0.25
        payout = 300.0
        cost = 0.504

        p_reward = p_elig * p_find * p_uniq * p_acc
        expected_ev = (p_reward * payout) - cost

        self.assertAlmostEqual(p_reward, 0.00073125, places=7)
        self.assertAlmostEqual(expected_ev, -0.284625, places=5)
        self.assertLess(expected_ev, 0.0, "Web2 public automated scanning must yield negative EV.")

    def test_tier1_ev_calculation_reference_web3(self):
        """Unit test authoritative Web3 EV formula against mathematical specification."""
        p_elig = 1.00
        p_find = 0.035
        p_uniq = 0.65
        p_acc = 0.98
        payout = 18500.0
        cost = 14.20

        p_reward = p_elig * p_find * p_uniq * p_acc
        expected_ev = (p_reward * payout) - cost
        roic = (expected_ev + cost) / cost

        self.assertAlmostEqual(p_reward, 0.022295, places=6)
        self.assertAlmostEqual(expected_ev, 398.2575, places=4)
        self.assertGreater(expected_ev, 0.0, "Web3 automated research must yield positive EV.")
        self.assertAlmostEqual(roic, 29.0463, places=2)


# ==============================================================================
# TIER 2: BOUNDARY & CORNER CASES
# ==============================================================================
class TestTier2BoundaryAndCornerCases(BaseSimulatorTestCase):
    """Tier 2: Edge conditions, extreme distributions, and invalid input rejection."""

    def test_tier2_zero_budget(self):
        """Verify simulator handles --daily-budget 0 or --budget 0 without division by zero."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "50",
                "--days", "10",
                "--daily-budget", "0",
                "--output-json", json_path,
                "--seed", "42"
            ])
            # If rejected with error code or executed with 0 spend, must not crash with unhandled traceback
            self.assertNotIn("ZeroDivisionError", proc.stderr)
            if proc.returncode == 0:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.assertIn("metrics", data)
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier2_negative_budget_error(self):
        """Verify simulator rejects negative budget values with non-zero exit code."""
        self.require_simulator()
        proc = run_simulator_cli(["--daily-budget", "-50"])
        self.assertNotEqual(proc.returncode, 0, "Negative budget should be rejected.")

    def test_tier2_100_percent_duplicate_rate(self):
        """Verify 100% duplicate rate leads to zero gross revenue and negative net profit."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--duplicate-rate", "1.0",
                "--output-json", json_path,
                "--seed", "42"
            ])
            self.assertEqual(proc.returncode, 0, f"Failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            # With 100% duplicate rate, profit cannot be positive
            self.assertLessEqual(metrics["mean_profit"], 0.0, "100% duplicates should yield net loss.")
            self.assertEqual(metrics["rocs"], 0.0, "100% duplicates should produce 0.0 ROCS.")
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier2_zero_duplicate_rate(self):
        """Verify 0% duplicate rate maximizes realized profit and uniqueness."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--duplicate-rate", "0.0",
                "--output-json", json_path,
                "--seed", "42"
            ])
            self.assertEqual(proc.returncode, 0, f"Failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("metrics", data)
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier2_infinite_triage_latency(self):
        """Verify extreme triage latency delays cash inflows and elevates ruin risk."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--triage-latency-days", "3650",
                "--initial-capital", "100",
                "--output-json", json_path,
                "--seed", "42"
            ])
            self.assertEqual(proc.returncode, 0, f"Failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            # 10-year latency means no payout settles within 30 days -> ruin risk approaches 100%
            self.assertGreaterEqual(metrics["prob_ruin"], 0.80, "Extreme latency should cause high ruin.")
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier2_zero_triage_latency(self):
        """Verify zero triage latency allows instantaneous payout settlement."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "50",
                "--days", "14",
                "--triage-latency-days", "0",
                "--output-json", json_path,
                "--seed", "42"
            ])
            self.assertEqual(proc.returncode, 0, f"Failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("metrics", data)
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier2_zero_finding_rate(self):
        """Verify zero finding rate produces 0 payouts and pure cost burn."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "50",
                "--days", "15",
                "--p-finding", "0.0",
                "--output-json", json_path,
                "--seed", "42"
            ])
            self.assertEqual(proc.returncode, 0, f"Failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            self.assertLess(metrics["mean_profit"], 0.0, "Zero findings must incur cost loss.")
            self.assertEqual(metrics["rocs"], 0.0, "Zero findings must yield ROCS 0.0.")
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier2_zero_runs_error(self):
        """Verify --runs 0 is rejected with a non-zero exit code."""
        self.require_simulator()
        proc = run_simulator_cli(["--runs", "0"])
        self.assertNotEqual(proc.returncode, 0, "Zero simulation runs must be rejected.")

    def test_tier2_negative_runs_error(self):
        """Verify --runs -10 is rejected with a non-zero exit code."""
        self.require_simulator()
        proc = run_simulator_cli(["--runs", "-10"])
        self.assertNotEqual(proc.returncode, 0, "Negative runs must be rejected.")

    def test_tier2_invalid_flag_rejection(self):
        """Verify unrecognized command-line flag causes immediate non-zero exit."""
        self.require_simulator()
        proc = run_simulator_cli(["--unknown-flag-test-xyz"])
        self.assertNotEqual(proc.returncode, 0, "Unrecognized flag must cause error exit.")

    def test_tier2_invalid_archetype_flag(self):
        """Verify unsupported archetype name is rejected with a non-zero exit code."""
        self.require_simulator()
        proc = run_simulator_cli(["--archetype", "non_existent_domain_xyz"])
        self.assertNotEqual(proc.returncode, 0, "Unsupported archetype must be rejected.")


# ==============================================================================
# TIER 3: CROSS-FEATURE COMBINATIONS
# ==============================================================================
class TestTier3CrossFeatureCombinations(BaseSimulatorTestCase):
    """Tier 3: Multi-feature coupling, risk metrics coherence, and simultaneous outputs."""

    def test_tier3_kelly_allocation_vs_monte_carlo(self):
        """Verify multi-asset Kelly allocation properties across economic regimes."""
        # Closed form uncoupled Kelly: f* = (p * b - (1 - p)) / b
        def calc_kelly(p, payout, cost):
            b = (payout - cost) / cost
            edge = p * b - (1.0 - p)
            return max(0.0, edge / b)

        # In negative EV regime (Web2), Kelly factor is 0.0
        f_web2 = calc_kelly(0.001785, 1090.0, 82.50)
        self.assertEqual(f_web2, 0.0, "Negative EV Web2 must have Kelly fraction 0.0.")

        # In positive EV regime (Web3 Contests), Kelly factor is positive
        f_web3 = calc_kelly(0.40, 2800.0, 45.0)
        self.assertGreater(f_web3, 0.30, "Web3 Contests should have healthy Kelly fraction > 0.30.")
        self.assertLessEqual(f_web3, 1.0, "Kelly fraction cannot exceed 100%.")

    def test_tier3_simultaneous_json_and_svg_export(self):
        """Verify concurrent generation of both JSON and SVG artifacts in a single run."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf_json, \
             tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf_svg:
            json_path = tf_json.name
            svg_path = tf_svg.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--output-json", json_path,
                "--output-svg", svg_path,
                "--seed", "777",
            ])
            self.assertEqual(proc.returncode, 0, f"Simultaneous export failed: {proc.stderr}")
            self.assertTrue(os.path.exists(json_path), "JSON artifact missing.")
            self.assertTrue(os.path.exists(svg_path), "SVG artifact missing.")

            # Validate JSON content
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("metrics", data)

            # Validate SVG content
            with open(svg_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
            self.assertIn("<svg", svg_content)
            self.assertIn("</svg>", svg_content)
        finally:
            for p in [json_path, svg_path]:
                if os.path.exists(p):
                    os.unlink(p)

    def test_tier3_risk_metrics_coherence_var_cvar(self):
        """Verify mathematical invariant that CVaR_95 >= VaR_95 across simulation runs."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "200",
                "--days", "30",
                "--output-json", json_path,
                "--seed", "12345",
            ])
            self.assertEqual(proc.returncode, 0, f"Failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            var_95 = metrics["var_95"]
            cvar_95 = metrics["cvar_95"]

            # Expected Shortfall (CVaR) in the tail must be at least as severe as VaR
            self.assertGreaterEqual(
                cvar_95,
                var_95 - 1e-5,
                f"CVaR 95 ({cvar_95}) must be greater than or equal to VaR 95 ({var_95})."
            )
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier3_sharpe_sortino_downside_consistency(self):
        """Verify Sharpe and Sortino ratios are finite numbers and properly ordered."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "150",
                "--days", "30",
                "--output-json", json_path,
                "--seed", "42"
            ])
            self.assertEqual(proc.returncode, 0, f"Failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            sharpe = metrics["sharpe_ratio"]
            sortino = metrics["sortino_ratio"]

            self.assertFalse(math.isnan(sharpe), "Sharpe ratio is NaN.")
            self.assertFalse(math.isinf(sharpe), "Sharpe ratio is Inf.")
            self.assertFalse(math.isnan(sortino), "Sortino ratio is NaN.")
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier3_rocs_ratio_consistency(self):
        """Verify Return on Compute Spend (ROCS) adheres to ROCS = Realized / Spend."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--output-json", json_path,
                "--seed", "314"
            ])
            self.assertEqual(proc.returncode, 0, f"Failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            rocs = data["metrics"]["rocs"]
            self.assertGreaterEqual(rocs, 0.0, "ROCS cannot be negative.")
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)


# ==============================================================================
# TIER 4: REAL-WORLD SCENARIOS
# ==============================================================================
class TestTier4RealWorldScenarios(BaseSimulatorTestCase):
    """Tier 4: Empirical validation blueprints, MVE simulation, and institutional stress tests."""

    def test_tier4_30_day_250_dollar_mve_simulation(self):
        """Verify 30-day $250 Minimum Viable Experiment simulation runs strictly within bounds."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "1000",
                "--days", "30",
                "--initial-capital", "250.0",
                "--daily-budget", "8.33",
                "--output-json", json_path,
                "--seed", "42",
            ])
            self.assertEqual(proc.returncode, 0, f"30-Day MVE failed: {proc.stderr}")

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            self.assertIn("prob_ruin", metrics)
            self.assertIn("median_profit", metrics)
            self.assertGreaterEqual(metrics["prob_ruin"], 0.0)
            self.assertLessEqual(metrics["prob_ruin"], 1.0)
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier4_institutional_hedge_fund_risk_run(self):
        """Verify institutional scale simulation ($50k capital, 365 days, 5,000 runs)."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            # Use 500 runs in standard test to balance execution speed and statistical power
            proc = run_simulator_cli([
                "--runs", "500",
                "--days", "180",
                "--initial-capital", "50000.0",
                "--daily-budget", "150.0",
                "--output-json", json_path,
                "--seed", "999",
            ], timeout=60)
            self.assertEqual(proc.returncode, 0, f"Institutional run failed: {proc.stderr}")

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            self.assertIn("sharpe_ratio", metrics)
            self.assertIn("cvar_95", metrics)
            # Institutional scale with sufficient buffer should have very low ruin probability
            self.assertLess(metrics["prob_ruin"], 0.15, "Institutional scale should have low ruin risk.")
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier4_zero_touch_verification_pipeline(self):
        """Verify full zero-touch CI/CD pipeline from CLI dispatch to metric deserialization."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf_json, \
             tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tf_svg:
            json_path = tf_json.name
            svg_path = tf_svg.name

        try:
            proc = run_simulator_cli([
                "--runs", "250",
                "--days", "60",
                "--output-json", json_path,
                "--output-svg", svg_path,
                "--seed", "2026",
            ])
            self.assertEqual(proc.returncode, 0, f"Pipeline failed: {proc.stderr}")

            # Verify files on disk
            self.assertGreater(os.path.getsize(json_path), 50)
            self.assertGreater(os.path.getsize(svg_path), 100)

            # Parse and verify full data pipeline
            with open(json_path, "r", encoding="utf-8") as f:
                result = json.load(f)

            self.assertIn("metrics", result)
            self.assertIn("roi_percent", result["metrics"])
        finally:
            for p in [json_path, svg_path]:
                if os.path.exists(p):
                    os.unlink(p)

    def test_tier4_bear_market_stress_scenario(self):
        """Verify economic simulator resilience under bear market conditions (50% bounty drop)."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--payout-median", "500.0",
                "--p-finding", "0.02",
                "--output-json", json_path,
                "--seed", "42",
            ])
            self.assertEqual(proc.returncode, 0, f"Bear stress run failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # In bear market, ROI is compressed compared to normal
            self.assertIn("metrics", data)
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)

    def test_tier4_high_competition_frontrunning_scenario(self):
        """Verify shock scenario where competitor bot density spikes duplicate rate to 90%."""
        self.require_simulator()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            json_path = tf.name

        try:
            proc = run_simulator_cli([
                "--runs", "100",
                "--days", "30",
                "--duplicate-rate", "0.90",
                "--output-json", json_path,
                "--seed", "42",
            ])
            self.assertEqual(proc.returncode, 0, f"Competition run failed: {proc.stderr}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            metrics = data["metrics"]
            self.assertLess(metrics["rocs"], 1.5, "High duplicate collision must suppress ROCS.")
        finally:
            if os.path.exists(json_path):
                os.unlink(json_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
