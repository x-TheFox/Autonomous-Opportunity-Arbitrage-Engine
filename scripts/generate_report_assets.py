#!/usr/bin/env python3
"""
Autonomous Opportunity Arbitrage Engine (AOAE) — Publication-Grade SVG Generator
Generates:
  - assets/ev_comparison.svg
  - assets/kelly_allocation.svg
  - assets/financial_trajectories.svg
  - assets/sensitivity_heatmap.svg

All SVGs are well-formed XML, self-contained, responsive, and styled with high-contrast
dark modern palettes for publication readiness.
"""

import os
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def build_ev_comparison_svg(filepath: Path):
    width, height = 1000, 560
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
    <linearGradient id="web3Grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#10b981" />
      <stop offset="100%" stop-color="#34d399" />
    </linearGradient>
    <linearGradient id="web2Grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f43f5e" />
      <stop offset="100%" stop-color="#fb7185" />
    </linearGradient>
    <linearGradient id="web3AreaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.0" />
    </linearGradient>
    <linearGradient id="web2AreaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.0" />
      <stop offset="100%" stop-color="#f43f5e" stop-opacity="0.30" />
    </linearGradient>
    <filter id="glow3" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad)" rx="12" stroke="#1e293b" stroke-width="1.5" />

  <!-- Header -->
  <text x="50" y="46" fill="#f8fafc" font-size="20" font-weight="700" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Expected Value (EV) per Target: Web3 Smart Contracts vs Web2 Bug Bounties</text>
  <text x="50" y="70" fill="#94a3b8" font-size="13" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Cumulative Net Expected Profit across Evaluated Target Volumes | 17-Subsystem Parametric Model</text>

  <!-- Metric Badges Top Right -->
  <g transform="translate(620, 26)">
    <rect width="150" height="52" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5" filter="url(#cardShadow)"/>
    <text x="75" y="22" fill="#94a3b8" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">WEB3 NET EV</text>
    <text x="75" y="42" fill="#34d399" font-size="16" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">+$398.26 / target</text>
  </g>
  <g transform="translate(790, 26)">
    <rect width="150" height="52" rx="8" fill="#1e293b" stroke="#f43f5e" stroke-width="1.5" filter="url(#cardShadow)"/>
    <text x="75" y="22" fill="#94a3b8" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">WEB2 NET EV</text>
    <text x="75" y="42" fill="#fb7185" font-size="16" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">-$80.55 / target</text>
  </g>

  <!-- Plot Area Frame -->
  <!-- Origin at x=100, y=360 (y=0 is at 360). Top is y=110 (+$400,000), Bottom is y=480 (-$100,000) -->
  <!-- Width: 100 to 920 = 820px. 0 to 1000 targets -->
  <rect x="100" y="100" width="820" height="390" fill="#0d1526" rx="6" stroke="#334155" stroke-width="1"/>

  <!-- Horizontal Grid Lines -->
  <!-- +$400k (y=120), +$300k (y=180), +$200k (y=240), +$100k (y=300), $0 (y=360), -$100k (y=420) -->
  <line x1="100" y1="120" x2="920" y2="120" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="124" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">+$400k</text>

  <line x1="100" y1="180" x2="920" y2="180" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="184" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">+$300k</text>

  <line x1="100" y1="240" x2="920" y2="240" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="244" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">+$200k</text>

  <line x1="100" y1="300" x2="920" y2="300" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="304" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">+$100k</text>

  <!-- Zero Axis Baseline -->
  <line x1="100" y1="360" x2="920" y2="360" stroke="#475569" stroke-width="2"/>
  <text x="90" y="364" fill="#94a3b8" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="end">$0</text>

  <line x1="100" y1="425" x2="920" y2="425" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="429" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">-$100k</text>

  <!-- Vertical Grid Lines (Targets: 0, 200, 400, 600, 800, 1000) -->
  <!-- x coordinates: 100, 264, 428, 592, 756, 920 -->
  <line x1="264" y1="100" x2="264" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="264" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">200 Targets</text>

  <line x1="428" y1="100" x2="428" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="428" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">400 Targets</text>

  <line x1="592" y1="100" x2="592" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="592" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">600 Targets</text>

  <line x1="756" y1="100" x2="756" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="756" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">800 Targets</text>

  <line x1="920" y1="100" x2="920" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="920" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">1,000 Targets</text>

  <!-- Data Curves & Shaded Areas -->
  <!-- Web3 curve: starts at (100, 360). At 1000 targets: EV = +$398,260. Y pos: 360 - (398.26/400)*240 = 360 - 238.9 = 121.1 -->
  <!-- Web3 shaded area -->
  <polygon points="100,360 920,121 920,360" fill="url(#web3AreaGrad)"/>
  <!-- Web3 line -->
  <line x1="100" y1="360" x2="920" y2="121" stroke="url(#web3Grad)" stroke-width="3.5" filter="url(#glow3)"/>

  <!-- Web2 curve: starts at (100, 360). At 1000 targets: EV = -$80,550. Y pos: 360 + (80.55/100)*65 = 360 + 52.3 = 412.3 -->
  <!-- Web2 shaded area -->
  <polygon points="100,360 920,412 920,360" fill="url(#web2AreaGrad)"/>
  <!-- Web2 line -->
  <line x1="100" y1="360" x2="920" y2="412" stroke="url(#web2Grad)" stroke-width="3" stroke-dasharray="6,4"/>

  <!-- Callout Markers & Annotations -->
  <!-- Web3 Marker at 1000 targets -->
  <circle cx="920" cy="121" r="6" fill="#10b981" stroke="#f8fafc" stroke-width="2"/>
  <rect x="760" y="112" width="150" height="36" rx="6" fill="#1e293b" stroke="#34d399" stroke-width="1" opacity="0.95"/>
  <text x="835" y="127" fill="#f8fafc" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">+$398,260 NET</text>
  <text x="835" y="141" fill="#34d399" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">ROCS: 14.30x (Superprofit)</text>

  <!-- Web2 Marker at 1000 targets -->
  <circle cx="920" cy="412" r="5" fill="#f43f5e" stroke="#f8fafc" stroke-width="1.5"/>
  <rect x="760" y="420" width="150" height="36" rx="6" fill="#1e293b" stroke="#f43f5e" stroke-width="1" opacity="0.95"/>
  <text x="835" y="435" fill="#f8fafc" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">-$80,550 NET LOSS</text>
  <text x="835" y="449" fill="#fb7185" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">ROCS: 0.40x (Insolvent)</text>

  <!-- Breakeven Inflection Note -->
  <g transform="translate(130, 130)">
    <rect width="280" height="110" rx="8" fill="#111827" stroke="#38bdf8" stroke-width="1" opacity="0.95"/>
    <text x="14" y="24" fill="#38bdf8" font-size="12" font-weight="bold" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Key Parametric Drivers</text>
    <text x="14" y="46" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">• Web3 Acceptance: 98% (Deterministic PoC)</text>
    <text x="14" y="64" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">• Web3 Duplicate Rate: 35% (vs Web2 85%)</text>
    <text x="14" y="82" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">• Web3 Median Payout: $18,500 (vs Web2 $300)</text>
    <text x="14" y="100" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">• Web3 Cash Conversion: -19 Days (Negative CCC)</text>
  </g>

  <!-- Legend Bottom -->
  <g transform="translate(100, 528)">
    <line x1="0" y1="8" x2="30" y2="8" stroke="#10b981" stroke-width="3"/>
    <text x="40" y="12" fill="#e2e8f0" font-size="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Web3 Smart Contracts (Machine-Verifiable / Code4rena &amp; Immunefi)</text>
    
    <line x1="480" y1="8" x2="510" y2="8" stroke="#f43f5e" stroke-width="2.5" stroke-dasharray="6,4"/>
    <text x="520" y="12" fill="#e2e8f0" font-size="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Web2 Bug Bounties (Human Triage Pushback / HackerOne &amp; Bugcrowd)</text>
  </g>
</svg>"""
    filepath.write_text(svg.strip(), encoding="utf-8")


def build_kelly_allocation_svg(filepath: Path):
    width, height = 1000, 560
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad2" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
    <linearGradient id="auditGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#38bdf8" />
    </linearGradient>
    <linearGradient id="standingGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#059669" />
      <stop offset="100%" stop-color="#34d399" />
    </linearGradient>
    <linearGradient id="zeroGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#e11d48" />
      <stop offset="100%" stop-color="#f43f5e" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad2)" rx="12" stroke="#1e293b" stroke-width="1.5" />

  <!-- Header -->
  <text x="50" y="46" fill="#f8fafc" font-size="20" font-weight="700" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Multi-Asset Fractional Kelly Capital &amp; Compute Allocation</text>
  <text x="50" y="70" fill="#94a3b8" font-size="13" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Quarter-Kelly (0.25 f*) Budget Allocation Schedule Governing Autonomous Execution Tiers</text>

  <!-- Top Formula Card -->
  <g transform="translate(50, 92)">
    <rect width="900" height="54" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>
    <text x="30" y="32" fill="#38bdf8" font-size="13" font-family="monospace, sans-serif" font-weight="bold">Fractional Kelly Equation:</text>
    <text x="245" y="32" fill="#f8fafc" font-size="13" font-family="monospace, sans-serif">f* = p - (1 - p) / b  |  f_allocated = max(0, 0.25 * f*)</text>
    <text x="680" y="32" fill="#94a3b8" font-size="12" font-family="monospace, sans-serif">Safety Margin: 75% Drawdown Shield</text>
  </g>

  <!-- Macro Allocation Horizontal Bar Visualizer -->
  <g transform="translate(50, 166)">
    <text x="0" y="16" fill="#cbd5e1" font-size="13" font-weight="bold" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Active Portfolio Compute Dispatch (100% of Daily Compute Budget)</text>
    
    <!-- Outer Bar Container (width 900) -->
    <rect x="0" y="28" width="900" height="42" rx="6" fill="#0d1526" stroke="#334155" stroke-width="1"/>

    <!-- Audit Contests Segment: 65% = 585px -->
    <rect x="0" y="28" width="585" height="42" rx="6" fill="url(#auditGrad)"/>
    <text x="292" y="54" fill="#0f172a" font-size="14" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">Audit Contests: 65% Allocation ($32.50/day)</text>

    <!-- Standing Criticals Segment: 35% = 315px -->
    <rect x="585" y="28" width="315" height="42" rx="0" fill="url(#standingGrad)"/>
    <text x="742" y="54" fill="#0f172a" font-size="14" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">Standing Criticals: 35% ($17.50/day)</text>
  </g>

  <!-- Detailed Regime Breakdown Cards (3 Cards Side-by-Side) -->

  <!-- Card 1: Time-Bound Audit Contests (65%) -->
  <g transform="translate(50, 260)">
    <rect width="285" height="260" rx="10" fill="#131e32" stroke="#38bdf8" stroke-width="1.5"/>
    <rect x="0" y="0" width="285" height="38" rx="10" fill="#0284c7" fill-opacity="0.25"/>
    <text x="20" y="25" fill="#38bdf8" font-size="14" font-weight="bold" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Audit Contests (Code4rena/Sherlock)</text>

    <text x="20" y="65" fill="#94a3b8" font-size="11" font-family="monospace, sans-serif">PRIMARY ASSET CLASS</text>
    <text x="20" y="90" fill="#38bdf8" font-size="24" font-weight="bold" font-family="monospace, sans-serif">65.0%</text>
    <text x="100" y="88" fill="#94a3b8" font-size="12" font-family="monospace, sans-serif">Budget Sizing</text>

    <line x1="20" y1="108" x2="265" y2="108" stroke="#334155" stroke-width="1"/>

    <text x="20" y="130" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Win Probability (p):</text>
    <text x="265" y="130" fill="#f8fafc" font-size="11" font-family="monospace, sans-serif" text-anchor="end">35.0%</text>

    <text x="20" y="152" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Payout Odds (b):</text>
    <text x="265" y="152" fill="#f8fafc" font-size="11" font-family="monospace, sans-serif" text-anchor="end">52.0x</text>

    <text x="20" y="174" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Unconstrained Kelly (f*):</text>
    <text x="265" y="174" fill="#f8fafc" font-size="11" font-family="monospace, sans-serif" text-anchor="end">33.75%</text>

    <text x="20" y="196" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Quarter Kelly (0.25 f*):</text>
    <text x="265" y="196" fill="#38bdf8" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="end">8.44%</text>

    <text x="20" y="218" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Triage Latency:</text>
    <text x="265" y="218" fill="#10b981" font-size="11" font-family="monospace, sans-serif" text-anchor="end">3–7 Days</text>

    <text x="20" y="240" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Strategic Function:</text>
    <text x="265" y="240" fill="#94a3b8" font-size="10" font-family="monospace, sans-serif" text-anchor="end">High Velocity Turnover</text>
  </g>

  <!-- Card 2: Standing Criticals (35%) -->
  <g transform="translate(358, 260)">
    <rect width="285" height="260" rx="10" fill="#102521" stroke="#34d399" stroke-width="1.5"/>
    <rect x="0" y="0" width="285" height="38" rx="10" fill="#059669" fill-opacity="0.25"/>
    <text x="20" y="25" fill="#34d399" font-size="14" font-weight="bold" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Standing Criticals (Immunefi)</text>

    <text x="20" y="65" fill="#94a3b8" font-size="11" font-family="monospace, sans-serif">HIGH-CONVICTION POOL</text>
    <text x="20" y="90" fill="#34d399" font-size="24" font-weight="bold" font-family="monospace, sans-serif">35.0%</text>
    <text x="100" y="88" fill="#94a3b8" font-size="12" font-family="monospace, sans-serif">Budget Sizing</text>

    <line x1="20" y1="108" x2="265" y2="108" stroke="#334155" stroke-width="1"/>

    <text x="20" y="130" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Win Probability (p):</text>
    <text x="265" y="130" fill="#f8fafc" font-size="11" font-family="monospace, sans-serif" text-anchor="end">2.23%</text>

    <text x="20" y="152" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Payout Odds (b):</text>
    <text x="265" y="152" fill="#f8fafc" font-size="11" font-family="monospace, sans-serif" text-anchor="end">1,301.8x</text>

    <text x="20" y="174" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Unconstrained Kelly (f*):</text>
    <text x="265" y="174" fill="#f8fafc" font-size="11" font-family="monospace, sans-serif" text-anchor="end">2.16%</text>

    <text x="20" y="196" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Quarter Kelly (0.25 f*):</text>
    <text x="265" y="196" fill="#34d399" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="end">0.54%</text>

    <text x="20" y="218" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Triage Latency:</text>
    <text x="265" y="218" fill="#f59e0b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">14–21 Days</text>

    <text x="20" y="240" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Strategic Function:</text>
    <text x="265" y="240" fill="#94a3b8" font-size="10" font-family="monospace, sans-serif" text-anchor="end">Outsized Payout Convexity</text>
  </g>

  <!-- Card 3: Negative-EV & Web2 Domains (0% - Hard Veto) -->
  <g transform="translate(665, 260)">
    <rect width="285" height="260" rx="10" fill="#251217" stroke="#f43f5e" stroke-width="1.5"/>
    <rect x="0" y="0" width="285" height="38" rx="10" fill="#e11d48" fill-opacity="0.25"/>
    <text x="20" y="25" fill="#f43f5e" font-size="14" font-weight="bold" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Negative-EV Domains (Web2)</text>

    <text x="20" y="65" fill="#94a3b8" font-size="11" font-family="monospace, sans-serif">SUB-ZERO EXPECTATION</text>
    <text x="20" y="90" fill="#f43f5e" font-size="24" font-weight="bold" font-family="monospace, sans-serif">0.0%</text>
    <text x="90" y="88" fill="#fb7185" font-size="12" font-family="monospace, sans-serif">HARD SYSTEM VETO</text>

    <line x1="20" y1="108" x2="265" y2="108" stroke="#334155" stroke-width="1"/>

    <text x="20" y="130" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Win Probability (p):</text>
    <text x="265" y="130" fill="#f8fafc" font-size="11" font-family="monospace, sans-serif" text-anchor="end">0.07% (Sub-Noise)</text>

    <text x="20" y="152" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Payout Odds (b):</text>
    <text x="265" y="152" fill="#f8fafc" font-size="11" font-family="monospace, sans-serif" text-anchor="end">594.2x</text>

    <text x="20" y="174" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Unconstrained Kelly (f*):</text>
    <text x="265" y="174" fill="#f43f5e" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="end">-0.10% (NEGATIVE)</text>

    <text x="20" y="196" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Quarter Kelly (0.25 f*):</text>
    <text x="265" y="196" fill="#f43f5e" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="end">0.00% (Pruned)</text>

    <text x="20" y="218" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Triage Latency:</text>
    <text x="265" y="218" fill="#f43f5e" font-size="11" font-family="monospace, sans-serif" text-anchor="end">45–90 Days</text>

    <text x="20" y="240" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif">Strategic Action:</text>
    <text x="265" y="240" fill="#f43f5e" font-size="10" font-family="monospace, sans-serif" text-anchor="end">Subsystem 03 Pre-Filter Drop</text>
  </g>
</svg>"""
    filepath.write_text(svg.strip(), encoding="utf-8")


def build_financial_trajectories_svg(filepath: Path):
    width, height = 1000, 560
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad3" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
    <linearGradient id="upsideArea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.30" />
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.02" />
    </linearGradient>
    <linearGradient id="baseArea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.25" />
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.01" />
    </linearGradient>
    <linearGradient id="consArea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.0" />
      <stop offset="100%" stop-color="#f43f5e" stop-opacity="0.25" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad3)" rx="12" stroke="#1e293b" stroke-width="1.5" />

  <!-- Title & Subtitle -->
  <text x="50" y="46" fill="#f8fafc" font-size="20" font-weight="700" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">365-Day Cumulative Profit Trajectories: Monte Carlo Financial Regimes</text>
  <text x="50" y="70" fill="#94a3b8" font-size="13" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">10,000 Stochastic Iterations Across Conservative, Base, and Upside Capital Schedules</text>

  <!-- Plot Area Frame -->
  <!-- Left: 100, Width: 820 -> Right: 920. Top: 100, Height: 390 -> Bottom: 490 -->
  <!-- Y mapping: +$350k at y=115, $0 at y=390, -$50k at y=460 -->
  <rect x="100" y="100" width="820" height="390" fill="#0d1526" rx="6" stroke="#334155" stroke-width="1"/>

  <!-- Horizontal Grid Lines -->
  <line x1="100" y1="125" x2="920" y2="125" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="129" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">+$300k</text>

  <line x1="100" y1="190" x2="920" y2="190" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="194" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">+$200k</text>

  <line x1="100" y1="255" x2="920" y2="255" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="259" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">+$100k</text>

  <line x1="100" y1="320" x2="920" y2="320" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="324" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">+$50k</text>

  <!-- Zero Baseline -->
  <line x1="100" y1="390" x2="920" y2="390" stroke="#475569" stroke-width="2"/>
  <text x="90" y="394" fill="#94a3b8" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="end">$0</text>

  <line x1="100" y1="445" x2="920" y2="445" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="90" y="449" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="end">-$50k</text>

  <!-- Vertical Month Markers (0, 3, 6, 9, 12 Months / 0, 91, 182, 273, 365 Days) -->
  <!-- X: 100, 305, 510, 715, 920 -->
  <line x1="305" y1="100" x2="305" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="305" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">Day 90 (Q1)</text>

  <line x1="510" y1="100" x2="510" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="510" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">Day 180 (Q2)</text>

  <line x1="715" y1="100" x2="715" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="715" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">Day 270 (Q3)</text>

  <line x1="920" y1="100" x2="920" y2="490" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="920" y="508" fill="#64748b" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">Day 365 (Q4)</text>

  <!-- Shaded Envelopes -->
  <!-- Upside Envelope: 90% CI (ends between y=105 and y=145) -->
  <polygon points="100,390 305,320 510,240 715,160 920,105 920,145 715,200 510,280 305,345 100,390" fill="url(#upsideArea)"/>
  <!-- Upside Median Trajectory (ends at y=122 / +$304.5k) -->
  <polyline points="100,390 150,380 220,355 305,330 400,295 510,255 620,215 715,175 820,145 920,122" fill="none" stroke="#10b981" stroke-width="3"/>
  <circle cx="920" cy="122" r="5" fill="#10b981" stroke="#f8fafc" stroke-width="1.5"/>

  <!-- Base Envelope: 90% CI (ends between y=300 and y=325) -->
  <polygon points="100,390 305,375 510,355 715,335 920,300 920,325 715,350 510,370 305,385 100,390" fill="url(#baseArea)"/>
  <!-- Base Median Trajectory (ends at y=312 / +$59.1k) -->
  <polyline points="100,390 150,388 220,382 305,372 400,360 510,348 620,335 715,322 820,315 920,312" fill="none" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="920" cy="312" r="4.5" fill="#38bdf8" stroke="#f8fafc" stroke-width="1.5"/>

  <!-- Conservative Envelope & Trajectory (ends at y=418 / -$20.9k) -->
  <polygon points="100,390 305,398 510,405 715,415 920,428 920,412 715,404 510,398 305,394 100,390" fill="url(#consArea)"/>
  <polyline points="100,390 150,393 220,397 305,401 400,405 510,410 620,413 715,416 820,417 920,418" fill="none" stroke="#f43f5e" stroke-width="2" stroke-dasharray="5,3"/>
  <circle cx="920" cy="418" r="4" fill="#f43f5e" stroke="#f8fafc" stroke-width="1.5"/>

  <!-- Callout Annotations -->
  <!-- Upside Callout -->
  <g transform="translate(680, 115)">
    <rect width="230" height="42" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="1" opacity="0.95"/>
    <text x="115" y="18" fill="#34d399" font-size="12" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">UPSIDE: +$304,589 / yr</text>
    <text x="115" y="34" fill="#94a3b8" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">ROCS: 14.30x | Sharpe: 3.42</text>
  </g>

  <!-- Base Callout -->
  <g transform="translate(680, 275)">
    <rect width="230" height="42" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="1" opacity="0.95"/>
    <text x="115" y="18" fill="#38bdf8" font-size="12" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">BASE: +$59,153 / yr</text>
    <text x="115" y="34" fill="#94a3b8" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">ROCS: 4.50x | Sharpe: 1.88</text>
  </g>

  <!-- Conservative Callout -->
  <g transform="translate(680, 430)">
    <rect width="230" height="42" rx="6" fill="#1e293b" stroke="#f43f5e" stroke-width="1" opacity="0.95"/>
    <text x="115" y="18" fill="#fb7185" font-size="12" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">CONSERVATIVE: -$20,965 / yr</text>
    <text x="115" y="34" fill="#94a3b8" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">ROCS: 0.40x | Insolvent Bleed</text>
  </g>

  <!-- Bottom Legend -->
  <g transform="translate(100, 528)">
    <line x1="0" y1="8" x2="25" y2="8" stroke="#10b981" stroke-width="3"/>
    <text x="35" y="12" fill="#e2e8f0" font-size="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Upside (Web3 Dominant)</text>

    <line x1="240" y1="8" x2="265" y2="8" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="275" y="12" fill="#e2e8f0" font-size="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Base (Adversarial Hybrid)</text>

    <line x1="480" y1="8" x2="505" y2="8" stroke="#f43f5e" stroke-width="2" stroke-dasharray="5,3"/>
    <text x="515" y="12" fill="#e2e8f0" font-size="12" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Conservative (Web2 Heavy)</text>

    <rect x="740" y="3" width="12" height="10" fill="#38bdf8" fill-opacity="0.3"/>
    <text x="760" y="12" fill="#94a3b8" font-size="11" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">90% Confidence Interval</text>
  </g>
</svg>"""
    filepath.write_text(svg.strip(), encoding="utf-8")


def build_sensitivity_heatmap_svg(filepath: Path):
    width, height = 1000, 560
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad4" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{width}" height="{height}" fill="url(#bgGrad4)" rx="12" stroke="#1e293b" stroke-width="1.5" />

  <!-- Title & Subtitle -->
  <text x="50" y="46" fill="#f8fafc" font-size="20" font-weight="700" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">Return on Compute Spend (ROCS) Parameter Sensitivity Matrix</text>
  <text x="50" y="70" fill="#94a3b8" font-size="13" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">2D Heatmap: ROCS Multiple as a Function of Duplicate Collision Rate (%) and Triage Settlement Latency (Days)</text>

  <!-- Matrix Coordinates:
       X columns: Triage Latency: 3d, 7d, 14d, 21d, 30d, 45d, 60d (7 columns)
       Y rows: Duplicate Rate: 15%, 25%, 35%, 50%, 65%, 80%, 90% (7 rows)
       Grid Area: Left x=180, Top y=100.
       Col Width: 95px * 7 = 665px -> ends at x=845.
       Row Height: 48px * 7 = 336px -> ends at y=436.
  -->

  <!-- Axis Titles -->
  <text x="512" y="92" fill="#38bdf8" font-size="12" font-weight="bold" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" text-anchor="middle">TRIAGE SETTLEMENT LATENCY (DAYS) →</text>
  <text x="35" y="270" fill="#f43f5e" font-size="12" font-weight="bold" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" text-anchor="middle" transform="rotate(-90 35 270)">DUPLICATE COLLISION RATE (%) →</text>

  <!-- Column Headers -->
  <g transform="translate(180, 100)">
    <text x="47" y="-6" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">3 Days</text>
    <text x="142" y="-6" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">7 Days</text>
    <text x="237" y="-6" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">14 Days</text>
    <text x="332" y="-6" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">21 Days</text>
    <text x="427" y="-6" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">30 Days</text>
    <text x="522" y="-6" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">45 Days</text>
    <text x="617" y="-6" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="middle">60 Days</text>
  </g>

  <!-- Row Headers (Y) -->
  <g transform="translate(165, 100)">
    <text x="0" y="28" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="end">15%</text>
    <text x="0" y="76" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="end">25%</text>
    <text x="0" y="124" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="end">35%</text>
    <text x="0" y="172" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="end">50%</text>
    <text x="0" y="220" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="end">65%</text>
    <text x="0" y="268" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="end">80%</text>
    <text x="0" y="316" fill="#cbd5e1" font-size="11" font-family="monospace, sans-serif" text-anchor="end">90%</text>
  </g>

  <!-- Heatmap Cells Matrix: (row, col) -->
  <!-- Color Palette:
       Emerald Green (>12x): #065f46 text #34d399
       Teal Green (8-12x): #0f766e text #2dd4bf
       Cyan Blue (4-8x): #0369a1 text #38bdf8
       Amber (1.0-4x): #78350f text #fbbf24
       Crimson Insolvent (<1.0x): #881337 text #fb7185
  -->
  <g transform="translate(180, 100)">
    <!-- Row 0: 15% Dup -->
    <rect x="2" y="2" width="91" height="44" rx="4" fill="#065f46"/><text x="47" y="28" fill="#34d399" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">18.7x</text>
    <rect x="97" y="2" width="91" height="44" rx="4" fill="#065f46"/><text x="142" y="28" fill="#34d399" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">18.2x</text>
    <rect x="192" y="2" width="91" height="44" rx="4" fill="#065f46"/><text x="237" y="28" fill="#34d399" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">17.4x</text>
    <rect x="287" y="2" width="91" height="44" rx="4" fill="#0f766e"/><text x="332" y="28" fill="#2dd4bf" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">16.1x</text>
    <rect x="382" y="2" width="91" height="44" rx="4" fill="#0f766e"/><text x="427" y="28" fill="#2dd4bf" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">14.8x</text>
    <rect x="477" y="2" width="91" height="44" rx="4" fill="#0369a1"/><text x="522" y="28" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">12.5x</text>
    <rect x="572" y="2" width="91" height="44" rx="4" fill="#0369a1"/><text x="617" y="28" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">10.2x</text>

    <!-- Row 1: 25% Dup -->
    <rect x="2" y="50" width="91" height="44" rx="4" fill="#065f46"/><text x="47" y="76" fill="#34d399" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">16.5x</text>
    <rect x="97" y="50" width="91" height="44" rx="4" fill="#065f46"/><text x="142" y="76" fill="#34d399" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">16.0x</text>
    <rect x="192" y="50" width="91" height="44" rx="4" fill="#0f766e"/><text x="237" y="76" fill="#2dd4bf" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">15.2x</text>
    <rect x="287" y="50" width="91" height="44" rx="4" fill="#0f766e"/><text x="332" y="76" fill="#2dd4bf" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">14.0x</text>
    <rect x="382" y="50" width="91" height="44" rx="4" fill="#0369a1"/><text x="427" y="76" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">12.9x</text>
    <rect x="477" y="50" width="91" height="44" rx="4" fill="#0369a1"/><text x="522" y="76" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">10.8x</text>
    <rect x="572" y="50" width="91" height="44" rx="4" fill="#0369a1"/><text x="617" y="76" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">8.9x</text>

    <!-- Row 2: 35% Dup (Web3 Baseline) -->
    <rect x="2" y="98" width="91" height="44" rx="4" fill="#065f46"/><text x="47" y="124" fill="#34d399" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">15.1x</text>
    <rect x="97" y="98" width="91" height="44" rx="4" fill="#065f46"/><text x="142" y="124" fill="#34d399" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">14.8x</text>
    <!-- Web3 Optimal Target: 35% Dup, 14 Days -->
    <rect x="192" y="98" width="91" height="44" rx="4" fill="#065f46" stroke="#f8fafc" stroke-width="2.5"/><text x="237" y="124" fill="#f8fafc" font-size="14" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">14.3x ★</text>
    <rect x="287" y="98" width="91" height="44" rx="4" fill="#0f766e"/><text x="332" y="124" fill="#2dd4bf" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">12.9x</text>
    <rect x="382" y="98" width="91" height="44" rx="4" fill="#0369a1"/><text x="427" y="124" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">11.6x</text>
    <rect x="477" y="98" width="91" height="44" rx="4" fill="#0369a1"/><text x="522" y="124" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">9.4x</text>
    <rect x="572" y="98" width="91" height="44" rx="4" fill="#0369a1"/><text x="617" y="124" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">7.6x</text>

    <!-- Row 3: 50% Dup -->
    <rect x="2" y="146" width="91" height="44" rx="4" fill="#0f766e"/><text x="47" y="172" fill="#2dd4bf" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">11.2x</text>
    <rect x="97" y="146" width="91" height="44" rx="4" fill="#0f766e"/><text x="142" y="172" fill="#2dd4bf" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">10.8x</text>
    <rect x="192" y="146" width="91" height="44" rx="4" fill="#0369a1"/><text x="237" y="172" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">9.9x</text>
    <rect x="287" y="146" width="91" height="44" rx="4" fill="#0369a1"/><text x="332" y="172" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">8.8x</text>
    <rect x="382" y="146" width="91" height="44" rx="4" fill="#0369a1"/><text x="427" y="172" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">7.7x</text>
    <rect x="477" y="146" width="91" height="44" rx="4" fill="#0369a1"/><text x="522" y="172" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">5.9x</text>
    <rect x="572" y="146" width="91" height="44" rx="4" fill="#78350f"/><text x="617" y="172" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">4.2x</text>

    <!-- Row 4: 65% Dup -->
    <rect x="2" y="194" width="91" height="44" rx="4" fill="#0369a1"/><text x="47" y="220" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">7.8x</text>
    <rect x="97" y="194" width="91" height="44" rx="4" fill="#0369a1"/><text x="142" y="220" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">7.4x</text>
    <rect x="192" y="194" width="91" height="44" rx="4" fill="#0369a1"/><text x="237" y="220" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">6.5x</text>
    <rect x="287" y="194" width="91" height="44" rx="4" fill="#0369a1"/><text x="332" y="220" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">5.6x</text>
    <rect x="382" y="194" width="91" height="44" rx="4" fill="#78350f"/><text x="427" y="220" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">4.8x</text>
    <rect x="477" y="194" width="91" height="44" rx="4" fill="#78350f"/><text x="522" y="220" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">3.4x</text>
    <rect x="572" y="194" width="91" height="44" rx="4" fill="#78350f"/><text x="617" y="220" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">2.1x</text>

    <!-- Row 5: 80% Dup -->
    <rect x="2" y="242" width="91" height="44" rx="4" fill="#78350f"/><text x="47" y="268" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">4.2x</text>
    <rect x="97" y="242" width="91" height="44" rx="4" fill="#78350f"/><text x="142" y="268" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">3.9x</text>
    <rect x="192" y="242" width="91" height="44" rx="4" fill="#78350f"/><text x="237" y="268" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">3.2x</text>
    <rect x="287" y="242" width="91" height="44" rx="4" fill="#78350f"/><text x="332" y="268" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">2.5x</text>
    <rect x="382" y="242" width="91" height="44" rx="4" fill="#78350f"/><text x="427" y="268" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">1.8x</text>
    <rect x="477" y="242" width="91" height="44" rx="4" fill="#881337"/><text x="522" y="268" fill="#fb7185" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">0.9x</text>
    <rect x="572" y="242" width="91" height="44" rx="4" fill="#881337"/><text x="617" y="268" fill="#fb7185" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">0.5x</text>

    <!-- Row 6: 90% Dup (Web2 Insolvent Zone) -->
    <rect x="2" y="290" width="91" height="44" rx="4" fill="#78350f"/><text x="47" y="316" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">1.9x</text>
    <rect x="97" y="290" width="91" height="44" rx="4" fill="#78350f"/><text x="142" y="316" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">1.7x</text>
    <rect x="192" y="290" width="91" height="44" rx="4" fill="#78350f"/><text x="237" y="316" fill="#fbbf24" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">1.3x</text>
    <rect x="287" y="290" width="91" height="44" rx="4" fill="#881337"/><text x="332" y="316" fill="#fb7185" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">0.9x</text>
    <rect x="382" y="290" width="91" height="44" rx="4" fill="#881337"/><text x="427" y="316" fill="#fb7185" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">0.7x</text>
    <!-- Web2 Public Bug Bounty Reality: 85-90% Dup, 45-60 Days Latency -->
    <rect x="477" y="290" width="91" height="44" rx="4" fill="#881337" stroke="#fb7185" stroke-width="2"/><text x="522" y="316" fill="#fb7185" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">0.4x ✖</text>
    <rect x="572" y="290" width="91" height="44" rx="4" fill="#881337"/><text x="617" y="316" fill="#fb7185" font-size="13" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">0.25x</text>
  </g>

  <!-- Legend & Regime Explanations at Bottom -->
  <g transform="translate(180, 460)">
    <rect x="0" y="0" width="18" height="18" rx="3" fill="#065f46"/>
    <text x="26" y="14" fill="#cbd5e1" font-size="11" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">ROCS &gt; 12x (Hyper-Productive)</text>

    <rect x="200" y="0" width="18" height="18" rx="3" fill="#0369a1"/>
    <text x="226" y="14" fill="#cbd5e1" font-size="11" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">ROCS 5x–12x (Strong Growth)</text>

    <rect x="400" y="0" width="18" height="18" rx="3" fill="#78350f"/>
    <text x="426" y="14" fill="#cbd5e1" font-size="11" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">ROCS 1x–5x (Marginal)</text>

    <rect x="580" y="0" width="18" height="18" rx="3" fill="#881337"/>
    <text x="606" y="14" fill="#fb7185" font-size="11" font-weight="bold" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">ROCS &lt; 1.0x (Insolvent Bleed)</text>
  </g>

  <!-- Side Note Callout Right -->
  <g transform="translate(860, 160)">
    <rect width="120" height="120" rx="8" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
    <text x="60" y="24" fill="#34d399" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">★ Web3 Sweetspot</text>
    <text x="60" y="44" fill="#cbd5e1" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">Dup Rate: 35%</text>
    <text x="60" y="62" fill="#cbd5e1" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">Latency: 14d</text>
    <text x="60" y="82" fill="#38bdf8" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">ROCS: 14.3x</text>
    <text x="60" y="102" fill="#94a3b8" font-size="9" font-family="monospace, sans-serif" text-anchor="middle">Cash Cycle: -19d</text>
  </g>
  <g transform="translate(860, 310)">
    <rect width="120" height="120" rx="8" fill="#1e293b" stroke="#f43f5e" stroke-width="1.5"/>
    <text x="60" y="24" fill="#fb7185" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">✖ Web2 Quagmire</text>
    <text x="60" y="44" fill="#cbd5e1" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">Dup Rate: 85%</text>
    <text x="60" y="62" fill="#cbd5e1" font-size="10" font-family="monospace, sans-serif" text-anchor="middle">Latency: 45-60d</text>
    <text x="60" y="82" fill="#f43f5e" font-size="11" font-weight="bold" font-family="monospace, sans-serif" text-anchor="middle">ROCS: 0.40x</text>
    <text x="60" y="102" fill="#94a3b8" font-size="9" font-family="monospace, sans-serif" text-anchor="middle">Cash Cycle: +32d</text>
  </g>
</svg>"""
    filepath.write_text(svg.strip(), encoding="utf-8")


def main():
    print("[*] Generating publication-grade SVG assets...")
    build_ev_comparison_svg(ASSETS_DIR / "ev_comparison.svg")
    print("  -> Created assets/ev_comparison.svg")

    build_kelly_allocation_svg(ASSETS_DIR / "kelly_allocation.svg")
    print("  -> Created assets/kelly_allocation.svg")

    build_financial_trajectories_svg(ASSETS_DIR / "financial_trajectories.svg")
    print("  -> Created assets/financial_trajectories.svg")

    build_sensitivity_heatmap_svg(ASSETS_DIR / "sensitivity_heatmap.svg")
    print("  -> Created assets/sensitivity_heatmap.svg")

    # Verify XML well-formedness
    for p in ASSETS_DIR.glob("*.svg"):
        tree = ET.parse(str(p))
        root = tree.getroot()
        assert root.tag.endswith("svg"), f"Tag {root.tag} not ending in svg"
        print(f"  ✔ Verified XML validity: {p.name} (root tag: {root.tag})")

    print("[✔] All 4 SVG assets successfully generated and verified.")


if __name__ == "__main__":
    main()
