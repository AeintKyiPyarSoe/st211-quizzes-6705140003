# Intention-Revealing Test Naming Conventions

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab02-EffectiveTestCases](../README.md)

---

## Overview

This subfolder demonstrates the importance of **Descriptive Test Naming**. Automated tests are not just validation scripts—they are **living documentation** and executable specifications of how the software should behave.

When tests are named clearly and systematically, anyone reviewing test results (e.g., in continuous integration logs or terminal output) can immediately understand what functionality broke without reading the test implementation.

---

## Files in this Directory

| File | Description |
|---|---|
| [`bank.py`](./bank.py) | `BankAccount` domain implementation. |
| [`test_named.py`](./test_named.py) | Unit test suite implementing standardized, descriptive test names. |

---

## Naming Pattern & Examples

A widely recognized standard for naming unit tests is:
$$\text{test\_}\langle\text{action / unit\_under\_test}\rangle\text{\_}\langle\text{condition / scenario}\rangle\text{\_}\langle\text{expected\_result}\rangle$$

### Code from `test_named.py`:

```python
import pytest
from bank import BankAccount

# 1. Positive scenario: depositing valid funds
def test_deposit_positive_amount_increases_balance():   
    account = BankAccount(100)
    account.deposit(50)
    assert account.balance == 150

# 2. Negative scenario: depositing negative funds
def test_deposit_negative_amount_raises_value_error():   
    account = BankAccount(100)
    with pytest.raises(ValueError): 
        account.deposit(-10)

# 3. Negative scenario: overdrawing beyond current balance
def test_withdraw_more_than_balance_raises_value_error():   
    account = BankAccount(100)
    with pytest.raises(ValueError): 
        account.withdraw(200)

# 4. Boundary scenario: withdrawing the exact remaining balance
def test_withdraw_exact_balance_leaves_zero():  
    account = BankAccount(100)
    account.withdraw(100)
    assert account.balance == 0
```

---

## Comparison: Vague vs. Descriptive Names

| Poor Naming (Vague) | Descriptive Naming (Living Specification) | Why It Matters |
|---|---|---|
| `test_deposit` | `test_deposit_positive_amount_increases_balance` | States the exact business rule being verified. |
| `test_deposit_error` | `test_deposit_negative_amount_raises_value_error` | Specifies the condition (-10) and expected outcome (`ValueError`). |
| `test_withdraw_1` | `test_withdraw_more_than_balance_raises_value_error` | Clarifies the guard condition against overdrafts. |
| `test_withdraw_2` | `test_withdraw_exact_balance_leaves_zero` | Clearly defines the boundary condition ($100 - $100 = $0). |

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab02-EffectiveTestCases/descriptive-test-names -v
```

### From within this Directory:
```bash
python -m pytest test_named.py -v
```

### Expected Output:
Notice how the test runner output reads like an English specification:
```text
test_named.py::test_deposit_positive_amount_increases_balance PASSED
test_named.py::test_deposit_negative_amount_raises_value_error PASSED
test_named.py::test_withdraw_more_than_balance_raises_value_error PASSED
test_named.py::test_withdraw_exact_balance_leaves_zero PASSED
```
