# Parametrized Fixtures in Pytest

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab05-Parametrization](../README.md)

---

## Overview

In integration and system testing, test suites must often verify the same business logic against multiple environments, such as different database backends (SQLite, PostgreSQL, MySQL) or multiple web browsers (Chrome, Firefox, Safari).

Writing separate test functions or manually iterating through configurations violates test isolation and the DRY principle. Pytest solves this with **Parametrized Fixtures**. By supplying the `params` argument to `@pytest.fixture`, Pytest automatically re-executes every dependent test function once for each parameter value.

---

## Files in this Directory

| File | Description |
|---|---|
| [`test_param_fixture.py`](./test_param_fixture.py) | Parametrized fixture providing multiple database engines (`sqlite`, `postgresql`, `mysql`) via `request.param`. |
| [`test_browser.py`](./test_browser.py) | Parametrized browser fixture with setup and teardown lifecycle management using Python's `yield` statement. |

---

## Technical Details

### 1. Basic Parametrized Fixtures (`test_param_fixture.py`)

A fixture is parametrized by specifying a sequence of items in `params`:

```python
import pytest

@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    # request is a built-in Pytest fixture providing metadata about the test
    return request.param

def test_database_connection(database_type):
    print(f"\n Testing with {database_type}")
    assert database_type in ["sqlite", "postgresql", "mysql"]
```

#### How it Works:
1. `request` is a built-in Pytest fixture that exposes the `param` attribute containing the current item from `params`.
2. Any test taking `database_type` as an argument is executed 3 times:
   - `test_database_connection[sqlite]`
   - `test_database_connection[postgresql]`
   - `test_database_connection[mysql]`

---

### 2. Parametrized Fixtures with Setup & Teardown (`test_browser.py`)

Using `yield` inside a parametrized fixture allows managing resource lifecycles (such as starting and stopping simulated browser drivers) cleanly across all configurations:

```python
import pytest

@pytest.fixture(params=["chrome", "firefox", "safari"])
def browser(request):
    browser_name = request.param
    print(f"\n [setup] Launching {browser_name}")
    yield browser_name  # Hand control over to the test function
    print(f"\n [teardown] Closing {browser_name}")

def test_page_load(browser):
    assert browser is not None

def test_browser_clickable(browser):
    assert len(browser) > 0
```

#### Multiplicative Execution:
- There are 2 test functions (`test_page_load` and `test_browser_clickable`).
- There are 3 browser configurations (`chrome`, `firefox`, `safari`).
- **Total Test Runs:** $2 \times 3 = 6$ tests.
- For every individual test, the fixture executes its **setup** before the test runs, and its **teardown** immediately after the test completes.

---

## Key Differences: Test Parametrization vs. Fixture Parametrization

| Feature | `@pytest.mark.parametrize` | `@pytest.fixture(params=...)` |
|---|---|---|
| **Scope** | Applies only to the single decorated test function. | Automatically applies to *all* test functions requesting the fixture. |
| **Use Case** | Diverse data inputs, calculations, boundary edge cases. | Environmental configurations, databases, browsers, API clients. |
| **Lifecycle** | Injects static data values into arguments. | Injects managed resources with full setup and teardown capabilities. |

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab05-Parametrization/parametrized-fixtures -v
```

### Viewing Setup and Teardown Order:
Add `-s` to display print statements and `--setup-show` to trace fixture lifecycles:
```bash
python -m pytest Lab05-Parametrization/parametrized-fixtures/test_browser.py -v -s --setup-show
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: .../Lab05-Parametrization/parametrized-fixtures
collected 9 items

test_browser.py::test_page_load[chrome] PASSED                           [ 11%]
test_browser.py::test_page_load[firefox] PASSED                          [ 22%]
test_browser.py::test_page_load[safari] PASSED                           [ 33%]
test_browser.py::test_browser_clickable[chrome] PASSED                   [ 44%]
test_browser.py::test_browser_clickable[firefox] PASSED                  [ 55%]
test_browser.py::test_browser_clickable[safari] PASSED                   [ 66%]
test_param_fixture.py::test_database_connection[sqlite] PASSED           [ 77%]
test_param_fixture.py::test_database_connection[postgresql] PASSED       [ 88%]
test_param_fixture.py::test_database_connection[mysql] PASSED            [100%]

============================== 9 passed in 0.10s ==============================
```
