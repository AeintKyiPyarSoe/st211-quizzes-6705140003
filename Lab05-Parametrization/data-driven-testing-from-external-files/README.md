# Data-Driven Testing from External Files (JSON & CSV)

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab05-Parametrization](../README.md)

---

## Overview

In enterprise testing environments, test datasets are often maintained by QA engineers, domain analysts, or product managers in human-readable external formats like **JSON** and **CSV**. Hardcoding hundreds of test records directly into Python source code creates unnecessary friction and bloat.

**Data-Driven Testing (DDT)** decouples test logic from test data. In Pytest, we can invoke custom helper functions inside `@pytest.mark.parametrize` to parse external files during the test collection phase and populate parameter tables dynamically.

---

## Files in this Directory

| File | Description |
|---|---|
| [`validate.py`](./validate.py) | Login validation logic `is_valid_login(username, password)` requiring non-empty credentials. |
| [`logins.csv`](./logins.csv) | External CSV dataset defining username, password, and expected boolean validity. |
| [`test_cases.json`](./test_cases.json) | External JSON dataset defining input strings and expected uppercase outputs, including a non-string edge case. |
| [`test_csv_driven.py`](./test_csv_driven.py) | Data-driven test reading `logins.csv` using Python's `csv.DictReader` to feed `@pytest.mark.parametrize`. |
| [`test_data_driven.py`](./test_data_driven.py) | Data-driven test loading `test_cases.json` using Python's `json` module to feed string manipulation assertions. |

---

## Technical Details

### 1. The Validation Domain Model (`validate.py`)

```python
def is_valid_login(username, password):
    return bool(username) and bool(password)
```

- Returns `True` only when both `username` and `password` evaluate to truthy non-empty strings.
- Returns `False` if either field is empty or missing.

---

### 2. CSV-Driven Testing (`test_csv_driven.py` & `logins.csv`)

#### The Data File (`logins.csv`):
```csv
username,password,valid
admin,admin123,True
user,pass456,True
hacker,,False
,nopassword,False
```

#### Test Implementation (`test_csv_driven.py`):
```python
import csv
import pytest
from validate import is_valid_login

def load_login_cases():
    cases = []
    with open("logins.csv") as f:
        for row in csv.DictReader(f):
            expected = row["valid"] == "True"  # Convert string to boolean
            cases.append((row["username"], row["password"], expected))
    return cases

@pytest.mark.parametrize("username,password,expected", load_login_cases())
def test_is_valid_login(username, password, expected):
    assert is_valid_login(username, password) == expected
```

#### Execution Matrix:
| Username | Password | Expected | Actual Result | Status |
|---|---|---|---|---|
| `admin` | `admin123` | `True` | `True` | **PASSED** |
| `user` | `pass456` | `True` | `True` | **PASSED** |
| `hacker` | *(empty)* | `False` | `False` | **PASSED** |
| *(empty)* | `nopassword` | `False` | `False` | **PASSED** |

---

### 3. JSON-Driven Testing & Data Type Verification (`test_data_driven.py` & `test_cases.json`)

#### The Data File (`test_cases.json`):
```json
[
    {"input": "hello", "expected": "HELLO"},
    {"input": "world", "expected": "WORLD"},
    {"input": "PyTest", "expected": "PYTEST"},
    {"input": "123abc", "expected": "123ABC"},
    {"input": 1, "expected": 1.00}
]
```

#### Test Implementation (`test_data_driven.py`):
```python
import json
import pytest

def load_cases():
    with open('test_cases.json') as f:
        data = json.load(f)
    return [(case['input'], case['expected']) for case in data]

@pytest.mark.parametrize("text,expected", load_cases())
def test_uppercase(text, expected):
    assert text.upper() == expected
```

#### Analysis of Case 5:
- In cases 1 through 4, string inputs pass string uppercase validation smoothly.
- In case 5 (`{"input": 1, "expected": 1.00}`), `text` is parsed as an `int`. Calling `text.upper()` raises an `AttributeError: 'int' object has no attribute 'upper'`.
- This purposefully highlights a key benefit of external data validation: **catching unexpected data types or malformed external inputs early**.

---

## Key Benefits of External Data-Driven Testing

1. **Separation of Concerns:** Business data and test scenarios can be authored, audited, and updated in spreadsheet tools or databases without touching Python code.
2. **Reusability Across Tools:** The same CSV or JSON test data files can be shared between unit tests, integration tests, and external API test suites.
3. **Dynamic Test Generation:** Adding new test rows to `logins.csv` automatically expands the Pytest test plan without requiring code modifications.

---

## How to Run the Tests

> [!IMPORTANT]
> The helper functions `load_login_cases()` and `load_cases()` read `logins.csv` and `test_cases.json` from the current working directory. Always execute the test runner from within this submodule's directory.

### Run from this Directory:
```bash
# Navigate to the folder (or set cwd) and run:
python -m pytest . -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: .../Lab05-Parametrization/data-driven-testing-from-external-files
collected 9 items

test_csv_driven.py::test_is_valid_login[admin-admin123-True] PASSED      [ 11%]
test_csv_driven.py::test_is_valid_login[user-pass456-True] PASSED        [ 22%]
test_csv_driven.py::test_is_valid_login[hacker--False] PASSED            [ 33%]
test_csv_driven.py::test_is_valid_login[-nopassword-False] PASSED        [ 44%]
test_data_driven.py::test_uppercase[hello-HELLO] PASSED                  [ 55%]
test_data_driven.py::test_uppercase[world-WORLD] PASSED                  [ 66%]
test_data_driven.py::test_uppercase[PyTest-PYTEST] PASSED                [ 77%]
test_data_driven.py::test_uppercase[123abc-123ABC] PASSED                [ 88%]
test_data_driven.py::test_uppercase[1-1.0] FAILED                        [100%]

================================== FAILURES ===================================
____________________________ test_uppercase[1-1.0] ____________________________

text = 1, expected = 1.0

    @pytest.mark.parametrize("text,expected", load_cases())
    def test_uppercase(text, expected):
>       assert text.upper() == expected
E       AttributeError: 'int' object has no attribute 'upper'

test_data_driven.py:11: AttributeError
========================= 1 failed, 8 passed in 0.18s =========================
```
