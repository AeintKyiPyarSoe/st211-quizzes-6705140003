# Parameter IDs & Test Readability

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab05-Parametrization](../README.md)

---

## Overview

When running parameterized test suites with numerous test cases or complex input structures (such as dictionaries, objects, or custom classes), Pytest's default naming mechanism can produce ambiguous or uninformative test identifiers (e.g., `test_user_has_name[user0]`).

This subfolder demonstrates how to enhance test diagnostics and readability through:
1. **Default Test IDs vs. Custom `ids` List:** Naming test cases explicitly with meaningful labels.
2. **Granular Identifiers with `pytest.param`:** Labeling individual parameter tuples inline.
3. **Targeted Test Marks per Parameter:** Applying marks (such as `@pytest.mark.xfail` or `@pytest.mark.skip`) to specific test cases within a parameterized matrix without marking the entire suite.

---

## Files in this Directory

| File | Description |
|---|---|
| [`test_default_ids.py`](./test_default_ids.py) | Demonstration of Pytest's default naming scheme when parameterizing over complex objects (e.g. `[user0]`, `[user1]`). |
| [`test_custom_ids.py`](./test_custom_ids.py) | Enhancing test identification by supplying a descriptive `ids=[...]` list. |
| [`test_param_ids.py`](./test_param_ids.py) | Using `pytest.param(..., id="...")` to configure explicit names for individual parameter sets. |
| [`test_param_marks.py`](./test_param_marks.py) | Applying individual Pytest markers (`marks=pytest.mark.xfail`) to specific parameter sets using `pytest.param`. |

---

## Technical Details

### 1. Default Naming for Complex Data (`test_default_ids.py`)

When parameter values are dictionaries or non-primitive objects, Pytest cannot stringify them cleanly in the console output, defaulting to numeric indices:

```python
import pytest

@pytest.mark.parametrize("user", [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}, 
])
def test_user_has_name(user):
    assert "name" in user
```

**Pytest output:**
```text
test_default_ids.py::test_user_has_name[user0] PASSED
test_default_ids.py::test_user_has_name[user1] PASSED
```
*Limitation:* If `user0` fails, the test report does not reveal which user dataset caused the failure without opening the traceback.

---

### 2. Custom IDs List (`test_custom_ids.py`)

Supplying the `ids` keyword argument provides readable names for each case:

```python
import pytest

@pytest.mark.parametrize("user", [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}, 
], ids=["alice-adult", "bob-adult"])
def test_user_has_name(user):
    assert "name" in user
```

**Pytest output:**
```text
test_custom_ids.py::test_user_has_name[alice-adult] PASSED
test_custom_ids.py::test_user_has_name[bob-adult] PASSED
```

---

### 3. Inline Identification with `pytest.param` (`test_param_ids.py`)

Instead of maintaining a separate list of string IDs that must align with the parameters, `pytest.param` couples the data and its label in a single line:

```python
import pytest
from discount import apply_discount

@pytest.mark.parametrize("price,percent,expected", [
    pytest.param(100, 0, 100, id="no_discount"), 
    pytest.param(100, 50, 50, id="half_off"), 
    pytest.param(100, 100, 0, id="free"),
])
def test_discount(price, percent, expected):
    assert apply_discount(price, percent) == expected
```

**Pytest output:**
```text
test_param_ids.py::test_discount[no_discount] PASSED
test_param_ids.py::test_discount[half_off] PASSED
test_param_ids.py::test_discount[free] PASSED
```

---

### 4. Per-Case Markers with `pytest.param` (`test_param_marks.py`)

`pytest.param` allows attaching Pytest marks (such as `xfail` or `skip`) directly to an individual parameter set without affecting the remaining test cases:

```python
import pytest

@pytest.mark.parametrize("value,expected", [
    pytest.param(2, 4, id="two_squared"),
    pytest.param(3, 9, id="three_squared"),
    pytest.param(5, 20, id="known_bug",
                 marks=pytest.mark.xfail),  # Known bug: 5**2 = 25, expected 20
])
def test_square(value, expected):
    assert value ** 2 == expected
```

- Cases `two_squared` ($2^2 = 4$) and `three_squared` ($3^2 = 9$) run normally and **PASS**.
- Case `known_bug` ($5^2 = 25 \ne 20$) is reported as **XFAIL (Expected Failure)**, preventing the build/CI pipeline from breaking while tracking the defect.

---

## How to Run the Tests

### From the Repository Root:

> [!NOTE]
> Since `test_param_ids.py` imports `apply_discount` from `multiple-parameters/discount.py`, set `PYTHONPATH` so Python can resolve the module:

**PowerShell (Windows):**
```powershell
$env:PYTHONPATH="Lab05-Parametrization/multiple-parameters"; python -m pytest Lab05-Parametrization/parameter-ids-and-readability -v
```

**Bash / Linux / macOS:**
```bash
PYTHONPATH=Lab05-Parametrization/multiple-parameters python -m pytest Lab05-Parametrization/parameter-ids-and-readability -v
```

### Running Individual Tests:
```powershell
python -m pytest Lab05-Parametrization/parameter-ids-and-readability/test_custom_ids.py -v
python -m pytest Lab05-Parametrization/parameter-ids-and-readability/test_param_marks.py -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: .../Lab05-Parametrization/parameter-ids-and-readability
collected 10 items

test_custom_ids.py::test_user_has_name[alice-adult] PASSED               [ 10%]
test_custom_ids.py::test_user_has_name[bob-adult] PASSED                 [ 20%]
test_default_ids.py::test_user_has_name[user0] PASSED                    [ 30%]
test_default_ids.py::test_user_has_name[user1] PASSED                    [ 40%]
test_param_ids.py::test_discount[no_discount] PASSED                     [ 50%]
test_param_ids.py::test_discount[half_off] PASSED                        [ 60%]
test_param_ids.py::test_discount[free] PASSED                            [ 70%]
test_param_marks.py::test_square[two_squared] PASSED                     [ 80%]
test_param_marks.py::test_square[three_squared] PASSED                   [ 90%]
test_param_marks.py::test_square[known_bug] XFAIL                        [100%]

======================== 9 passed, 1 xfailed in 0.17s =========================
```
