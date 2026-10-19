# Sharing Fixtures Globally with `conftest.py`

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab04-FixturesAndTestDataManagement](../README.md)

---

## Overview

When building medium-to-large automated test suites, multiple test files often need the same fixtures (e.g., standard user accounts, authenticated sessions, seed databases). Defining the same fixture repeatedly across multiple `.py` test files violates the DRY (Don't Repeat Yourself) principle.

Pytest resolves this through special configuration and hook files named **`conftest.py`**.

When Pytest discovers tests, it automatically searches for `conftest.py` in the test directory and its parent directories. Any fixture declared inside `conftest.py` is immediately accessible to all test files in that folder tree **without requiring any `import` statements**.

---

## Files in this Directory

| File | Description |
|---|---|
| [`bank.py`](./bank.py) | `BankAccount` domain model handling balances, deposits, and withdrawal constraints. |
| [`conftest.py`](./conftest.py) | Centralized fixture repository defining `empty_account`, `funded_account`, and `sample_users`. |
| [`test_shared_a.py`](./test_shared_a.py) | Unit test module testing initial account balances using fixtures discovered automatically from `conftest.py`. |
| [`test_shared_b.py`](./test_shared_b.py) | Unit test module validating user lists and account withdrawal operations using fixtures discovered from `conftest.py`. |

---

## Technical Details

### 1. The Central Fixture Hub (`conftest.py`)

In `conftest.py`, fixtures are defined normally with `@pytest.fixture`:

```python
import pytest
from bank import BankAccount

@pytest.fixture
def empty_account():
    """Provides a fresh BankAccount with a starting balance of 0."""
    return BankAccount(0)

@pytest.fixture
def funded_account():
    """Provides a fresh BankAccount pre-seeded with 1000 balance."""
    return BankAccount(1000)

@pytest.fixture
def sample_users():
    """Provides a standard list of mock user records for role verification."""
    return [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"},
        {"id": 3, "name": "Carol", "role": "user"},
    ]
```

---

### 2. Consuming Fixtures Across Multiple Files

#### `test_shared_a.py`:
```python
def test_empty_account_starts_at_zero(empty_account):
    assert empty_account.balance == 0
    
def test_funded_account_has_money(funded_account):
    assert funded_account.balance == 1000
```

#### `test_shared_b.py`:
```python
def test_user_count(sample_users):
    assert len(sample_users) == 3

def test_first_user_is_admin(sample_users):
    assert sample_users[0]["role"] == "admin"
    
def test_funded_can_withdraw(funded_account):
    funded_account.withdraw(500)
    assert funded_account.balance == 500
```

Notice that neither test file includes `import conftest` or `from conftest import funded_account`. Pytest handles dependency injection automatically via matching argument names.

---

### 3. Test Isolation Maintained Across Files

Even though `funded_account` is defined once in `conftest.py` and requested in both `test_shared_a.py` and `test_shared_b.py`:
- In `test_shared_b.py`, `test_funded_can_withdraw` executes `funded_account.withdraw(500)`, reducing balance to `500`.
- In `test_shared_a.py`, `test_funded_account_has_money` still asserts `funded_account.balance == 1000`.
- Because the fixture has default `function` scope, Pytest instantiates an independent `BankAccount(1000)` object for each test function regardless of which file it lives in.

---

## Rules & Best Practices for `conftest.py`

> [!CAUTION]
> **Never Import `conftest.py` Manually:**
> Writing `import conftest` or `from conftest import ...` in your test files is a severe anti-pattern in Pytest. It causes Python's module caching system (`sys.modules`) to register duplicate module instances, disrupting fixture discovery and hook registrations.

> [!TIP]
> **Hierarchical Discovery:**
> Pytest searches for `conftest.py` hierarchically. A root `conftest.py` provides fixtures for the entire project, while a subdirectory `conftest.py` can provide fixtures scoped strictly to that package or override parent fixtures.

---

## How to Run the Tests

### From the Repository Root:

```bash
# Run all tests in the sharing-fixtures-with-conftest.py module
python -m pytest Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py -v
```

### From within this Directory:

```bash
# Run both test suites
python -m pytest -v

# Run only test_shared_a.py
python -m pytest test_shared_a.py -v

# Run only test_shared_b.py
python -m pytest test_shared_b.py -v
```

---

## Expected Output

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: .../st211-quizzes-6705140003
collecting ... collected 5 items

Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_a.py::test_empty_account_starts_at_zero PASSED [ 20%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_a.py::test_funded_account_has_money PASSED [ 40%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_b.py::test_user_count PASSED [ 60%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_b.py::test_first_user_is_admin PASSED [ 80%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_b.py::test_funded_can_withdraw PASSED [100%]

============================== 5 passed in 0.05s ==============================
```
