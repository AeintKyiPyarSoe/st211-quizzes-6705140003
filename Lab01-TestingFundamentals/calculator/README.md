# Basic Calculator Unit Testing

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab01-TestingFundamentals](../README.md)

---

## Overview

This subfolder provides an introductory demonstration of writing basic unit tests for Python arithmetic functions using the `pytest` test runner. It verifies core operations across multiple test inputs including positive numbers, negative numbers, identity values (zeros), and division operations.

---

## Files in this Directory

| File | Description |
|---|---|
| [`calculator.py`](./calculator.py) | Implementation of arithmetic functions `add(a, b)` and `divide(a, b)` with guard check for zero divisor. |
| [`test_calculator.py`](./test_calculator.py) | Unit test suite containing multiple assertions per test function covering various arithmetic scenarios. |

---

## Code Breakdown

### Source Implementation (`calculator.py`)
```python
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### Test Suite (`test_calculator.py`)
```python
from calculator import add, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
```

### Key Takeaways:
- **Test Discovery:** Pytest automatically detects files named `test_*.py` and executes functions prefixed with `test_`.
- **Multiple Inputs:** `test_add` asserts behavior across positive operands (`2, 3`), opposite signs (`-1, 1`), and neutral elements (`0, 0`).
- **Python Native `assert`:** Unlike other frameworks (e.g. `unittest` with `self.assertEqual`), Pytest uses plain Python `assert` statements, providing detailed introspection upon failure.

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab01-TestingFundamentals/calculator -v
```

### From within this Directory:
```bash
python -m pytest test_calculator.py -v
```

### Expected Output:
```text
test_calculator.py::test_add PASSED
test_calculator.py::test_divide PASSED
```
