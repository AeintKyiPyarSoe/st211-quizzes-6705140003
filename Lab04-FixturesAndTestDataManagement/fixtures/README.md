# Pytest Fixtures & Dependency Injection

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab04-FixturesAndTestDataManagement](../README.md)

---

## Overview

In automated unit testing, test suites frequently require pre-configured objects, database connections, sample datasets, or system states before execution. Manually recreating this setup inside every single test leads to **Arrange Bloat**, code duplication, and high maintenance costs.

This directory demonstrates **Pytest Fixtures**—Pytest's dependency injection mechanism for providing reusable, isolated test dependencies to test functions cleanly and declaratively.

---

## Files in this Directory

| File | Description |
|---|---|
| [`bank.py`](./bank.py) | `BankAccount` domain model handling balance tracking, positive deposits, and withdrawal constraints. |
| [`test_after.py`](./test_after.py) | Unit test suite refactored to consume a reusable `@pytest.fixture` dependency. |

---

## Technical Details

### 1. The Domain Model (`bank.py`)

The `BankAccount` class encapsulates standard banking transaction logic:

```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        return self.balance
```

- Initial balance defaults to `0` or a specified amount.
- `deposit(amount)` enforces that amounts must be strictly greater than zero.
- `withdraw(amount)` verifies sufficient balance before deducting funds, raising `ValueError("Insufficient funds.")` on overdraft attempts.

---

### 2. Refactoring to Pytest Fixtures (`test_after.py`)

#### Before Fixtures (Manual Setup Anti-Pattern)
In classical test suites, every test manually constructs its own test objects:

```python
# Repetitive instantiation across every test function
def test_deposit():
    account = BankAccount(100)  # Duplicated Arrange step
    account.deposit(50)
    assert account.balance == 150

def test_withdraw():
    account = BankAccount(100)  # Duplicated Arrange step
    account.withdraw(30)
    assert account.balance == 70
```
*Downside:* If the `BankAccount` constructor changes (e.g., requiring an `account_id` or `currency`), every single test must be updated manually.

#### After Fixtures (Declarative Dependency Injection)
With Pytest fixtures, object creation is centralized into a dedicated fixture function decorated with `@pytest.fixture`:

```python
import pytest
from bank import BankAccount

@pytest.fixture
# Fixture is not a test function; it provides test dependencies
def account():
    return BankAccount(100)

def test_deposit(account):
    account.deposit(50)
    assert account.balance == 150
    
def test_withdraw(account):
    account.withdraw(30)
    assert account.balance == 70
```

---

## Key Principles of Pytest Fixtures

1. **Explicit Dependency Injection:** Test functions declare what they need by listing fixture names as arguments (`def test_deposit(account):`). Pytest inspects the function signature at runtime, executes the corresponding fixture, and passes its return value into the test.
2. **Separation of Concerns:** Test functions focus purely on the **Act** and **Assert** phases of the AAA pattern, leaving the **Arrange** phase to the fixture.
3. **Guaranteed Test Isolation:** By default, fixtures have **function scope** (`scope="function"`). Pytest executes the fixture function anew for each dependent test. 
   - When `test_deposit` runs, it receives a new `BankAccount(100)` instance and modifies its balance to `150`.
   - When `test_withdraw` runs, it receives a fresh, separate `BankAccount(100)` instance. The mutation from `test_deposit` does not contaminate `test_withdraw`.
4. **Maintainability:** If the setup logic or constructor parameters change in the future, only the fixture implementation needs to be modified.

---

## How to Run the Tests

### From the Repository Root:

```bash
# Run all tests in the fixtures folder
python -m pytest Lab04-FixturesAndTestDataManagement/fixtures -v
```

### From within this Directory:

```bash
# Run test suite
python -m pytest test_after.py -v

# Run with fixture setup/teardown execution details
python -m pytest --setup-show -v
```

---

## Expected Output

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0
rootdir: .../Lab04-FixturesAndTestDataManagement/fixtures
collected 2 items

test_after.py::test_deposit PASSED                                       [ 50%]
test_after.py::test_withdraw PASSED                                      [100%]

============================== 2 passed in 0.08s ==============================
```
