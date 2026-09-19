# Assertion Types: Collections & Floating-Point Precision

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab3-Assertions-Organizations](../README.md)

---

## Overview

This subfolder demonstrates specialized assertion techniques in Pytest:
1. **Floating-Point Precision Testing (`test_floats.py`):** Handling the inherent inaccuracies of binary floating-point representation (IEEE 754) using `pytest.approx()`.
2. **Collection Assertions (`test_collections.py`):** Testing Python data structures (lists, dictionaries, and sets), verifying equality, order-insensitivity, and set operations.

---

## Files in this Directory

| File | Description |
|---|---|
| [`test_floats.py`](./test_floats.py) | Demonstrates floating-point rounding errors and proper assertion using `pytest.approx()`. |
| [`test_collections.py`](./test_collections.py) | Demonstrates deep assertions on lists, dictionaries, and set algebra operations. |

---

## Technical Details

### 1. Floating-Point Precision (`test_floats.py`)

Because computers use binary (base-2) floating point internally, many decimal (base-10) fractions cannot be represented exactly:

$$\frac{1}{10} + \frac{2}{10} = 0.30000000000000004440892098500626...$$

```python
from pytest import approx

def test_float_precision():
    # Pytest's approx() performs tolerance-based comparison
    assert 0.1 + 0.2 == approx(0.3)

def test_float_without_approx_fails():
    # Demonstrates that exact equality fails in standard Python
    assert 0.1 + 0.2 != 0.3
```

- **Without `approx()`:** Comparing floating-point numbers directly with `==` results in brittle, false-negative test failures.
- **With `approx()`:** Pytest checks whether the difference is within a relative tolerance of $1 \times 10^{-6}$ by default, ensuring numerical tests remain robust across different architectures and compilers.

---

### 2. Collection Assertions (`test_collections.py`)

Pytest provides rich diff outputs when comparing data structures:

```python
def test_list_equality():
    # Sequential order and element equality
    assert [1, 2, 3] == [1, 2, 3]

def test_list_contents():
    # Order-independent comparison using sorted()
    result = [3, 2, 1]
    assert sorted(result) == [1, 2, 3]

def test_dict_equality(): 
    # Key-value equivalence regardless of insertion order
    expected = {"Name": "Alice", "Age": 30}
    actual = {"Age": 30, "Name": "Alice"}
    assert actual == expected

def test_set_operations():
    # Set intersection (&): elements common to both sets
    assert {1, 2, 3} & {2, 3, 4} == {2, 3}
    
    # Set union (|): all unique elements combined
    assert {1, 2, 3} | {2, 3, 4} == {1, 2, 3, 4}
    
    # Set difference (-): elements in first set but not second
    assert {1, 2, 3} - {2, 3, 4} == {1}
```

---

## How to Run the Tests

### From the Repository Root:
```bash
# Run all assertion tests
python -m pytest Lab3-Assertions-Organizations/assertion-types -v

# Run floating-point tests
python -m pytest Lab3-Assertions-Organizations/assertion-types/test_floats.py -v

# Run collection tests
python -m pytest Lab3-Assertions-Organizations/assertion-types/test_collections.py -v
```

### From within this Directory:
```bash
python -m pytest -v
```

### Expected Output:
```text
test_collections.py::test_list_equality PASSED
test_collections.py::test_list_contents PASSED
test_collections.py::test_dict_equality PASSED
test_collections.py::test_set_operations PASSED
test_floats.py::test_float_precision PASSED
test_floats.py::test_float_without_approx_fails PASSED
```
