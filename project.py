import random
import time
import numpy as np  # for precise_arctans

PI = 3.1415926535897932384


def taylor(x):
    """
    Computes arctan(x) using Taylor series expansion with range reduction.
    For x < 0: arctan(-x) = -arctan(x)
    For x <= 0.5: computes Taylor series directly via taylor_core
    For 0.5 < x <= 1: arctan(x) = pi/4 + arctan((x-1)/(x+1))
    For x > 1: arctan(x) = pi/2 - arctan(1/x)
    """
    if x < 0:
        return -taylor(-x)
    
    # Handle large values: arctan(x) = pi/2 - arctan(1/x)
    if x > 1:
        return PI / 2 - taylor(1 / x)
    
    # For 0.5 < x <= 1: arctan(x) = pi/4 + arctan((x-1)/(x+1))
    if x > 0.5:
        y = (x - 1) / (x + 1)
        return PI / 4 + taylor_core(y)

    return taylor_core(x)


def taylor_core(x):
    """
    Computes arctan(x) using Taylor series for |x| <= 0.5.
    Series: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
    """
    result = 0.0
    term = x
    n = 1

    for i in range(100):  # Max iterations to prevent infinite loops
        contribution = term / n
        result += contribution
        if abs(contribution) < 1e-17:  # Convergence threshold
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
    missed = [i for i in range(len(error)) if np.abs(error[i]) > 10**(-15)]
    print(missed)

    print(f"Runtime: {runtime:.4f} seconds")
