# MATH 351 Coding Project: Arctangent to Machine Precision
# Authors: Sam Spurlock, Michal Klopotowski
# Date: December 5, 2025

import random
import time
import numpy as np  # used in __main__ for precise arctan calculation ONLY

"""
Strategy: arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...
This series converges very slowly for x near 1 and diverges for |x| > 1.

To fix this, we use range reduction:
No matter what x is, we can reduce it to the interval [0, tan(pi/8)]~[0, 0.4142]
Inside this interval, the Taylor series converges quickly.

Large inputs (x > cotan(pi/8) ~ 2.4142): use identity arctan(x) = pi/2 - arctan(1/x)
Medium inputs ([tan(pi/8) < x < cotan(pi/8)]~[0.4142 < x < 2.4142]): use identity arctan(x) = pi/4 + arctan((x-1)/(x+1))
Small inputs (0 <= x <= tan(pi/8)~0.4142): use Taylor series directly
"""


def taylor_coeffs_generator(n: int):
    """
    Generates Taylor series coefficients for arctan(x): (-1)^n / (2n + 1)
    """
    sign = 1.0
    denom = 1.0
    for _ in range(n):
        yield sign / denom
        sign = -sign  # Flip sign
        denom += 2.0  # Increment denominator by 2


def machin_series(x: float, n: int) -> float:
    """
    Computes arctan(x) using Taylor (Maclaurin) series with n_terms.
    arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...
    """
    res, term, x_squared = 0.0, x, x * x
    for coeff in taylor_coeffs_generator(n):
        res += coeff * term
        term *= x_squared
    return res


def compute_pi() -> float:
    """
    Calculates pi to 15 decimal places of precision using Machin's formula:
    pi ~ 16*arctan(1/5) - 4*arctan(1/239)
    """
    return 16.0 * machin_series(0.2, 10) - 4.0 * machin_series(1.0/239.0, 3)


def boundaries():
    """
    Calculates range reduction boundaries [tan(pi/8), cotan(pi/8)] using
    unrolled Newton's method for sqrt(2) to 15 decimal places of precision.
    """
    r = 1.5  # Initial guess for sqrt(2)

    # Loop unrolling 4 iterations
    r = (r + 2.0 / r) * 0.5  # First iteration
    r = (r + 2.0 / r) * 0.5  # Second iteration
    r = (r + 2.0 / r) * 0.5  # Third iteration
    r = (r + 2.0 / r) * 0.5  # Fourth iteration

    # tan(pi/8) = sqrt(2) - 1, cotan(pi/8) = sqrt(2) + 1
    return r - 1.0, r + 1.0


def taylor_coeffs(n: int = 18):
    """
    Generates Taylor series coefficients: (-1)^n / (2n + 1)
    """
    return list(taylor_coeffs_generator(n))


def constants():
    """
    Precomputes constants: pi/2, pi/4, tan(pi/8), cot(pi/8), Taylor coefficients
    """
    pi = compute_pi()
    tan_pi_8, cotan_pi_8 = boundaries()
    coeffs = taylor_coeffs()
    return pi/2.0, pi/4.0, tan_pi_8, cotan_pi_8, coeffs


def MyArctan(data_list):
    # Generate constants
    pi_2, pi_4, tan_pi_8, cotan_pi_8, c = constants()

    # Optimization: Local variable lookup is faster than global/list lookup
    c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17 = c[0:18]

    results = []
    append = results.append  # Local variable lookup optimization
    # Process each input value with range reduction and Taylor series approximation
    for val in data_list:
        # Handle sign
        sign = 1.0
        if val < 0:
            val = -val
            sign = -1.0
        # Range reduction
        # Map everything to [0, tan(pi/8)]~[0, 0.4142]
        offset = 0.0
        if val > cotan_pi_8:
            # val > cotan(pi/8): Use identity arctan(x) = pi/2 - arctan(1/x)
            offset = pi_2
            val = -1.0 / val
        elif val > tan_pi_8:
            # tan(pi/8) < val < cotan(pi/8): Use identity arctan(x) = pi/4 + arctan((x-1)/(x+1))
            offset = pi_4
            val = (val - 1.0) / (1.0 + val)

        # Horner's method for polynomial evaluation expanded to avoid loop overhead
        # This is taylor series for arctan(x)
        x2 = val * val  # x^2

        poly = c17
        poly = c16 + x2 * poly
        poly = c15 + x2 * poly
        poly = c14 + x2 * poly
        poly = c13 + x2 * poly
        poly = c12 + x2 * poly
        poly = c11 + x2 * poly
        poly = c10 + x2 * poly
        poly = c9 + x2 * poly
        poly = c8 + x2 * poly
        poly = c7 + x2 * poly
        poly = c6 + x2 * poly
        poly = c5 + x2 * poly
        poly = c4 + x2 * poly
        poly = c3 + x2 * poly
        poly = c2 + x2 * poly
        poly = c1 + x2 * poly
        poly = c0 + x2 * poly

        # Final result: sign * (offset + x * P(x^2))
        append(sign * (offset + val * poly))

    return results


# What I will do with your code, is to run everything above, and then
if __name__ == "__main__":
    data_list = [random.uniform(-5, 5) for _ in range(10**6)]  # this will be the same for
    precise_arctans = [np.arctan(x) for x in data_list]

    start = time.time()
    output = MyArctan(data_list)
    end = time.time()

    runtime = end - start
    error = [abs(precise_arctans[i] - output[i]) for i in range(10**6)]
    missed = [i for i in range(len(error)) if np.abs(error[i]) > 10**(-15)]
    print(missed)

    print(f"Runtime: {runtime:.4f} seconds")
