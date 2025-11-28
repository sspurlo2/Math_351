import random
import time
import numpy as np  # for precise_arctans


def taylor(x):
    """
    Computes arctan(x) using Taylor series expansion.
    For |x| < 1: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
    For |x| >= 1: uses identity arctan(x) = sign(x) * π/2 - arctan(1/x)
    """
    # Handle large values using identity
    if abs(x) > 1:
        sign = 1 if x > 0 else -1
        return sign * np.pi / 2 - taylor(1 / x)
    
    # Taylor series for |x| < 1
    result = 0.0
    term = x
    n = 1
    
    # Compute terms until convergence (terms become very small)
    for i in range(100):  # Max iterations to prevent infinite loops
        result += term / n
        if abs(term / n) < 1e-15:  # Convergence threshold
            break
        term *= -x * x
        n += 2
    
    return result


def polynomial(x, coeffs):
    """
    Evaluates a polynomial at x with given coefficients.
    Polynomial: coeffs[0] + coeffs[1]*x + coeffs[2]*x² + ...
    """
    result = 0.0
    x_power = 1.0
    for coeff in coeffs:
        result += coeff * x_power
        x_power *= x
    return result


def arctan(data_list):
    """
    Computes arctan for each value in the data_list using Taylor series.
    Returns a list of arctan values.
    """
    results = [taylor(x) for x in data_list]
    return results


# What I will do with your code, is to run everything above, and then
if __name__ == "__main__":
    data_list = [random.uniform(-5, 5) for _ in range(10**6)]  # this will be the same for
    precise_arctans = [np.arctan(x) for x in data_list]
    
    start = time.time()
    output = arctan(data_list)
    end = time.time()
    
    runtime = end - start
    error = [abs(precise_arctans[i] - output[i]) for i in range(10**6)]
    
    print(f"Runtime: {runtime:.4f} seconds")
