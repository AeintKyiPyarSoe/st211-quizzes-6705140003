# Test Independence vs. Shared State

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab02-EffectiveTestCases](../README.md)

---

## Overview

This subfolder demonstrates the critical testing principle of **Test Independence and Isolation**. It directly compares:
1. **The Anti-Pattern (`test_dependent.py`):** Tests that share mutable state via a global object, causing execution order dependence and fragility.
2. **The Best Practice (`test_independent.py`):** Tests that are completely isolated, each creating its own fresh instance, allowing arbitrary execution order and parallelizability.

---

## Files in this Directory

| File | Description |
|---|---|
| [`bank.py`](./bank.py) | `BankAccount` domain implementation. |
| [`test_dependent.py`](./test_dependent.py) | Anti-pattern demonstrating shared mutable state across test functions. |
| [`test_independent.py`](./test_independent.py) | Best practice demonstrating isolated tests with fresh instances. |

---

## Direct Code Comparison

### The Anti-Pattern (`test_dependent.py`)

```python
from bank import BankAccount

# BAD: Shared mutable object across tests
shared_account = BankAccount(100)

def test_a_deposit():
    shared_account.deposit(50)
    assert shared_account.balance == 150

def test_b_withdraw():
    # Relies on test_a_deposit having already run and mutated balance to 150!
    shared_account.withdraw(30)
    assert shared_account.balance == 120
```

#### Why Shared State is Dangerous:
- **Execution Order Dependency:** If tests run out of alphabetical order, or in reverse, `test_b_withdraw` runs against balance `100` and fails (`100 - 30 = 70 != 120`).
- **Cannot Run in Isolation:** Executing `pytest test_dependent.py -k test_b_withdraw` immediately fails because `test_a_deposit` was skipped.
- **Cascading Failures:** If `test_a_deposit` fails or throws an exception, `test_b_withdraw` also fails even if withdrawal logic is completely correct.
- **Impossible to Parallelize:** Test runners that execute tests concurrently (e.g., `pytest-xdist`) cause race conditions on shared state.

---

### The Best Practice (`test_independent.py`)

```python
from bank import BankAccount

# GOOD: Each test instantiates its own isolated, fresh object
def test_deposit_independent():
    account = BankAccount(100)
    account.deposit(50)
    assert account.balance == 150

def test_withdraw_independent():
    account = BankAccount(100)
    account.withdraw(30)
    assert account.balance == 70
```

#### Advantages of Test Independence:
- **Order-Agnostic:** Tests can execute in any sequence, shuffled randomly, or concurrently.
- **Isolatable:** Any individual test can be run independently without running the entire suite.
- **Deterministic:** The starting state of the system is explicit and identical every time.
- **Zero Side Effects:** Changes made inside one test have zero impact on any other test.

---

## How to Run the Tests

### From the Repository Root:
```bash
# Run both test files
python -m pytest Lab02-EffectiveTestCases/dependent-independent-tests -v

# Run only the isolated, best-practice tests
python -m pytest Lab02-EffectiveTestCases/dependent-independent-tests/test_independent.py -v
```

### From within this Directory:
```bash
python -m pytest test_independent.py -v
```

### Expected Output:
```text
test_dependent.py::test_a_deposit PASSED
test_dependent.py::test_b_withdraw PASSED
test_independent.py::test_deposit_independent PASSED
test_independent.py::test_withdraw_independent PASSED
```
