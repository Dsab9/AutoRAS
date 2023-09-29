import numpy as np
from scipy.optimize import minimize

def scipy_nelder_mead():
    initial_values = Man_n_vals
    x0 = np.array(initial_values)
    result = minimize(n_m_function, x0, method='Nelder-Mead',
                                     options={'disp': True, 'xatol': 1e-5, 'maxiter': max_runs})
                                              # 'bounds': (lwr_bounds, uppr_bounds)})
    print(f"Nelder-Mead result: {result}")