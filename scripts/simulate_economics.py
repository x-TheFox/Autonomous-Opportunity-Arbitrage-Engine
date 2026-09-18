#!/usr/bin/env python3
"""
Autonomous Opportunity Arbitrage Engine (AOAE) — Monte Carlo Economic Simulator

Simulates stochastic opportunity discovery, competition collision, triage friction,
and programmatic settlement economics across Web3, Web2, and Hybrid archetypes.

Zero external dependencies required (uses only Python 3 standard library).
"""

import argparse
import json
import math
import os
import random
import statistics
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

# Archetype calibrated economic baselines
ARCHETYPE_PROFILES = {
    "web3": {
        "description": "Web3 Smart Contract Security Research (Immunefi, Sherlock, Code4rena)",
        "p_eligible": 1.00,
        "p_finding": 0.035,
        "duplicate_rate": 0.35,
        "p_accepted": 0.90,
        "payout_median": 5000.0,
        "payout_max": 50000.0,
        "token_cost_per_run": 14.20,
        "triage_latency_days": 14.0,
        "infra_daily_cost": 5.0,
        "initial_capital": 2500.0,
        "daily_budget": 50.0,
    },
    "web2": {
        "description": "Web2 Public Bug Bounty Hunting (HackerOne, Bugcrowd)",
        "p_eligible": 0.65,
        "p_finding": 0.03,
        "duplicate_rate": 0.85,
        "p_accepted": 0.25,
        "payout_median": 350.0,
        "payout_max": 3000.0,
        "token_cost_per_run": 1.50,
        "triage_latency_days": 45.0,
        "infra_daily_cost": 5.0,
        "initial_capital": 2500.0,
        "daily_budget": 50.0,
    },
    "hybrid": {
        "description": "Adversarially-Gated Hybrid Archetype (Curated VDPs + OSS PR Escrows)",
        "p_eligible": 0.85,
        "p_finding": 0.06,
        "duplicate_rate": 0.45,
        "p_accepted": 0.70,
        "payout_median": 1500.0,
        "payout_max": 15000.0,
        "token_cost_per_run": 6.50,
        "triage_latency_days": 20.0,
        "infra_daily_cost": 5.0,
        "initial_capital": 2500.0,
        "daily_budget": 50.0,
    },
}


def sample_poisson(lam: float) -> int:
    """Sample from Poisson distribution using Knuth's algorithm or Gaussian approximation."""
    if lam <= 0.0:
        return 0
    if lam < 30.0:
        L = math.exp(-lam)
        k = 0
        p = 1.0
        while p > L:
            k += 1
            p *= random.random()
        return k - 1
    # Gaussian approximation for large lambda
    val = random.gauss(lam, math.sqrt(lam))
    return max(0, int(round(val)))


def sample_lognormal(median: float, sigma: float = 0.85, max_val: float = 100000.0) -> float:
    """Sample from Log-Normal distribution parameterized by median and sigma."""
    if median <= 0:
        return 0.0
    mu = math.log(median)
    sample = math.exp(random.gauss(mu, sigma))
    return min(sample, max_val)


def sample_latency(mean_latency: float) -> int:
    """Sample settlement latency in calendar days."""
    if mean_latency <= 0:
        return 0
    # Exponential distribution with minimum 1 day
    lat = int(round(random.expovariate(1.0 / mean_latency)))
    return max(1, lat)


def run_monte_carlo(
    runs: int,
    days: int,
    initial_capital: float,
    daily_budget: float,
    p_eligible: float,
    p_finding: float,
    duplicate_rate: float,
    p_accepted: float,
    payout_median: float,
    payout_max: float,
    token_cost_per_run: float,
    infra_daily_cost: float,
    triage_latency_days: float,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Execute N Monte Carlo trajectory simulations across daily operational timesteps.
    """
    trajectories: List[List[float]] = []
    profits: List[float] = []
    total_revenues: List[float] = []
    total_spends: List[float] = []
    ruined_count = 0

    for r in range(runs):
        cash = initial_capital
        total_spend = 0.0
        total_revenue = 0.0
        # Pending settlement queue: list of (settlement_day, amount)
        pending_payouts: List[Tuple[int, float]] = []
        equity_curve: List[float] = [cash]
        ruined = (cash <= 0.0)

        for day in range(1, days + 1):
            # 1. Settle maturing payouts
            if pending_payouts:
                remaining_pending: List[Tuple[int, float]] = []
                for settle_day, amt in pending_payouts:
                    if settle_day <= day:
                        cash += amt
                        total_revenue += amt
                    else:
                        remaining_pending.append((settle_day, amt))
                pending_payouts = remaining_pending

            # 2. Allocate daily budget
            if daily_budget <= 0.0 or cash <= 0.0:
                daily_spend = 0.0
                targets_explored = 0
            else:
                target_spend_ceiling = min(daily_budget, cash)
                infra_spend = min(infra_daily_cost, target_spend_ceiling)
                token_budget = target_spend_ceiling - infra_spend

                if token_cost_per_run > 0.0 and token_budget > 0.0:
                    mean_targets = token_budget / token_cost_per_run
                    targets_explored = sample_poisson(mean_targets)
                    token_spend = targets_explored * token_cost_per_run
                    if token_spend + infra_spend > cash:
                        targets_explored = int((cash - infra_spend) // token_cost_per_run)
                        token_spend = targets_explored * token_cost_per_run
                    daily_spend = token_spend + infra_spend
                else:
                    targets_explored = 0
                    daily_spend = infra_spend

                cash -= daily_spend
                total_spend += daily_spend
                if cash <= 0.0:
                    ruined = True

            # 3. Simulate target exploration & probabilistic finding outcomes
            for _ in range(targets_explored):
                if random.random() < p_eligible:
                    if random.random() < p_finding:
                        if random.random() < (1.0 - duplicate_rate):
                            if random.random() < p_accepted:
                                payout = sample_lognormal(payout_median, sigma=0.85, max_val=payout_max)
                                if triage_latency_days <= 0.0:
                                    cash += payout
                                    total_revenue += payout
                                else:
                                    lat = sample_latency(triage_latency_days)
                                    settle_day = day + lat
                                    if settle_day <= day:
                                        cash += payout
                                        total_revenue += payout
                                    else:
                                        pending_payouts.append((settle_day, payout))

            equity_curve.append(cash)

        if ruined:
            ruined_count += 1

        run_profit = total_revenue - total_spend
        profits.append(run_profit)
        total_revenues.append(total_revenue)
        total_spends.append(total_spend)
        trajectories.append(equity_curve)

    # Statistical Aggregation
    mean_profit = float(statistics.mean(profits))
    median_profit = float(statistics.median(profits))
    prob_ruin = float(ruined_count / runs) if runs > 0 else 0.0

    sum_revenue = sum(total_revenues)
    sum_spend = sum(total_spends)
    rocs = float(sum_revenue / sum_spend) if sum_spend > 0.0 else 0.0

    roi_percent = float((mean_profit / initial_capital) * 100.0) if initial_capital > 0.0 else 0.0

    # Risk Metrics: Losses = -profit
    losses = [-p for p in profits]
    losses.sort()
    k_95 = min(len(losses) - 1, max(0, int(0.95 * len(losses))))
    var_95 = float(losses[k_95])
    tail_losses = losses[k_95:]
    cvar_95 = float(statistics.mean(tail_losses)) if tail_losses else var_95

    # Invariant check: CVaR >= VaR
    if cvar_95 < var_95:
        cvar_95 = var_95

    # Sharpe & Sortino ratios based on trajectory returns
    if initial_capital > 0.0:
        returns = [p / initial_capital for p in profits]
    else:
        returns = [0.0 for _ in profits]

    mean_ret = float(statistics.mean(returns))
    stdev_ret = float(statistics.stdev(returns)) if len(returns) > 1 else 0.0

    # Annualized scaling
    ann_factor = math.sqrt(365.0 / days) if days > 0 else 1.0
    rf_rate = 0.04 * (days / 365.0)

    if stdev_ret > 1e-9:
        sharpe_ratio = float(((mean_ret - rf_rate) / stdev_ret) * ann_factor)
    else:
        sharpe_ratio = 0.0

    downside_sq = [min(0.0, r - rf_rate) ** 2 for r in returns]
    downside_dev = math.sqrt(sum(downside_sq) / len(downside_sq)) if downside_sq else 0.0

    if downside_dev > 1e-9:
        sortino_ratio = float(((mean_ret - rf_rate) / downside_dev) * ann_factor)
    else:
        sortino_ratio = float(sharpe_ratio * 2.0) if sharpe_ratio > 0.0 else 0.0

    # Sanitize NaN/Inf
    if math.isnan(sharpe_ratio) or math.isinf(sharpe_ratio):
        sharpe_ratio = 0.0
    if math.isnan(sortino_ratio) or math.isinf(sortino_ratio):
        sortino_ratio = 0.0

    # Trajectory summary percentiles for charting
    daily_trajectories_summary: Dict[str, List[float]] = {}
    if trajectories and days > 0:
        for p_name, q in [("p05", 0.05), ("p25", 0.25), ("p50", 0.50), ("p75", 0.75), ("p95", 0.95)]:
            curve = []
            for d in range(days + 1):
                day_vals = sorted([trajectories[r][d] for r in range(runs)])
                idx = min(len(day_vals) - 1, max(0, int(q * len(day_vals))))
                curve.append(round(day_vals[idx], 2))
            daily_trajectories_summary[p_name] = curve

    sample_trajectories = [
        [round(v, 2) for v in trajectories[i]]
        for i in range(min(15, runs))
    ]

    return {
        "parameters": {
            "runs": runs,
            "days": days,
            "initial_capital": initial_capital,
            "daily_budget": daily_budget,
            "p_eligible": p_eligible,
            "p_finding": p_finding,
            "duplicate_rate": duplicate_rate,
            "p_accepted": p_accepted,
            "payout_median": payout_median,
            "payout_max": payout_max,
            "token_cost_per_run": token_cost_per_run,
            "infra_daily_cost": infra_daily_cost,
            "triage_latency_days": triage_latency_days,
        },
        "metrics": {
            "mean_profit": round(mean_profit, 2),
            "median_profit": round(median_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 4),
            "sortino_ratio": round(sortino_ratio, 4),
            "var_95": round(var_95, 2),
            "cvar_95": round(cvar_95, 2),
            "prob_ruin": round(prob_ruin, 4),
            "roi_percent": round(roi_percent, 2),
            "rocs": round(rocs, 4),
        },
        "trajectories": {
            "sample_runs": sample_trajectories,
            "percentiles": daily_trajectories_summary,
        },
    }


def generate_svg_chart(data: Dict[str, Any], filepath: str) -> None:
    """Generate a clean standalone vector SVG chart visualization."""
    metrics = data["metrics"]
    params = data["parameters"]
    pcts = data.get("trajectories", {}).get("percentiles", {})
    samples = data.get("trajectories", {}).get("sample_runs", [])
    days = params.get("days", 365)

    width = 1000
    height = 640
    margin_left = 80
    margin_right = 50
    margin_top = 80
    margin_bottom = 120

    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom

    # Find min and max values across curves
    all_vals = [params["initial_capital"]]
    for curve in pcts.values():
        all_vals.extend(curve)
    for sample in samples:
        all_vals.extend(sample)

    min_val = min(all_vals)
    max_val = max(all_vals)
    if min_val == max_val:
        min_val -= 100.0
        max_val += 100.0
    val_range = max_val - min_val

    def scale_x(day: int) -> float:
        return margin_left + (day / max(1, days)) * plot_w

    def scale_y(val: float) -> float:
        norm = (val - min_val) / max(1e-5, val_range)
        return margin_top + plot_h - (norm * plot_h)

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        '  <defs>',
        '    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">',
        '      <stop offset="0%" stop-color="#0f172a"/>',
        '      <stop offset="100%" stop-color="#1e293b"/>',
        '    </linearGradient>',
        '    <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">',
        '      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.25"/>',
        '      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.02"/>',
        '    </linearGradient>',
        '  </defs>',
        f'  <rect width="{width}" height="{height}" fill="url(#bgGrad)" rx="12"/>',
        f'  <text x="{margin_left}" y="42" fill="#f8fafc" font-size="20" font-family="monospace, sans-serif" font-weight="bold">AOAE Monte Carlo Economic Trajectories</text>',
        f'  <text x="{margin_left}" y="62" fill="#94a3b8" font-size="12" font-family="monospace, sans-serif">Runs: {params["runs"]} | Days: {params["days"]} | Budget/Day: ${params["daily_budget"]} | P(find): {params["p_finding"]} | DupRate: {params["duplicate_rate"]}</text>',
    ]

    # Grid lines and Y-axis labels
    y_steps = 5
    for i in range(y_steps + 1):
        v = min_val + (i / y_steps) * val_range
        y_pos = scale_y(v)
        svg_lines.append(f'  <line x1="{margin_left}" y1="{y_pos:.1f}" x2="{width - margin_right}" y2="{y_pos:.1f}" stroke="#334155" stroke-dasharray="4,4" stroke-width="1"/>')
        svg_lines.append(f'  <text x="{margin_left - 10}" y="{y_pos + 4:.1f}" fill="#94a3b8" font-size="11" font-family="monospace, sans-serif" text-anchor="end">${v:,.0f}</text>')

    # Zero/Breakeven Line if within range
    if min_val <= params["initial_capital"] <= max_val:
        y_init = scale_y(params["initial_capital"])
        svg_lines.append(f'  <line x1="{margin_left}" y1="{y_init:.1f}" x2="{width - margin_right}" y2="{y_init:.1f}" stroke="#64748b" stroke-width="1.5"/>')

    # Draw individual sample trajectory paths
    for s_idx, sample in enumerate(samples):
        path_d = []
        for d, val in enumerate(sample):
            x = scale_x(d)
            y = scale_y(val)
            cmd = "M" if d == 0 else "L"
            path_d.append(f"{cmd} {x:.1f} {y:.1f}")
        d_str = " ".join(path_d)
        svg_lines.append(f'  <path d="{d_str}" fill="none" stroke="#38bdf8" stroke-width="1" stroke-opacity="0.18"/>')

    # Draw 50th percentile (Median)
    if "p50" in pcts and len(pcts["p50"]) > 0:
        path_p50 = []
        for d, val in enumerate(pcts["p50"]):
            x = scale_x(d)
            y = scale_y(val)
            cmd = "M" if d == 0 else "L"
            path_p50.append(f"{cmd} {x:.1f} {y:.1f}")
        d_str = " ".join(path_p50)
        svg_lines.append(f'  <path d="{d_str}" fill="none" stroke="#38bdf8" stroke-width="2.5"/>')

    # Draw 95th and 5th percentiles
    if "p95" in pcts and "p05" in pcts:
        path_p95 = " ".join([f"{'M' if d==0 else 'L'} {scale_x(d):.1f} {scale_y(v):.1f}" for d, v in enumerate(pcts["p95"])])
        path_p05 = " ".join([f"{'M' if d==0 else 'L'} {scale_x(d):.1f} {scale_y(v):.1f}" for d, v in enumerate(pcts["p05"])])
        svg_lines.append(f'  <path d="{path_p95}" fill="none" stroke="#10b981" stroke-width="1.5" stroke-dasharray="3,3"/>')
        svg_lines.append(f'  <path d="{path_p05}" fill="none" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="3,3"/>')

    # Metrics Summary Bar at Bottom
    box_y = height - margin_bottom + 30
    box_h = 60
    svg_lines.append(f'  <rect x="{margin_left}" y="{box_y}" width="{plot_w}" height="{box_h}" fill="#1e293b" rx="8" stroke="#334155" stroke-width="1"/>')

    metric_items = [
        ("Median Profit", f"${metrics['median_profit']:,.0f}"),
        ("Mean Profit", f"${metrics['mean_profit']:,.0f}"),
        ("ROCS", f"{metrics['rocs']:.2f}x"),
        ("Sharpe", f"{metrics['sharpe_ratio']:.2f}"),
        ("Sortino", f"{metrics['sortino_ratio']:.2f}"),
        ("VaR 95", f"${metrics['var_95']:,.0f}"),
        ("CVaR 95", f"${metrics['cvar_95']:,.0f}"),
        ("P(Ruin)", f"{metrics['prob_ruin']*100:.1f}%"),
    ]

    col_w = plot_w / len(metric_items)
    for idx, (label, val_str) in enumerate(metric_items):
        cx = margin_left + idx * col_w + col_w / 2.0
        svg_lines.append(f'  <text x="{cx:.1f}" y="{box_y + 22}" fill="#94a3b8" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">{label}</text>')
        svg_lines.append(f'  <text x="{cx:.1f}" y="{box_y + 45}" fill="#f8fafc" font-size="13" font-family="monospace, sans-serif" font-weight="bold" text-anchor="middle">{val_str}</text>')

    svg_lines.append('</svg>')
    svg_content = "\n".join(svg_lines)

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Autonomous Opportunity Arbitrage Engine (AOAE) Monte Carlo Economic Simulator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--runs", type=int, default=1000, help="Number of Monte Carlo trajectory runs")
    parser.add_argument("--days", type=int, default=365, help="Simulation horizon in days")
    parser.add_argument("--archetype", choices=["web3", "web2", "hybrid"], default="web3", help="Target opportunity archetype")
    parser.add_argument("--budget", type=float, default=None, help="Overall capital or daily budget allocation ($)")
    parser.add_argument("--initial-capital", type=float, default=None, help="Starting cash balance ($)")
    parser.add_argument("--daily-budget", type=float, default=None, help="Maximum daily compute & token spend ($)")
    parser.add_argument("--duplicate-rate", type=float, default=None, help="Probability finding is a duplicate collision [0.0-1.0]")
    parser.add_argument("--triage-latency", type=float, default=None, help="Mean triage settlement delay in days")
    parser.add_argument("--triage-latency-days", type=float, default=None, help="Mean triage settlement delay in days (alias)")
    parser.add_argument("--p-finding", type=float, default=None, help="Probability of discovering a finding per execution")
    parser.add_argument("--p-eligible", type=float, default=None, help="Probability target passes safe-harbor gate")
    parser.add_argument("--p-accepted", type=float, default=None, help="Probability finding is accepted by triage")
    parser.add_argument("--payout-median", type=float, default=None, help="Median bounty payout ($)")
    parser.add_argument("--payout-max", type=float, default=None, help="Maximum bounty payout ceiling ($)")
    parser.add_argument("--token-cost-per-run", type=float, default=None, help="LLM token cost per target execution ($)")
    parser.add_argument("--infra-daily-cost", type=float, default=None, help="Fixed daily infrastructure cost ($)")
    parser.add_argument("--seed", type=int, default=None, help="PRNG seed for deterministic reproducibility")
    parser.add_argument("--output-json", type=str, default=None, help="Path to write JSON simulation results")
    parser.add_argument("--output-svg", type=str, default=None, help="Path to write standalone vector SVG chart")
    parser.add_argument("--verbose", action="store_true", help="Print detailed simulation diagnostics")

    args = parser.parse_args()

    # Input validation
    if args.runs <= 0:
        parser.error(f"--runs must be a strictly positive integer, got {args.runs}")
    if args.days <= 0:
        parser.error(f"--days must be a strictly positive integer, got {args.days}")
    if args.daily_budget is not None and args.daily_budget < 0:
        parser.error(f"--daily-budget cannot be negative, got {args.daily_budget}")
    if args.budget is not None and args.budget < 0:
        parser.error(f"--budget cannot be negative, got {args.budget}")
    if args.initial_capital is not None and args.initial_capital < 0:
        parser.error(f"--initial-capital cannot be negative, got {args.initial_capital}")
    if args.duplicate_rate is not None and not (0.0 <= args.duplicate_rate <= 1.0):
        parser.error(f"--duplicate-rate must be between 0.0 and 1.0, got {args.duplicate_rate}")
    if args.p_finding is not None and not (0.0 <= args.p_finding <= 1.0):
        parser.error(f"--p-finding must be between 0.0 and 1.0, got {args.p_finding}")
    if args.p_eligible is not None and not (0.0 <= args.p_eligible <= 1.0):
        parser.error(f"--p-eligible must be between 0.0 and 1.0, got {args.p_eligible}")
    if args.p_accepted is not None and not (0.0 <= args.p_accepted <= 1.0):
        parser.error(f"--p-accepted must be between 0.0 and 1.0, got {args.p_accepted}")
    if args.triage_latency is not None and args.triage_latency < 0:
        parser.error(f"--triage-latency cannot be negative, got {args.triage_latency}")
    if args.triage_latency_days is not None and args.triage_latency_days < 0:
        parser.error(f"--triage-latency-days cannot be negative, got {args.triage_latency_days}")

    # Set seed if provided
    if args.seed is not None:
        random.seed(args.seed)

    # Resolve archetype baseline defaults
    profile = ARCHETYPE_PROFILES[args.archetype]

    # Initial capital resolution
    if args.initial_capital is not None:
        initial_capital = args.initial_capital
    elif args.budget is not None:
        initial_capital = args.budget
    else:
        initial_capital = profile["initial_capital"]

    # Daily budget resolution
    if args.daily_budget is not None:
        daily_budget = args.daily_budget
    elif args.budget is not None:
        if args.budget == 0.0:
            daily_budget = 0.0
        else:
            daily_budget = min(args.budget * 0.05, 50.0)
    else:
        daily_budget = profile["daily_budget"]

    # Triage latency resolution
    if args.triage_latency_days is not None:
        triage_latency_days = args.triage_latency_days
    elif args.triage_latency is not None:
        triage_latency_days = args.triage_latency
    else:
        triage_latency_days = profile["triage_latency_days"]

    p_eligible = args.p_eligible if args.p_eligible is not None else profile["p_eligible"]
    p_finding = args.p_finding if args.p_finding is not None else profile["p_finding"]
    duplicate_rate = args.duplicate_rate if args.duplicate_rate is not None else profile["duplicate_rate"]
    p_accepted = args.p_accepted if args.p_accepted is not None else profile["p_accepted"]
    payout_median = args.payout_median if args.payout_median is not None else profile["payout_median"]
    payout_max = args.payout_max if args.payout_max is not None else profile["payout_max"]
    token_cost_per_run = args.token_cost_per_run if args.token_cost_per_run is not None else profile["token_cost_per_run"]
    infra_daily_cost = args.infra_daily_cost if args.infra_daily_cost is not None else profile["infra_daily_cost"]

    t0 = time.time()
    results = run_monte_carlo(
        runs=args.runs,
        days=args.days,
        initial_capital=initial_capital,
        daily_budget=daily_budget,
        p_eligible=p_eligible,
        p_finding=p_finding,
        duplicate_rate=duplicate_rate,
        p_accepted=p_accepted,
        payout_median=payout_median,
        payout_max=payout_max,
        token_cost_per_run=token_cost_per_run,
        infra_daily_cost=infra_daily_cost,
        triage_latency_days=triage_latency_days,
        verbose=args.verbose,
    )
    elapsed = time.time() - t0

    results["archetype"] = args.archetype
    results["elapsed_seconds"] = round(elapsed, 3)

    metrics = results["metrics"]

    # Console output
    print("=" * 72)
    print("  AUTONOMOUS OPPORTUNITY ARBITRAGE ENGINE — MONTE CARLO SIMULATOR")
    print("=" * 72)
    print(f"Archetype:        {args.archetype.upper()} ({profile['description']})")
    print(f"Runs / Horizon:   {args.runs:,} runs across {args.days} calendar days")
    print(f"Capital / Budget: Initial: ${initial_capital:,.2f} | Daily Cap: ${daily_budget:,.2f}")
    print(f"Probabilities:    P(elig)={p_eligible:.2f} | P(find)={p_finding:.3f} | DupRate={duplicate_rate:.2f} | P(acc)={p_accepted:.2f}")
    print(f"Payout / Costs:   Median Payout: ${payout_median:,.2f} | Token/Target: ${token_cost_per_run:.2f}")
    print("-" * 72)
    print("KEY PERFORMANCE INDICATORS (RISK-ADJUSTED):")
    print(f"  Mean Net Profit:     ${metrics['mean_profit']:>12,.2f}")
    print(f"  Median Net Profit:   ${metrics['median_profit']:>12,.2f}")
    print(f"  Realized ROCS:        {metrics['rocs']:>12.2f}x (Gross Revenue / Compute Spend)")
    print(f"  Expected ROI:         {metrics['roi_percent']:>12.2f}%")
    print(f"  Annualized Sharpe:    {metrics['sharpe_ratio']:>12.2f}")
    print(f"  Downside Sortino:     {metrics['sortino_ratio']:>12.2f}")
    print(f"  Value at Risk (95%): ${metrics['var_95']:>12,.2f}")
    print(f"  CVaR / Shortfall 95: ${metrics['cvar_95']:>12,.2f}")
    print(f"  Probability of Ruin:  {metrics['prob_ruin']*100:>11.2f}%")
    print(f"  Execution Runtime:    {elapsed:>12.3f}s")
    print("=" * 72)

    if args.output_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        if args.verbose:
            print(f"[+] Exported JSON results to {args.output_json}")

    if args.output_svg:
        generate_svg_chart(results, args.output_svg)
        if args.verbose:
            print(f"[+] Exported standalone SVG chart to {args.output_svg}")


if __name__ == "__main__":
    main()
