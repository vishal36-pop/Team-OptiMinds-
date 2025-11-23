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

### Decision Variables
\(x_i\): output of machine \(i\), with \(0 \le x_i \le u_i\)

### Cost Function
\[
C_i(x_i) = \alpha_i x_i^2 + \beta_i x_i + \gamma_i
\]

### Demand Modeling
Random demand \(D\) has:
- Mean: \(\mu_D\)  
- Standard deviation: \(\sigma_D\)  

We convert stochastic demand into a deterministic target:
\[
D_{\text{eff}} = \mu_D + B\sigma_D
\]

**Where:**
- Normal mode: \(B = z_p\)  
- Robust mode: \(B = \sqrt{\tfrac{p}{1-p}}\)

### Optimization Problem
\[
\min_{x} \sum_{i=1}^n (\alpha_i x_i^2 + \beta_i x_i)
\]

Subject to:
\[
\sum x_i \ge D_{\text{eff}}, \qquad 0 \le x_i \le u_i
\]

### Dual Variables
- **\(\lambda\):** Shadow price of demand (cost of requiring 1 more reliable unit)
- **\(\nu_i^u\):** Indicates if machine \(i\) is at full capacity
- **KKT residuals:** Validate optimality

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
