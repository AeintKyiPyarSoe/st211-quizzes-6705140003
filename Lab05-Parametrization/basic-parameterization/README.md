# Basic Parameterization in Pytest

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab05-Parametrization](../README.md)

---

## Overview

In automated unit testing, testing a function against only a single input is rarely sufficient. Functions often have multiple branches, equivalence partitions, and boundary values. Writing a dedicated `test_*` function for each input value leads to repetitive boilerplate code and maintenance friction.

Pytest provides the `@pytest.mark.parametrize` decorator to solve this problem. It allows developers to define a single test function and execute it repeatedly across a list of distinct inputs and expected outputs. Each iteration is treated by Pytest as an independent test case.

---

## Files in this Directory

| File | Description |
|---|---|
| [`mathutils.py`](./mathutils.py) | Utility module implementing `is_even(n)` (parity check) and `factorial(n)` (iterative factorial with negative input validation). |
| [`test_param.py`](./test_param.py) | Parameterized test suite validating `is_even` against collections of even and odd integers. |
| [`test_factorial.py`](./test_factorial.py) | Parameterized test suite validating `factorial` using paired `(n, expected)` tuples across boundary and equivalence values. |

---

## Technical Details

### 1. The Functions Under Test (`mathutils.py`)

```python
def is_even(n):
    return n % 2 == 0  # True if n is even, False if n is odd

def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):  # Multiply 1 * 2 * 3 * ... * n
        result *= i
    return result
```

- `is_even(n)`: Computes modulo 2 arithmetic to classify parity.
- `factorial(n)`: Implements factorial calculation for non-negative integers ($0! = 1, 1! = 1, \dots$). Raises `ValueError` for negative inputs.

---

### 2. Single-Argument Parameterization (`test_param.py`)

When validating that multiple inputs all produce the same boolean outcome or condition, pass a single parameter name and a sequence of values:

```python
import pytest
from mathutils import is_even

@pytest.mark.parametrize("number", [2, 4, 6, 8, 100])
def test_even_numbers(number):
    assert is_even(number) == True

@pytest.mark.parametrize("number", [1, 3, 5, 7, 99])
def test_odd_numbers(number):
    assert is_even(number) == False
```

#### How Pytest Executes This:
- Pytest discovers `test_even_numbers` and automatically generates 5 separate test cases: `test_even_numbers[2]`, `test_even_numbers[4]`, `test_even_numbers[6]`, `test_even_numbers[8]`, and `test_even_numbers[100]`.
- If one number fails, Pytest isolates the failure and continues executing the remaining test cases.

---

### 3. Paired-Argument Parameterization (`test_factorial.py`)

When each input corresponds to a unique expected output, pass a comma-separated argument string (`"n,expected"`) with a list of tuples `(input, expected)`:

```python
import pytest
from mathutils import factorial

@pytest.mark.parametrize("n,expected", [
    (0, 1),    # Boundary: 0! = 1
    (1, 1),    # Boundary: 1! = 1
    (2, 2),    # 2! = 2
    (3, 6),    # 3! = 6
    (4, 24),   # 4! = 24
    (5, 120),  # 5! = 120
])
def test_factorial(n, expected):
    assert factorial(n) == expected
```

---

## Key Benefits of Parameterization

1. **Elimination of Duplication (DRY):** Assertion logic is written once rather than duplicated across dozens of separate functions.
2. **Granular Failure Reporting:** Unlike looping inside a single test (where the first failure aborts the remaining checks), Pytest tests every parameter independently and reports exact passing and failing cases.
3. **Boundary & Equivalence Coverage:** Boundary values (such as $n = 0$ and $n = 1$) can be explicitly included and verified side-by-side with typical equivalence values.

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab05-Parametrization/basic-parameterization -v
```

### From within this Directory:
```bash
python -m pytest -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: .../Lab05-Parametrization/basic-parameterization
collected 16 items

test_factorial.py::test_factorial[0-1] PASSED                            [  6%]
test_factorial.py::test_factorial[1-1] PASSED                            [ 12%]
test_factorial.py::test_factorial[2-2] PASSED                            [ 18%]
test_factorial.py::test_factorial[3-6] PASSED                            [ 25%]
test_factorial.py::test_factorial[4-24] PASSED                           [ 31%]
test_factorial.py::test_factorial[5-120] PASSED                          [ 37%]
test_param.py::test_even_numbers[2] PASSED                               [ 43%]
test_param.py::test_even_numbers[4] PASSED                               [ 50%]
test_param.py::test_even_numbers[6] PASSED                               [ 56%]
test_param.py::test_even_numbers[8] PASSED                               [ 62%]
test_param.py::test_even_numbers[100] PASSED                             [ 68%]
test_param.py::test_odd_numbers[1] PASSED                                [ 75%]
test_param.py::test_odd_numbers[3] PASSED                                [ 81%]
test_param.py::test_odd_numbers[5] PASSED                                [ 87%]
test_param.py::test_odd_numbers[7] PASSED                                [ 93%]
test_param.py::test_odd_numbers[99] PASSED                               [100%]

============================= 16 passed in 0.11s ==============================
```
