def is_even(n):
    return n%2 == 0 # True if n is even, False if n is odd

def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n+1): # Multiply 1 * 2 * 3 * ... * n
        result *= i
    return result