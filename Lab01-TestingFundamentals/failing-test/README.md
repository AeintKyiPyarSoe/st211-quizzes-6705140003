# Exception Testing & Failure Analysis

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab01-TestingFundamentals](../README.md)

---

## Overview

This subfolder demonstrates two crucial aspects of automated software testing with Pytest:
1. **Testing Exception Handling:** Verifying that a function correctly raises an expected exception (e.g., `ValueError`) when provided invalid arguments using `with pytest.raises()`.
2. **Failure Analysis & Error Message Matching:** Inspecting Pytest's detailed failure output when an expected error message string does not match the actual exception message via regex matching (`match="..."`).

---

## Files in this Directory

| File | Description |
|---|---|
| [`calculator.py`](./calculator.py) | Arithmetic module containing `divide(a, b)` which raises `ValueError("Cannot divide by zero")` if `b == 0`. |
| [`test_raise_error.py`](./test_raise_error.py) | Test suite testing exception raising with `pytest.raises` and error message verification. |

---

## Concepts & Code Analysis

### 1. Exception Assertion (`test_divide_by_zero_raises`)
```python
import pytest
from calculator import divide

def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(10, 0)
```
- **How it works:** `pytest.raises(ExpectedException)` acts as a context manager. 
- If `divide(10, 0)` raises `ValueError`, the test **passes**.
- If no exception is raised or a different exception type occurs, Pytest fails the test.

---

### 2. Failure Analysis via Regex Matching (`test_divide_by_zero_raises_with_message`)
```python
def test_divide_by_zero_raises_with_message():
    with pytest.raises(ValueError, match="Cannot be divided by zero"):
        divide(5, 0)
```
- **Purpose:** The `match` argument accepts a regular expression to verify that the raised exception's error message contains expected phrasing.
- **Intentional Failure Demonstration:**
  - **Implementation message in `calculator.py`:** `"Cannot divide by zero"`
  - **Expected regex in test:** `"Cannot be divided by zero"`
- Because of this discrepancy, Pytest generates a clear, readable diff explaining exactly why the assertion failed:

```text
___________________ test_divide_by_zero_raises_with_message ___________________

    def test_divide_by_zero_raises_with_message():
>       with pytest.raises(ValueError, match = "Cannot be divided by zero"):
E       AssertionError: Regex pattern did not match.
E         Expected regex: 'Cannot be divided by zero'
E         Actual message: 'Cannot divide by zero'
```

This exercise demonstrates how Pytest produces actionable failure diagnostics, allowing developers to immediately isolate whether the issue lies in business logic or message formatting.

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab01-TestingFundamentals/failing-test -v
```

### From within this Directory:
```bash
python -m pytest test_raise_error.py -v
```

### Expected Output:
- `test_divide_by_zero_raises`: **PASSED**
- `test_divide_by_zero_raises_with_message`: **FAILED** (demonstrating regex mismatch output)
