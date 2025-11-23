# Robust Economic Dispatch Under Uncertain Demand

## Team Name
**OptiMinds**

## Team Members
- **Abhinav Reddy Alwala** – BT2024236
- **Lohith Pasumarthi** – BT2024248
- **Vishal Reddy Kondakindi** – BT2024102

## Project Title
**Robust Economic Dispatch Under Uncertain Demand**

---

## Project Description
This project develops an optimization model to determine optimal production levels across multiple machines in a manufacturing system under uncertain customer demand. Each machine has unique operating costs (quadratic cost curves) and capacity constraints. The model minimizes total production costs while ensuring high reliability in meeting stochastic demand.

We compare two reliability approaches:

1. **Normal (Gaussian) Method**  
   Assumes demand follows a bell-curve distribution and uses statistical quantiles to set safety buffers.

2. **Robust (Distribution-Free) Method**  
   Makes no distributional assumptions beyond mean and variance, using Chebyshev/Cantelli inequalities for worst-case guarantees.

The project quantifies the "price of robustness" – the cost premium for protection against distributional uncertainty.

---

## Libraries Used

### Core Dependencies
- **NumPy** (≥1.21.0) – Array operations and numerical computing
- **pandas** (≥1.3.0) – Data manipulation and tabular display
- **Matplotlib** (≥3.4.0) – Data visualization and plotting
- **SciPy** (≥1.7.0) – Statistical distributions and quantile functions
- **CVXPY** (≥1.2.0) – Convex optimization modeling framework

### Solver
- **OSQP** (installed with CVXPY) – Operator Splitting Quadratic Program solver

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/vishal36-pop/Team-OptiMinds-.git
cd Team-OptiMinds-
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Notebook
```bash
# Open Jupyter Notebook
jupyter notebook Opti.ipynb

# OR use VS Code with Jupyter extension
code Opti.ipynb
```

### 5. Generate LaTeX Report (Optional)
```bash
pdflatex problem_formulation.tex
```

---

## Project Structure
```
Team-OptiMinds-/
├── Opti.ipynb                    # Main analysis notebook
├── problem_formulation.tex       # LaTeX report document
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── (generated plots)             # PNG files for report
```

---

## What the Project Does
- Models a group of machines, each with custom cost curves and capacity limits  
- Converts uncertain demand into a reliable target using two different statistical techniques  
- Builds and solves a convex optimization problem using CVXPY  
- Compares Normal vs Robust modes in terms of:
  - Total cost  
  - Required safety buffer  
  - Machine utilization patterns  
  - Shadow prices (economic signals from the solver)  
- Visualizes results clearly using charts and tables  
- Checks optimality using KKT conditions (industry standard for optimization validation)

---

## Key Concepts (Explained Simply)

### Production System
A set of machines, each with:
- A maximum production capacity  
- A cost that increases faster as the machine produces more  
- A role in meeting the total demand

### Demand Uncertainty
Demand varies from day to day.  
Our model converts this uncertain demand into a “safe target” that ensures reliability.

### Normal vs Robust Reliability
- **Normal:** Works when demand is stable and predictable  
- **Robust:** Works even when demand is irregular, extreme, or unpredictable  
- **Trade-off:** Robust mode is safer but costs more

### Shadow Price
This is the “cost pressure” of meeting one more unit of demand.  
It increases when machines become scarce or hit their capacity limits.

---

## Implementation Summary (Notebook: `Opti.ipynb`)
The project is implemented entirely in Python using the following components:

1. **Data and Parameter Setup**
   - Randomized cost curves and machine capacities
   - Demand statistics (mean and variability)
   - Reliability setting

2. **Reliability Target Generator**
   - Converts uncertain demand to a safe target for both Normal and Robust modes

3. **Optimization Engine**
   - Uses CVXPY to solve a quadratic program
   - Finds the lowest-cost production plan that meets reliability and capacity rules

4. **Dual and KKT Analysis**
   - Extracts dual variables to understand economic behavior
   - Checks optimality conditions for correctness

5. **Visualization**
   - Production levels per machine
   - Cost breakdowns
   - Buffer comparison (Normal vs Robust)
   - Demand-to-cost curves
   - Reliability sensitivity charts

---

## Project Insights
- The **Robust** approach consistently requires a larger safety buffer compared to the **Normal** method.  
- This increased buffer causes:
  - Higher total cost  
  - More machines operating closer to maximum capacity  
  - Higher shadow price (indicating tighter system constraints)

- The **Normal** method is more cost-efficient but assumes demand behaves nicely.  
- The **Robust** method is better when demand risk is high or when the system must be extremely reliable.

---

## Environment Setup
This project includes a `requirements.txt` file for easy setup.

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt