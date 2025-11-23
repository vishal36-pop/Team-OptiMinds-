# README.md

## Team Name
OptiMinds

## Members
- Abhinav Reddy Alwala – <ID_1>
- Lohith Pasumarthi – <ID_2>
- Vishal Reddy Kondakindi – <BT2024102>

## Project Title
Robust Economic Dispatch Under Uncertain Demand

---

## Executive Summary
In this project, we build a robust production planning / economic dispatch model that decides how much each machine should produce when demand is uncertain. Each machine has a convex quadratic cost curve and a hard capacity limit, and we want to meet demand at a required reliability level while minimizing total cost.

We compare two reliability models:

1. **Normal (Quantile) Mode**  
   Assumes demand is roughly Gaussian. This gives a smaller, cheaper safety buffer.

2. **Robust Cantelli/Chebyshev Mode**  
   Makes *no* assumptions about the distribution — only mean and variance.  
   Much safer, but also more expensive.

We solve both formulations using CVXPY, study their outputs, analyze shadow prices and dual variables, verify KKT conditions, and plot everything clearly so the differences are easy to understand. The notebook shows how much extra cost we pay for robustness — basically the **“insurance premium”** of protecting against worst-case demand.

---

## Mathematical Formulation

### Symbol Glossary
| Symbol | Meaning | Notes / Code Name |
|--------|---------|-------------------|
| $n$ | Number of machines | `system.n` |
| $x_i$ | Production of machine $i$ | Decision var (CVXPY variable) |
| $u_i$ | Max capacity of machine $i$ | `system.u[i]` |
| $\ell_i$ | Min capacity (here 0) | `system.l[i] = 0` |
| $\alpha_i$ | Quadratic curvature coeff | `system.alpha[i]` |
| $\beta_i$ | Linear slope coeff | `system.beta[i]` |
| $\gamma_i$ | Fixed cost coeff | `system.gamma[i]` (added post‑solve) |
| $\mu_D$ | Mean demand | Input parameter |
| $\sigma_D$ | Demand std dev | Input parameter |
| $p$ | Reliability (service level) | e.g. $0.95$ |
| $\alpha_{\text{risk}}=1-p$ | Failure probability | Avoid confusing with $\alpha_i$ |
| $D_{\text{eff}}$ | Reliability‑adjusted (effective) demand | Computed per mode |
| $z_p$ | Normal quantile at reliability $p$ | `stats.norm.ppf(p)` |
| $k_p=\sqrt{\tfrac{p}{1-p}}$ | Cantelli buffer factor | Robust mode |
| $\lambda$ | Dual of demand constraint | Shadow price |
| $\nu_i^u$ | Dual of upper capacity | Scarcity indicator |
| $\nu_i^\ell$ | Dual of lower capacity | Usually zero (since $\ell_i=0$) |

We distinguish: Greek $\alpha_i$ (cost curvature) vs $\alpha_{\text{risk}}$ (failure probability). They are unrelated.

### Decision Variables
Capacity bounds: $$0 \le x_i \le u_i \quad i=1,\dots,n.$$

---

### Cost Function
Machine variable cost (used inside the optimization objective) excludes $\gamma_i$ during solve:
$$C_i^{\text{var}}(x_i)=\alpha_i x_i^2 + \beta_i x_i.$$
Reported total (after solve) adds fixed term: $$C_i^{\text{total}}(x_i)=\alpha_i x_i^2 + \beta_i x_i + \gamma_i.$$
Marginal variable cost: $$MC_i(x_i)=\frac{d}{dx_i}(\alpha_i x_i^2 + \beta_i x_i)=2\alpha_i x_i + \beta_i.$$

---

### Demand Modeling
Random demand $D$ (mean $\mu_D$, std $\sigma_D$) is converted to deterministic $$D_{\text{eff}}=\mu_D + B\,\sigma_D.$$ Buffer factor $B$ depends on mode:
$$B = \begin{cases}
z_p & \text{(Normal mode)}\\[4pt]
\sqrt{\dfrac{p}{1-p}} & \text{(Robust Cantelli mode)}
\end{cases}$$
Normal uses quantile $z_p$ of $\mathcal{N}(0,1)$ ensuring $\Pr(D \le D_{\text{eff}})\ge p$. Robust uses a moment bound (no distribution assumption) producing a larger $B$.

---

### Optimization Problem
Convex QP (variable cost objective):
$$\begin{aligned}
\min_{x \in \mathbb{R}^n}\ & \sum_{i=1}^n (\alpha_i x_i^2 + \beta_i x_i)\\
	ext{s.t.}\ & \sum_{i=1}^n x_i \ge D_{\text{eff}},\\
& 0 \le x_i \le u_i,\quad i=1,\dots,n.\end{aligned}$$
Economic signals arise from the Lagrange multipliers $\lambda,\nu_i^u,\nu_i^\ell$.

---

### Dual Variables & KKT
Stationarity of the Lagrangian gives for each free machine ($\nu_i^u=\nu_i^\ell=0$):
$$2\alpha_i x_i + \beta_i = \lambda.$$
Meaning all unconstrained machines share the same marginal cost equal to shadow price $\lambda$. When $x_i=u_i$, $\nu_i^u>0$ lifts the stationarity equation: $$2\alpha_i x_i + \beta_i - \lambda + \nu_i^u = 0.$$ KKT checks in the notebook numerically validate optimality.

---



## Reliability Modeling Modes

### Normal Mode
- Works when demand is well-behaved / Gaussian-like  
- Smaller buffer  
- Lower cost  
- Efficient and standard in many industries  

### Robust Mode
- Makes no distribution assumptions  
- Biggest safety buffer  
- Highest cost  
- Great when demand is volatile, risky, or unknown  

---

## Implementation Architecture (`Opti.ipynb`)

1. **Imports & Setup**  
   numpy, pandas, matplotlib, scipy.stats, cvxpy  

2. **ProductionSystem**  
   - Generates random but reproducible machine cost curves  
   - Sets machine capacities and coefficients  

3. **solve_dispatch**  
   - Builds and solves the quadratic program  
   - Returns production plan, total cost, shadow price, duals  

4. **verify_kkt**  
   - Checks stationarity, primal/dual feasibility, slackness  
   - Ensures the solver reached a valid optimum  

5. **Scenario Comparison**  
   - Runs both Normal and Robust modes  
   - Outputs costs, effective demand, duals, buffer sizes  

6. **Visualization Suite**  
   - Production bar charts  
   - Cost breakdown comparison  
   - Shadow price shifts  
   - Per-machine convex cost curves  
   - Demand vs cost sweeps  
   - Reliability sensitivity curves  
   - Risk distribution plot  

---

## Figures & Key Insights

| Figure Type | What It Shows | Why It Matters |
|-------------|---------------|----------------|
| Production Profile | Which machine produces how much | Robust mode pushes machines to capacity |
| Cost Breakdown | Variable + fixed + buffer | Shows where extra cost comes from |
| Cost Curves | Each machine’s convex cost | Robust mode operates in steeper cost regions |
| Demand → Cost | Total cost under rising demand | Robust cost always higher (safety premium) |
| Reliability Sensitivity | Cost vs reliability target | Higher reliability → much higher cost |
| Risk Distribution | μ, Normal, Robust demand targets | Makes buffer difference easy to see |

---

## Key Economic Signals (Explained Simply)

- **Shadow Price (λ):**  
  How costly it is to demand one more “guaranteed” unit of production.
  
- **Capacity Duals:**  
  Show which machines are maxed out and driving the cost.

- **Buffer Difference:**  
  Robust mode needs more “extra units,” which directly increases cost.

- **Robust Premium (%):**  
  How much more you pay when you decide to be extra safe.

---

## Reproducibility
To make sure results always match:
- Use a fixed seed in `ProductionSystem(seed=...)`
- Use the same CVXPY + OSQP versions
- Run the notebook from top to bottom
- Store Python/package versions in `requirements.txt`

---

## Environment Setup

This project includes a **requirements.txt** file, so setup is easy:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
