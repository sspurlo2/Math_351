import random
import time
import numpy as np

def taylor_core(x):
    result = 0
    term = x
    n = 1
    while True:
        new_result = result + term / n
        if new_result == result:  # stops at machine precision
            break
        result = new_result
        term *= -x * x
        n += 2
    return result

def taylor(x, PI):
    if x < 0:
        return -taylor(-x, PI)

    one = 1
    two = one + one
    four = two + two   # ← define four
    half = one / two

    if x > one:
        return PI / two - taylor(one / x, PI)

    if x > half:
        y = (x - one) / (x + one)
        return PI / four + taylor_core(y)

    return taylor_core(x)

def MyArctan(data_list):
    PI = 16 * taylor_core(1/5) - 4 * taylor_core(1/239)
    return [taylor(x, PI) for x in data_list]
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