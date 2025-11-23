# README.md

## Team Name
OptiMinds

## Members
- Abhinav Reddy Alwala – BT2024236
- Lohith Pasumarthi – BT2024248
- Vishal Reddy Kondakindi – BT2024102

## Project Title
Robust Economic Dispatch Under Uncertain Demand

---

## Overview
This project focuses on building an optimization model that decides how much each machine in a production system should produce when customer demand is uncertain. Each machine has its own operating cost and a limit on how much it can produce. The goal of our model is to meet demand reliably while keeping the total production cost as low as possible.

To handle uncertainty, we compare two different reliability strategies:

1. **Normal (Statistical Quantile) Method**  
   Assumes demand behaves like a bell-curve (Gaussian).  
   This method adds a moderate safety buffer.

2. **Robust (Distribution-Free) Method**  
   Makes no assumptions about the shape of the demand distribution.  
   Only uses the mean and variance of demand.  
   This method creates a larger safety buffer to ensure worst-case protection.

Throughout the project, we analyze how these two approaches impact the total cost, machine usage, and reliability.

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
