# Clear AAA Test Case

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab02-EffectiveTestCases](../README.md)

---

## Overview

This subfolder demonstrates the refactored, best-practice solution to the "Fat Test" anti-pattern shown in [`bad-test/`](../bad-test/README.md). Here, a unit test focuses strictly on a **single behavior** using the **Arrange-Act-Assert (AAA)** pattern.

---

## Files in this Directory

| File | Description |
|---|---|
| [`bank.py`](./bank.py) | Clean `BankAccount` domain implementation supporting `deposit(amount)` and `withdraw(amount)` with validation. |
| [`test_bank.py`](./test_bank.py) | Refactored, single-responsibility unit test adhering to the AAA structure. |

---

## Best Practice Demonstration

### Refactored Test (`test_bank.py`)
```python
from bank import BankAccount

def test_deposit_increases_balance():
    # Arrange: initialize bank account with a starting balance
    account = BankAccount(balance=100)
    
    # Act: execute the single operation being tested
    new_balance = account.deposit(50)
    
    # Assert: verify the exact outcome of that single action
    assert new_balance == 150
```

### Why this Approach is Superior:
1. **Single Responsibility:** The test focuses solely on verifying that calling `deposit()` on an account increases its balance by the deposited amount.
2. **Immediate Diagnostics:** If this test fails, there is no ambiguity—the defect is unquestionably located inside `deposit()` or balance calculation.
3. **Self-Documenting:** The test function name `test_deposit_increases_balance` clearly explains the requirement without needing comments.
4. **Resilience:** Unrelated logic or future changes to `withdraw()` will never cause this test to fail or produce false negatives.

---

## Comparison: Anti-Pattern vs. Best Practice

| Metric | Bad Test (`test_bad_example.py`) | Clear AAA Test (`test_bank.py`) |
|---|---|---|
| **Operations Performed** | 3 (`deposit`, `withdraw`, `deposit`) | 1 (`deposit`) |
| **Failure Diagnosis** | Ambiguous, requires stepping through | Immediate and localized |
| **Interdependence** | High (steps depend on previous mutations) | Zero (isolated single action) |
| **Naming Quality** | Vague (`test_everything_at_once`) | Descriptive (`test_deposit_increases_balance`) |

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab02-EffectiveTestCases/clear-AAA-test -v
```

### From within this Directory:
```bash
python -m pytest test_bank.py -v
```

### Expected Output:
```text
test_bank.py::test_deposit_increases_balance PASSED
```
