import json
import numpy as np
import scipy.stats as stats
import cvxpy as cp
from typing import Dict, Any, Tuple

class ProductionSystem:
    def __init__(self, n_machines: int = 6, seed: int = 7,
                 alpha_bounds: Tuple[float, float] = (0.05, 0.2),
                 beta_bounds: Tuple[float, float] = (2.0, 5.0),
                 gamma_bounds: Tuple[float, float] = (10.0, 20.0),
                 capacity_bounds: Tuple[float, float] = (50.0, 150.0)):
        rng = np.random.default_rng(seed)
        self.n = n_machines
        self.alpha = rng.uniform(alpha_bounds[0], alpha_bounds[1], n_machines)
        self.beta = rng.uniform(beta_bounds[0], beta_bounds[1], n_machines)
        self.gamma = rng.uniform(gamma_bounds[0], gamma_bounds[1], n_machines)
        self.l = np.zeros(n_machines)
        self.u = rng.uniform(capacity_bounds[0], capacity_bounds[1], n_machines)

    def total_capacity(self) -> float:
        return float(np.sum(self.u))


def solve_dispatch(system: ProductionSystem, mu_D: float, sigma_D: float,
                   reliability: float = 0.95, mode: str = "normal") -> Dict[str, Any]:
    if sigma_D < 0 or mu_D < 0:
        raise ValueError("Demand statistics must be non-negative")
    if not 0.0 < reliability < 1.0:
        raise ValueError("Reliability must lie strictly between 0 and 1")

    x = cp.Variable(system.n)
    alpha_risk = 1.0 - reliability

    if mode == "normal":
        z_score = stats.norm.ppf(reliability)
        D_eff = mu_D + z_score * sigma_D
    elif mode == "robust":
        k_robust = np.sqrt((1 - alpha_risk) / alpha_risk)
        D_eff = mu_D + k_robust * sigma_D
    else:
        raise ValueError("Mode must be 'normal' or 'robust'")

    if D_eff > system.total_capacity() + 1e-6:
        raise ValueError("Effective demand exceeds total capacity")

    objective = cp.Minimize(cp.sum(cp.multiply(system.alpha, x**2) + cp.multiply(system.beta, x)))
    constraints = [cp.sum(x) >= D_eff, x <= system.u, x >= system.l]
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.OSQP, warm_start=True)

    if prob.status not in {"optimal", "optimal_inaccurate"}:
        return {"status": prob.status}

    dispatch = x.value
    total_cost = float(np.sum(system.alpha * dispatch**2 + system.beta * dispatch + system.gamma))
    return {
        "status": prob.status,
        "x": [float(v) for v in dispatch.tolist()],
        "cost": float(total_cost),
        "objective": float(prob.value),
        "D_eff": float(D_eff),
        "lambda": float(constraints[0].dual_value),
        "nu_u": [float(v) for v in constraints[1].dual_value.tolist()],
        "nu_l": [float(v) for v in constraints[2].dual_value.tolist()],
    }


def main():
    system = ProductionSystem(n_machines=6, seed=7)
    mu_D = 350.0
    sigma_D = 40.0
    reliability = 0.95

    normal = solve_dispatch(system, mu_D, sigma_D, reliability=reliability, mode="normal")
    robust = solve_dispatch(system, mu_D, sigma_D, reliability=reliability, mode="robust")

    buffer_normal = normal["D_eff"] - mu_D
    buffer_robust = robust["D_eff"] - mu_D
    extra_buffer = buffer_robust - buffer_normal

    var_cost_normal = float(normal["objective"])
    var_cost_robust = float(robust["objective"])
    fixed_cost = float(np.sum(system.gamma))

    total_normal = var_cost_normal + fixed_cost
    total_robust = var_cost_robust + fixed_cost
    premium_abs = total_robust - total_normal
    premium_pct = (premium_abs / total_normal) * 100 if total_normal > 0 else float("nan")

    lambda_shift = float(robust["lambda"] - normal["lambda"])

    results = {
        "scenario": {
            "mu_D": mu_D,
            "sigma_D": sigma_D,
            "reliability": reliability,
            "seed": 7,
        },
        "normal": normal,
        "robust": robust,
        "metrics": {
            "buffer_normal": buffer_normal,
            "buffer_robust": buffer_robust,
            "extra_buffer_units": extra_buffer,
            "total_cost_normal": total_normal,
            "total_cost_robust": total_robust,
            "premium_abs": premium_abs,
            "premium_pct": premium_pct,
            "lambda_normal": normal["lambda"],
            "lambda_robust": robust["lambda"],
            "lambda_shift": lambda_shift,
            "fixed_cost": fixed_cost,
        },
    }

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("=== Experiment Summary ===")
    print(f"Mean demand: {mu_D} | Std dev: {sigma_D} | Reliability: {reliability}")
    print(f"Normal effective demand: {normal['D_eff']:.2f} (buffer {buffer_normal:.2f})")
    print(f"Robust effective demand: {robust['D_eff']:.2f} (buffer {buffer_robust:.2f})")
    print(f"Extra buffer (robust vs normal): {extra_buffer:.2f} units")
    print(f"Total cost normal: ${total_normal:,.2f}")
    print(f"Total cost robust: ${total_robust:,.2f}")
    print(f"Robust premium: ${premium_abs:,.2f} ({premium_pct:.2f}%)")
    print(f"Shadow price shift (lambda): {lambda_shift:.2f}")
    print("Results saved to results.json")

if __name__ == "__main__":
    main()
