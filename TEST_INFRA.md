# Autonomous Opportunity Arbitrage Engine (AOAE) — E2E Test Infrastructure Specification

> **Document Status**: Production Specification  
> **Target Audience**: Core Developers, QA Engineers, Autonomous Subagents, Security Auditors  
> **Standard**: Zero External Dependencies (Python 3.10+ Standard Library)  
> **Scope**: Tiers 1–4 E2E Test Verification across all 25 PROJECT.md Features  

---

## 1. Executive Summary & Testing Philosophy

The **Autonomous Opportunity Arbitrage Engine (AOAE)** is a high-stakes, capital-allocating autonomous system designed to discover, evaluate, prove, and settle standing-reward opportunities with zero human intervention. A software system operating in adversarial capital environments cannot rely on superficial unit tests or mock facades.

This document defines the architecture, taxonomy, mathematical foundations, and execution contracts of the **AOAE Opaque-Box E2E Test Suite**.

### 1.1 Core Principles

1. **Opaque-Box Requirement Verification**: Tests treat the engine and its deliverables as black boxes, verifying observable interfaces, mathematical properties, data schemas, and runtime contracts derived strictly from `PROJECT.md` and `ORIGINAL_REQUEST.md`.
2. **Zero External Dependencies**: In alignment with the host environment constraints, all test code and execution scripts execute natively using the Python standard library (`unittest`, `math`, `statistics`, `argparse`, `json`, `re`, `xml.etree.ElementTree`, `subprocess`, `pathlib`). No third-party packages (`pytest`, `numpy`, `matplotlib`) are required.
3. **Dual-Track Testing Architecture**:
   - **Track A: Economic & Statistical Simulator Verification (`tests/test_simulator.py`)**: Validates the Monte Carlo financial engine (`scripts/simulate_economics.py`), parameter sensitivities, extreme boundary conditions, Kelly allocation mathematics, and schema conformance.
   - **Track B: Documentation, Asset & Formal Model Integrity (`tests/test_documentation_integrity.py`)**: Enforces zero-placeholder policies, markdown structural correctness, relative link integrity, Mermaid diagram syntax validation, SVG vector asset validity, and mathematical completeness across all 10 deep-dive documents and `README.md`.
4. **Progressive Testability**: The test harness supports staged milestone execution. Deliverables pending completion in active upstream milestones report explicit skips with diagnostic notifications, while completed deliverables undergo uncompromising, exhaustive validation. In Milestone 6, strict mode (`STRICT_E2E=1`) enforces 100% presence and passage.
5. **No Facade Testing**: Every test asserts genuine invariants. Tests fail if mathematical formulas deviate from authoritative derivations or if required schemas omit declared keys.

---

## 2. Four-Tier Testing Taxonomy

The AOAE test suite is organized into a four-tier hierarchical taxonomy spanning over 50 test cases:

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                             AOAE E2E TEST TAXONOMY                                   │
├────────────────────────────────┬─────────────────────────────────────────────────────┤
│ Tier                           │ Verification Objective                              │
├────────────────────────────────┼─────────────────────────────────────────────────────┤
│ Tier 1: Feature Coverage       │ Happy-path validation of CLI options, default runs, │
│ (>= 5 tests per feature)       │ archetypes, JSON schemas, doc existence & structure.│
├────────────────────────────────┼─────────────────────────────────────────────────────┤
│ Tier 2: Boundary & Corners     │ Stress tests at limits: zero budget, 100% duplicate │
│ (>= 5 tests per feature)       │ rates, infinite triage latency, negative budgets,   │
│                                │ zero placeholders (TODO/TBD), invalid CLI flags.    │
├────────────────────────────────┼─────────────────────────────────────────────────────┤
│ Tier 3: Cross-Feature Coupling │ Interaction testing: Kelly sizing vs Monte Carlo    │
│                                │ equity growth, simultaneous JSON/SVG generation,    │
│                                │ relative hyperlink resolution, Mermaid diagram AST. │
├────────────────────────────────┼─────────────────────────────────────────────────────┤
│ Tier 4: Real-World Scenarios   │ End-to-end simulations: 30-day $250 MVE run,        │
│                                │ institutional hedge-fund risk run, zero-touch       │
│                                │ verification pipeline, 28-dimension matrix audit.   │
├────────────────────────────────┼─────────────────────────────────────────────────────┤
│ [Tier 5: Adversarial Hardening]│ Extreme fuzzing, numerical overflow, and mutation   │
│ (Milestone 6 Scope)            │ testing to be executed during final hardening.      │
└────────────────────────────────┴─────────────────────────────────────────────────────┘
```

### 2.1 Tier 1: Feature Coverage
- **Objective**: Guarantee that every documented feature, CLI parameter, document structure, and data model exists and functions according to specification under nominal conditions.
- **Scope**:
  - `scripts/simulate_economics.py`: `--help`, default parameter execution, `--runs`, `--days`, `--archetype web3`, `--archetype web2`, `--output-json`, `--output-svg`, and PRNG seed reproducibility (`--seed`).
  - Documentation: Structural verification of `PROJECT.md`, `README.md`, and all 10 deep-dive documents (`docs/01` to `docs/10`).

### 2.2 Tier 2: Boundary & Corner Cases
- **Objective**: Ensure the system does not crash, divide by zero, emit unhandled exceptions, or violate invariants when pushed to logical, temporal, or financial extremes.
- **Scope**:
  - Financial Limits: Zero daily budget (`--daily-budget 0`), negative budgets (`--daily-budget -100`), zero initial capital (`--initial-capital 0`), zero simulation runs (`--runs 0`), negative runs (`--runs -5`).
  - Market Extremes: 100% duplicate rate (`--duplicate-rate 1.0`), 0% duplicate rate (`--duplicate-rate 0.0`), extreme triage latency (`--triage-latency-days 3650`), zero triage latency (`--triage-latency-days 0`), zero finding rate (`--p-finding 0.0`).
  - Argument Rejection: Graceful non-zero exit when passed invalid flags (e.g., `--invalid-flag-foo`) or unknown archetypes (`--archetype invalid`).
  - Editorial Discipline: Absolute zero-tolerance scan for placeholders (`TODO`, `TBD`, `FIXME`, `XXX`, `lorem ipsum`, unpopulated table cells) across all repository documentation.
  - Formatting Boundaries: Non-empty files, valid UTF-8 encoding without byte-order marks or replacement characters, correct markdown heading depth progression.

### 2.3 Tier 3: Cross-Feature Combinations
- **Objective**: Validate non-linear interactions between disparate subsystems and coupled analytical models.
- **Scope**:
  - Kelly Allocation vs. Capital Trajectory: Validating that positive Kelly fractions ($f^* > 0$) produce non-negative expected capital growth, whereas negative Kelly fractions trigger zero capital allocation.
  - Multi-Modal Asset Generation: Simultaneous export of structured JSON (`--output-json`) and vector visual assets (`--output-svg`), verifying XML well-formedness and JSON schema validity concurrently.
  - Risk Metric Coherence: Mathematical invariants across risk measures:
    $$\text{CVaR}_{95\%} \ge \text{VaR}_{95\%}$$
    $$\text{Sortino Ratio is defined and non-zero when downside volatility exists}$$
  - Documentation Cross-Referencing: Verification that relative hyperlinks between markdown documents and vector assets resolve to valid target files.
  - Visual Diagram Integrity: Lexical analysis of all embedded ` ```mermaid ` code blocks across all markdown documents to ensure valid graph headers and balanced syntactic delimiters.

### 2.4 Tier 4: Real-World Scenarios
- **Objective**: Execute end-to-end mission workflows replicating empirical operational conditions.
- **Scope**:
  - **Scenario 1: 30-Day $250 Minimum Viable Experiment (MVE)**: Simulates the exact parameter regime specified in `docs/10` ($250 initial capital, $8.33 daily budget, 30-day horizon, 1,000 Monte Carlo runs), verifying that spend never exceeds the capital ceiling and that probability of ruin is computed.
  - **Scenario 2: Institutional Hedge-Fund Risk Horizon**: Simulates an institutional scale run ($50,000 capital, 365 days, 5,000 runs), testing statistical stability, annualized Sharpe ratio computation, and drawdown tails.
  - **Scenario 3: Zero-Touch Verification Pipeline**: Headless automated execution that ingests CLI outputs, writes artifacts to disk, parses output JSON, and asserts type contracts across all metrics.
  - **Scenario 4: Master 28-Dimension Matrix Audit**: Programmatic inspection of `docs/05` ensuring all 28 rows (D01–D28) and all 8 archetype columns are fully populated with quantitative values.
  - **Scenario 5: 17 Subsystems Architecture Audit**: Programmatic inspection of `docs/07` ensuring all 17 subsystems contain complete entries across all 6 architectural vectors.

---

## 3. Authoritative Expected Output Derivations

All test assertions are derived from mathematical formulas and verified industry benchmarks documented in `ORIGINAL_REQUEST.md`, `PROJECT.md`, and Explorer Survey handoffs.

### 3.1 Parametric Expected Value (EV) Model
For any opportunity evaluation $i$:
$$\mathbb{E}[\text{EV}_i] = P(\text{eligible}_i) \times P(\text{finding}_i \mid \text{eligible}) \times P(\text{unique}_i \mid \text{finding}) \times P(\text{accepted}_i \mid \text{unique}) \times \text{Payout}_i - \sum \text{Costs}_i$$

#### Web2 Bug Bounty Reference Baseline:
- $P(\text{eligible}) = 0.65$
- $P(\text{finding}) = 0.03$
- $P(\text{unique}) = 0.15$ (85% duplicate rate)
- $P(\text{accepted}) = 0.25$ (75% noise / non-actionable rejection)
- $\text{Payout} = \$300.00$
- $\sum \text{Costs} = \$0.504$ (cloud compute + proxy + LLM token allocation)
- **Derived Expected Yield**:
  $$P(\text{payout}) = 0.65 \times 0.03 \times 0.15 \times 0.25 = 0.00073125$$
  $$\mathbb{E}[\text{Gross Revenue}] = 0.00073125 \times \$300.00 = \$0.219375$$
  $$\mathbb{E}[\text{Net EV}] = \$0.219375 - \$0.504 = \mathbf{-\$0.284625 \text{ per target (Negative EV)}}$$

#### Web3 Smart Contract Research Reference Baseline:
- $P(\text{eligible}) = 1.00$
- $P(\text{finding}) = 0.035$
- $P(\text{unique}) = 0.65$
- $P(\text{accepted}) = 0.98$ (Deterministic EVM local testnet proof)
- $\text{Payout} = \$18,500.00$
- $\sum \text{Costs} = \$14.20$
- **Derived Expected Yield**:
  $$P(\text{payout}) = 1.00 \times 0.035 \times 0.65 \times 0.98 = 0.022295$$
  $$\mathbb{E}[\text{Gross Revenue}] = 0.022295 \times \$18,500.00 = \$412.4575$$
  $$\mathbb{E}[\text{Net EV}] = \$412.4575 - \$14.20 = \mathbf{+\$398.2575 \text{ per target (Positive EV)}}$$
  $$\text{ROIC} = \frac{\$412.4575}{\$14.20} \approx \mathbf{29.04\times (2,804\% \text{ Net Return on Invested Compute})}$$

### 3.2 Multi-Asset Kelly Portfolio Model
The uncoupled Kelly growth optimal fraction $f^*$ for opportunity class $k$ is:
$$f_k^* = \max\left(0, \frac{p_k b_k - (1 - p_k)}{b_k}\right)$$
where $b_k = \frac{\text{Payout}_k - \text{Cost}_k}{\text{Cost}_k}$ is the net odds.
- **Web2 Bug Bounties**: $p_k b_k - (1 - p_k) < 0 \implies f^* = 0.00$ (Capital Allocation Blocked).
- **Web3 Audit Contests**: $p \approx 0.40, b \approx 61.22 \implies f^* \approx 0.390$ (Scaled to 65% portfolio focus).
- **Web3 Standing Critical Bounties**: $p \approx 0.0223, b \approx 1301.8 \implies f^* \approx 0.0215$ (Scaled to 35% portfolio focus).

### 3.3 Financial Risk & Performance Metric Definitions
1. **Value at Risk ($\text{VaR}_{95\%}$)**:
   $$\text{VaR}_{0.95} = -\text{Percentile}_{5\%}(\text{Terminal PnL})$$
2. **Conditional Value at Risk ($\text{CVaR}_{95\%}$ / Expected Shortfall)**:
   $$\text{CVaR}_{0.95} = -\mathbb{E}\left[\text{Terminal PnL} \;\middle|\; \text{Terminal PnL} \le -\text{VaR}_{0.95}\right]$$
   Invariant: $\text{CVaR}_{95\%} \ge \text{VaR}_{95\%}$.
3. **Return on Compute Spend (ROCS)**:
   $$\text{ROCS} = \frac{\sum \text{Realized Revenue}}{\sum \text{Compute Spend}}$$
4. **Annualized Sharpe Ratio**:
   $$\text{Sharpe} = \frac{\mu_{\text{daily}} - \frac{R_f}{365}}{\sigma_{\text{daily}}} \times \sqrt{365} \quad (R_f = 0.04)$$
5. **Sortino Ratio**:
   $$\text{Sortino} = \frac{\mu_{\text{daily}} - \frac{R_f}{365}}{\sigma_{\text{downside}}} \times \sqrt{365}$$

### 3.4 Simulator Output JSON Schema
The simulator output JSON must strictly comply with the following interface contract:

```json
{
  "parameters": {
    "runs": "int",
    "days": "int",
    "initial_capital": "float",
    "daily_budget": "float",
    "archetype": "string"
  },
  "metrics": {
    "mean_profit": "float",
    "median_profit": "float",
    "sharpe_ratio": "float",
    "sortino_ratio": "float",
    "var_95": "float",
    "cvar_95": "float",
    "prob_ruin": "float",
    "roi_percent": "float",
    "rocs": "float"
  }
}
```

---

## 4. Test Suite Inventory & File Map

```
/Users/mb/Documents/antigravity/clever-chandrasekhar/
├── tests/
│   ├── test_simulator.py               # 30+ Unit & Statistical Tests for Simulator Engine
│   ├── test_documentation_integrity.py # 25+ Markdown, Structural, Link, and Visual Integrity Tests
│   └── run_all_tests.sh                # Executable Unified Test Runner Script (Colored CLI)
├── TEST_INFRA.md                       # Test Suite Architecture, Taxonomy & Methodology
├── TEST_READY.md                       # Test Suite Readiness Signal & Feature Matrix
└── PROJECT.md                          # Master Project Index & Feature Inventory
```

---

## 5. Feature Coverage Matrix (F01–F25)

| Feature ID | Feature Name | Test Suite | Test Class | Test Methods |
|---|---|---|---|---|
| **F01** | Executive Verdict & Thesis | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_01_executive_verdict_structure` |
| **F02** | PDF Thesis Teardown & Ad Spend Fallacy | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_02_pdf_thesis_teardown_structure` |
| **F03** | Statutory Legal Analysis (CFAA/CMA) | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_02_pdf_thesis_teardown_structure` |
| **F04** | Five-Step Loop Failure Analysis | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_01_executive_verdict_structure`, `test_tier1_doc_02_pdf_thesis_teardown_structure` |
| **F05** | Formal Parametric EV Model | `test_simulator.py` | `TestTier1FeatureCoverage` | `test_tier1_ev_calculation_reference_web2`, `test_tier1_ev_calculation_reference_web3` |
| **F06** | Verified 2024–2026 Bounty Data | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_03_bounty_economics_structure` |
| **F07** | Web2 Automation Failure Bottlenecks | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_02_pdf_thesis_teardown_structure` |
| **F08** | Audit of 8 Alternative Archetypes | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_04_alternative_ecosystems_structure` |
| **F09** | Master 28-Dimension Matrix | `test_documentation_integrity.py` | `TestTier4DomainIntegrityScenarios` | `test_tier4_master_28_dimension_matrix_integrity` |
| **F10** | Deterministic Verification Theorem | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_06_winning_archetype_structure` |
| **F11** | EV per Compute-Hour Proof | `test_simulator.py` | `TestTier1FeatureCoverage` | `test_tier1_ev_calculation_reference_web3`, `test_tier1_cli_web3_archetype` |
| **F12** | Multi-Asset Kelly Portfolio Model | `test_simulator.py` | `TestTier3CrossFeatureCombinations` | `test_tier3_kelly_allocation_vs_monte_carlo` |
| **F13** | 17 Subsystems Specification | `test_documentation_integrity.py` | `TestTier4DomainIntegrityScenarios` | `test_tier4_17_subsystems_specification_integrity` |
| **F14** | Decoupled Architecture (Brain vs Hands) | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_07_architecture_structure` |
| **F15** | Dual-Agent Adversarial Validator | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_07_architecture_structure` |
| **F16** | High-Fidelity Mermaid Diagrams | `test_documentation_integrity.py` | `TestTier3CrossFeatureLinksAndVisualIntegrity` | `test_tier3_mermaid_diagram_syntax_validation`, `test_tier4_4_required_mermaid_diagrams_in_doc_07` |
| **F17** | 3-Tier Financial Schedules | `test_documentation_integrity.py` | `TestTier4DomainIntegrityScenarios` | `test_tier4_3_tier_financial_schedules_integrity` |
| **F18** | Interactive Monte Carlo Simulator | `test_simulator.py` | `TestTier1FeatureCoverage`, `TestTier2BoundaryAndCornerCases` | `test_tier1_cli_default_run`, `test_tier1_cli_output_json_schema`, `test_tier2_zero_budget`, etc. |
| **F19** | Adversarial Threat Model & Mitigations | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_doc_09_adversarial_analysis_structure` |
| **F20** | 30-Day $250 MVE Blueprint | `test_simulator.py` | `TestTier4RealWorldScenarios` | `test_tier4_30_day_250_dollar_mve_simulation` |
| **F21** | Quantitative Decision Gates | `test_documentation_integrity.py` | `TestTier4DomainIntegrityScenarios` | `test_tier4_mve_decision_gates_integrity` |
| **F22** | Master Executive Gateway (README.md) | `test_documentation_integrity.py` | `TestTier1DocStructureAndExistence` | `test_tier1_readme_structure` |
| **F23** | Programmatic Vector Graphics (`assets/`) | `test_documentation_integrity.py` | `TestTier3CrossFeatureLinksAndVisualIntegrity` | `test_tier3_svg_assets_xml_validity`, `test_tier3_svg_assets_referenced_in_docs` |
| **F24** | Comprehensive E2E Testing Suite | `run_all_tests.sh` | Full Suite Execution | Dual suite execution across all tiers |
| **F25** | Adversarial Coverage Hardening | `run_all_tests.sh` | Milestone 6 Gate | Verification gate and stress tests |

---

## 6. Progressive Testability Framework

To allow seamless parallel development across subagents:
1. **Dynamic Artifact Detection**: When a test evaluates an upstream deliverable that has not yet been authored (e.g. `scripts/simulate_economics.py` during Milestone 2), the test issues an explicit `unittest.skipTest()` with diagnostic milestone details.
2. **Deterministic Passage in Current State**: Running `./tests/run_all_tests.sh` at any point during active development exits with returncode 0 (`OK`), clearly differentiating executed passing tests from gracefully skipped milestone dependencies.
3. **Strict Mode for Final Acceptance (`STRICT_E2E=1`)**: During Milestone 6, setting `export STRICT_E2E=1` converts all skips into mandatory hard failures, ensuring no deliverable is omitted prior to final release.

---

## 7. Execution Guide

### 7.1 Unified Test Runner
To run the full E2E test suite across all tiers:
```bash
./tests/run_all_tests.sh
```

### 7.2 Running Individual Test Suites
To run only the simulator unit and statistical tests:
```bash
python3 -m unittest tests/test_simulator.py -v
```

To run only the documentation and asset integrity tests:
```bash
python3 -m unittest tests/test_documentation_integrity.py -v
```

### 7.3 Running in Strict Mode (Milestone 6)
```bash
STRICT_E2E=1 ./tests/run_all_tests.sh
```

---

## 8. Defect Escalation Protocol

When an assertion failure occurs, follow this decision tree:

```
                  ┌──────────────────────┐
                  │ Test Case Fails      │
                  └──────────┬───────────┘
                             │
            Is failure in test assertion logic 
            or out of sync with PROJECT.md?
                    /                 \
                 YES                   NO
                 /                       \
   ┌───────────────────────┐   ┌───────────────────────────┐
   │ Fix Test Code         │   │ Implementation Defect     │
   │ (QA / Test Writer)    │   │ Escalate to Worker Agent  │
   │ Follow PROJECT.md     │   │ via Orchestrator Handoff  │
   └───────────────────────┘   └───────────────────────────┘
```

1. **Test Defect**: If a test assertion contradicts `PROJECT.md` or `ORIGINAL_REQUEST.md`, update the test to align with the authoritative specification.
2. **Implementation Defect**: If implementation code produces incorrect EV math, violates output JSON schemas, or documentation contains prohibited placeholders (`TODO`/`TBD`), do NOT modify implementation code directly. Escalate the verbatim failure output, file path, and line numbers to the orchestrator for assignment to the relevant worker agent.
