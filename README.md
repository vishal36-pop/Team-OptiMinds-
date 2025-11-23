## Team Name
<TEAM_NAME>

## Members
- <MEMBER_NAME_1> – <ID_1>
- <MEMBER_NAME_2> – <ID_2>
- <MEMBER_NAME_3> – <ID_3>
- <MEMBER_NAME_4> – <ID_4>

## Project Title
<PROJECT_TITLE>

## Executive Summary
We develop a convex stochastic production planning framework that allocates output across heterogeneous machines under uncertain demand. Reliability (service level) requirements are converted into an effective deterministic demand using either Normal (quantile) buffering or a distribution‑free Cantelli/Chebyshev bound. The optimization minimizes quadratic + linear variable costs subject to meeting this reliability‑adjusted target while respecting capacity limits. Dual (shadow) prices and KKT residuals provide economic and optimality validation. Visual analyses quantify the cost premium of robust (distribution‑free) planning versus parametric (Gaussian) assumptions.

## Mathematical Formulation
Decision variables \(x_i\) denote production of machine \(i\) with \(0 \le x_i \le u_i\). Variable cost: \(C_i(x_i)=\alpha_i x_i^2 + \beta_i x_i\); fixed \(\gamma_i\) reported post‑solution. Reliability buffering yields \(D_{eff} = \mu_D + B\sigma_D\) where \(B = z_{p}\) (Normal mode) or \(B = \sqrt{\tfrac{p}{1-p}}\) (Robust Cantelli one‑sided). We solve:
\[
\min_{x} \sum_{i=1}^n (\alpha_i x_i^2 + \beta_i x_i) \quad \text{s.t.} \quad \sum_{i=1}^n x_i \ge D_{eff},\; 0 \le x_i \le u_i.
\]
Dual of demand constraint (\(\lambda\)) gives marginal cost of one more required unit; duals of upper bounds (\(\nu^u_i\)) signal scarcity. Optimality validated via stationarity and complementary slackness residuals.

## Reliability Modeling Modes
- Normal: Parametric quantile buffering (assumes approximate Normal demand). Efficient and typically less conservative.
- Robust: Cantelli (Chebyshev) one‑sided bound; no distributional assumption beyond finite mean/variance, often larger buffer and cost.

## Implementation Architecture (Notebook `Opti.ipynb`)
1. Imports: numpy, pandas, matplotlib, scipy.stats, cvxpy.
2. `ProductionSystem`: Random convex cost curves & capacities (reproducible with seed).
3. `solve_dispatch`: Builds & solves convex QP; returns primal solution and economics (cost, \(\lambda\), capacity duals).
4. `verify_kkt`: Reports stationarity & slackness residuals to confirm near‑optimality.
5. Scenario Comparison: Normal vs Robust runs (cost, effective demand, table, KKT output).
6. Visualization suite: Production profile bars, cost & buffer breakdown, shadow price comparison, per‑machine cost curves, demand vs cost sweep, risk distribution plot, reliability sensitivity curves.

## Figures & Analytical Insights
| Figure | Purpose | Key Insight |
|--------|---------|-------------|
| Production Profile (Grouped Bars) | Compare allocation across reliability modes vs capacities | Robust mode pushes several machines nearer capacity, raising scarcity duals. |
| Cost Breakdown & Buffers (3‑panel) | Variable vs fixed cost, safety buffer size, shadow price \(\lambda\) | Robust buffer increases variable cost and elevates \(\lambda\), quantifying insurance premium. |
| Per‑Machine Cost Curves | Overlay convex curves with chosen Normal/Robust outputs | Robust points move into steeper marginal cost regions—visual driver of premium. |
| Demand vs Total Cost Sweep | Cost trajectories for increasing mean demand | Robust curve consistently above Normal; gap approximates distributional ambiguity cost. |
| Risk Distribution (Vertical Targets) | Mean demand vs Normal and Robust \(D_{eff}\) | Robust target visibly farther right, illustrating conservative buffer selection. |
| Reliability Sensitivity | Cost vs reliability level (feasible range) | Rising reliability amplifies premium; percentage gap grows with buffer factor. |

## Key Economic Signals
- Shadow Price \(\lambda\): Marginal cost of one additional required unit; rises under tighter buffers.
- Capacity Duals \(\nu^u\): Positive values identify binding machines; expansion leverage points.
- Buffer Difference: Extra units in robust mode translate directly into incremental variable spend.
- Premium (%) = (Robust − Normal) / Normal cost; increases with reliability and variance.

## Reproducibility
Use a fixed seed in `ProductionSystem(seed=...)` for deterministic cost coefficients. Record: Python version, CVXPY version, solver (OSQP), and random seed in experiment logs. Ensure consistent reliability list filtering for feasibility (both modes solvable).

## Environment Setup
```powershell
python -m venv venv
./venv/Scripts/Activate.ps1
pip install numpy pandas matplotlib scipy cvxpy
python -c "import cvxpy; print(cvxpy.__version__)"
```
Optional: pin versions in `requirements.txt` for submission.

## How to Run
```powershell
jupyter notebook Opti.ipynb
```
Execute cells top‑to‑bottom. After scenario comparison, re‑run visualization cells to refresh figures if parameters change.

## File Structure
```
LICENSE
README.md
Opti.ipynb              # End-to-end modeling, solving, analysis
problem_formulation.tex # Formal math write-up (LaTeX)
```
Extend with scripts (`run_experiment.py`) or data folder if batching scenarios.

## Results (Populate with Actual Numbers)
- Normal vs Robust total cost: <FILL_COSTS>
- Buffer units difference: <FILL_BUFFER_UNITS>
- Shadow price shift: <FILL_LAMBDA_CHANGE>
- Robust premium (%): <FILL_PREMIUM_PERCENT>

## Limitations & Future Work
- Fixed cost treated additively; startup/non-convex effects omitted.
- Demand modeled only by mean/variance; richer distributions could refine buffer choice.
- Robust bound may be conservative; alternative distributionally robust (Wasserstein) sets could tighten premium.
- Scalability: Larger fleets may benefit from separability exploitation or decomposition.

## Academic Integrity & References
Cite sources for convex optimization (e.g., Boyd & Vandenberghe), distribution-free bounds, and any external data. Replace placeholders before submission.

## Placeholder Checklist
<TEAM_NAME>, member IDs, title, numeric results, premium %, references.

---
Prepared using figures and analysis embedded in `Opti.ipynb`. Update placeholders after final experimental runs.
