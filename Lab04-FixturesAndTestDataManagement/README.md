# Lab 04: Fixtures & Test Data Management

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

This directory contains the laboratory exercises for **Lab 04: Fixtures & Test Data Management**. The primary focus of this lab is understanding how to structure and inject test dependencies, eliminate boilerplate setup code, and maintain strict test isolation using **Pytest Fixtures**.

In automated testing, test suites rarely operate on static or isolated variables alone. Real-world applications require pre-configured objects, database handles, network stubs, or simulated environments. Pytest solves this through a flexible dependency injection architecture centered around `@pytest.fixture`.

### Key Learning Objectives
1. **Dependency Injection:** Understanding how Pytest discovers and injects dependencies into test functions through argument names.
2. **Eliminating Arrange Bloat:** Decoupling object creation and state initialization from test logic, keeping test functions concise and focused.
3. **Test Isolation:** Enforcing fresh state per test via Pytest's default `function` scoping, preventing test pollution and ordering dependencies.
4. **Maintenance Scalability:** Centralizing setup logic so domain model changes require updates in only one location.

---

## Directory Structure

```text
Lab04-FixturesAndTestDataManagement/
├── fixtures/                                # Core fixture definitions and refactoring
│   ├── bank.py                              # BankAccount domain model implementation
│   ├── test_after.py                        # Test suite refactored with @pytest.fixture
│   └── README.md                            # Detailed fixtures documentation
│
└── README.md                                # Lab 04 comprehensive guide
```

---

## Submodule Summaries

| Submodule | Directory | Key Topics Covered | Guide |
|---|---|---|:---:|
| **1. Fixtures** | [`fixtures/`](./fixtures/) | `@pytest.fixture`, dependency injection, eliminating Arrange duplication, test isolation | [View README](./fixtures/README.md) |

---

## Technical Details

### 1. The Problem: Duplicated Setup (Arrange Bloat)

Before fixtures, tests manually instantiate their dependencies inside each test method:

```python
# Anti-pattern: duplicated object instantiation
def test_deposit():
    account = BankAccount(100)
    account.deposit(50)
    assert account.balance == 150

def test_withdraw():
    account = BankAccount(100)
    account.withdraw(30)
    assert account.balance == 70
```

This violates the DRY (Don't Repeat Yourself) principle. If `BankAccount` requires new constructor arguments, every single test breaks simultaneously.

---

### 2. The Solution: Pytest Fixtures

Pytest introduces a declarative dependency injection pattern:

```python
import pytest
from bank import BankAccount

@pytest.fixture
def account():
    """Provides a fresh BankAccount instance initialized with 100."""
    return BankAccount(100)

def test_deposit(account):
    account.deposit(50)
    assert account.balance == 150

def test_withdraw(account):
    account.withdraw(30)
    assert account.balance == 70
```

### Why Fixtures Excel:
- **Zero Boilerplate:** Test functions declare what they need in their signature (`test_deposit(account)`).
- **Automatic Lifecycle Management:** Pytest executes `account()` before calling `test_deposit`, then executes `account()` again before calling `test_withdraw`.
- **Complete Test Isolation:** Mutating the account balance in one test cannot affect subsequent tests because each receives an isolated instance.

---

## How to Run Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running All Tests in Lab 04:

From the repository root:
```bash
python -m pytest Lab04-FixturesAndTestDataManagement/fixtures -v
```

### Viewing Fixture Setup and Teardown Order:

Pytest includes the `--setup-show` flag to trace exactly when fixtures are created and destroyed:
```bash
python -m pytest Lab04-FixturesAndTestDataManagement/fixtures -v --setup-show
```

### Expected Output:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0
rootdir: .../Lab04-FixturesAndTestDataManagement/fixtures
collected 2 items

test_after.py::test_deposit 
      SETUP    F account
        test_after.py::test_deposit (fixtures used: account) PASSED
      TEARDOWN F account
test_after.py::test_withdraw 
      SETUP    F account
        test_after.py::test_withdraw (fixtures used: account) PASSED
      TEARDOWN F account

============================== 2 passed in 0.08s ==============================
```
