# Multiple Parameters & Cartesian Product Testing

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab05-Parametrization](../README.md)

---

## Overview

Complex real-world functions frequently depend on multiple inputs, configuration flags, or error conditions. Pytest supports:
1. **Multi-Argument Parameterization:** Passing multiple inputs alongside expected outputs in structured tuples.
2. **Parameterized Exception Verification:** Combining parameterization with `pytest.raises` to test invalid inputs efficiently.
3. **Stacked Parameterization (Cartesian Products):** Stacking multiple `@pytest.mark.parametrize` decorators to generate all possible combinations of independent parameters automatically.

---

## Files in this Directory

| File | Description |
|---|---|
| [`discount.py`](./discount.py) | Discount calculation function `apply_discount(price, percent)` with percentage boundary validation ($0 \le \text{percent} \le 100$). |
| [`test_discount.py`](./test_discount.py) | Parameterized test suite validating discounted prices across diverse valid price and percentage combinations. |
| [`test_discount_errors.py`](./test_discount_errors.py) | Parameterized test suite verifying that invalid discount percentages trigger a `ValueError`. |
| [`test_multi.py`](./test_multi.py) | Demonstration of stacked `@pytest.mark.parametrize` decorators generating a Cartesian product matrix ($3 \times 2 = 6$ combinations). |

---

## Technical Details

### 1. The Domain Function (`discount.py`)

```python
def apply_discount(price, percent):
    if percent < 0 or percent > 100:
        raise ValueError("Percent must be between 0 and 100")
    return price * (1 - percent / 100)
```

- Enforces that `percent` must stay within the closed interval $[0, 100]$.
- Calculates the final price using decimal discount factor `1 - percent / 100`.

---

### 2. Multi-Argument Parameterization (`test_discount.py`)

Multiple parameters are declared as a comma-delimited string (`"price,percent,expected"`), matched by a list of 3-tuples:

```python
import pytest
from discount import apply_discount

@pytest.mark.parametrize("price,percent,expected", [
    (100, 0, 100),   # 0% discount boundary (no discount)
    (100, 50, 50),   # 50% discount
    (100, 100, 0),   # 100% discount boundary (free)
    (200, 25, 150),  # 25% discount on 200
    (50, 10, 45),    # 10% discount on 50
    (80, 10, 72),    # 10% discount on 80
])
def test_apply_discount_calculation(price, percent, expected):
    assert apply_discount(price, percent) == expected
```

---

### 3. Parameterized Error Handling (`test_discount_errors.py`)

Parameterization seamlessly pairs with `pytest.raises(...)` to verify boundary violations and out-of-range negative testing:

```python
import pytest
from discount import apply_discount

@pytest.mark.parametrize("bad_percent", [-1, -50, 101, 200])
def test_invalid_percent_raises(bad_percent):
    with pytest.raises(ValueError):
        apply_discount(100, bad_percent)
```

- Tests values strictly below 0 (`-1`, `-50`).
- Tests values strictly above 100 (`101`, `200`).
- Each bad input is tested independently to ensure `ValueError("Percent must be between 0 and 100")` is consistently raised.

---

### 4. Stacked Parameterization & Cartesian Products (`test_multi.py`)

When testing interactions between independent variables, stacking `@pytest.mark.parametrize` generates every possible pair (Cartesian product):

```python
import pytest

@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_combinations(x, y):
    assert x + y > 0
    print(f"\n Testing x={x}, y={y}")
```

#### Generated Matrix ($3 \times 2 = 6$ test executions):
1. `(y=10, x=1)`
2. `(y=10, x=2)`
3. `(y=10, x=3)`
4. `(y=20, x=1)`
5. `(y=20, x=2)`
6. `(y=20, x=3)`

> [!NOTE]
> Pytest evaluates stacked decorators from bottom to top; the inner decorator (`y`) is applied first, then combined with the outer decorator (`x`).

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab05-Parametrization/multiple-parameters -v
```

### To View Print Outputs from Stacked Combinations:
```bash
python -m pytest Lab05-Parametrization/multiple-parameters/test_multi.py -v -s
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: .../Lab05-Parametrization/multiple-parameters
collected 16 items

test_discount.py::test_apply_discount_calculation[100-0-100] PASSED      [  6%]
test_discount.py::test_apply_discount_calculation[100-50-50] PASSED      [ 12%]
test_discount.py::test_apply_discount_calculation[100-100-0] PASSED      [ 18%]
test_discount.py::test_apply_discount_calculation[200-25-150] PASSED     [ 25%]
test_discount.py::test_apply_discount_calculation[50-10-45] PASSED       [ 31%]
test_discount.py::test_apply_discount_calculation[80-10-72] PASSED       [ 37%]
test_discount_errors.py::test_invalid_percent_raises[-1] PASSED           [ 43%]
test_discount_errors.py::test_invalid_percent_raises[-50] PASSED          [ 50%]
test_discount_errors.py::test_invalid_percent_raises[101] PASSED          [ 56%]
test_discount_errors.py::test_invalid_percent_raises[200] PASSED          [ 62%]
test_multi.py::test_combinations[10-1] PASSED                             [ 68%]
test_multi.py::test_combinations[10-2] PASSED                             [ 75%]
test_multi.py::test_combinations[10-3] PASSED                             [ 81%]
test_multi.py::test_combinations[20-1] PASSED                             [ 87%]
test_multi.py::test_combinations[20-2] PASSED                             [ 93%]
test_multi.py::test_combinations[20-3] PASSED                             [100%]

============================= 16 passed in 0.11s ==============================
```
