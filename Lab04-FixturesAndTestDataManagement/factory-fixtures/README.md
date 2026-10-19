# Factory Fixtures (Fixtures as Object Generators)

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab04-FixturesAndTestDataManagement](../README.md)

---

## Overview

A standard Pytest fixture returns a single pre-configured object or value. However, tests frequently encounter scenarios where:
1. **Dynamic Arguments are Required:** Different tests need the same object initialized with distinct arguments (e.g., balance = 100 vs. balance = 5000).
2. **Multiple Instances are Needed in a Single Test:** Testing interactions between two or more objects (e.g., transferring funds between Account A and Account B, or comparing User 1 and User 2).
3. **Fixture Explosion Must Be Avoided:** Creating separate fixtures like `account_10`, `account_100`, `account_5000` causes unnecessary bloat and maintenance overhead.

The **Factory Fixture** pattern solves this by having the fixture return an **inner callable function** (a factory) rather than a static object. The test can then call this function repeatedly with custom arguments.

---

## Files in this Directory

| File | Description |
|---|---|
| [`bank.py`](./bank.py) | `BankAccount` domain model handling balances, deposits, and withdrawal constraints. |
| [`test_factory.py`](./test_factory.py) | Basic factory fixture (`make_account`) returning an inner builder function `_make(balance)` to instantiate `BankAccount` objects with customizable balances. |
| [`test_factory_advanced.py`](./test_factory_advanced.py) | Advanced factory fixture (`make_user`) combining dynamic object generation with lifecycle cleanup tracking (`yield` teardown). |

---

## Technical Details

### 1. Basic Factory Pattern (`test_factory.py`)

Instead of returning an instance directly, the fixture defines and returns a nested closure:

```python
import pytest
from bank import BankAccount

@pytest.fixture
def make_account():
    def _make(balance):
        return BankAccount(balance)
    return _make

def test_small_account(make_account):
    account = make_account(100)
    assert account.balance == 100
    
def test_large_account(make_account):
    account = make_account(5000)
    assert account.balance == 5000
    
def test_multiple_accounts(make_account):
    # Instantiating multiple distinct objects within a single test
    a = make_account(100)
    b = make_account(200)
    assert a.balance != b.balance
```

#### Why This Works:
- The fixture `make_account` is injected as a callable function.
- The test decides the exact initialization parameters (`100`, `5000`, `200`).
- Multiple independent objects can be generated in the same test without namespace conflicts.

---

### 2. Advanced Factory with Lifecycle Tracking (`test_factory_advanced.py`)

Factories can also track all generated objects in a local list and perform centralized cleanup when the test finishes:

```python
import pytest

@pytest.fixture
def make_user():
    created = []  # track what we make for cleanup

    def _make(name, role="user"):
        user = {"name": name, "role": role, "active": True}
        created.append(user)
        return user

    yield _make

    # Teardown: executes after the test completes
    print(f"\n[cleanup] created {len(created)} users during test")


def test_default_role(make_user):
    user = make_user("Alice")
    assert user["role"] == "user"


def test_custom_role(make_user):
    user = make_user("Bob", role="admin")
    assert user["role"] == "admin"
```

#### Real-World Applications:
- **Database Entity Cleanup:** A database factory creates test rows and records their IDs in a `created` list. After the test yields, teardown iterates through `created` to run `DELETE FROM users WHERE id IN (...)`.
- **File System Mocking:** A factory creates temporary files and registers their paths. The teardown block unlinks all created paths at once.

---

## Comparison: Standard vs. Factory Fixtures

| Attribute | Standard Fixture | Factory Fixture |
|---|---|---|
| **Return Type** | Object instance (e.g., `BankAccount(100)`) | Callable generator function (`_make(...)`) |
| **Flexibility** | Fixed configuration per fixture | Completely configurable parameters per call |
| **Object Count** | 1 instance per test signature | $N$ instances per test signature |
| **Use Case** | Uniform, static baseline state | Varied parameter states or multi-object interactions |

---

## How to Run the Tests

### From the Repository Root:

```bash
# Run all tests in factory-fixtures
python -m pytest Lab04-FixturesAndTestDataManagement/factory-fixtures -v

# Run with stdout printing (-s) to observe cleanup logs
python -m pytest Lab04-FixturesAndTestDataManagement/factory-fixtures -v -s
```

### From within this Directory:

```bash
# Run both test files
python -m pytest -v -s

# Run only test_factory.py
python -m pytest test_factory.py -v

# Run only test_factory_advanced.py
python -m pytest test_factory_advanced.py -v -s
```

---

## Expected Output

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: .../st211-quizzes-6705140003
collecting ... collected 5 items

Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory.py::test_small_account PASSED
Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory.py::test_large_account PASSED
Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory.py::test_multiple_accounts PASSED
Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory_advanced.py::test_default_role PASSED
[cleanup] created 1 users during test

Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory_advanced.py::test_custom_role PASSED
[cleanup] created 1 users during test


============================== 5 passed in 0.06s ==============================
```
