# The "Fat Test" Anti-Pattern

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab02-EffectiveTestCases](../README.md)

---

## Overview

This subfolder illustrates the **"Fat Test"** (or chained operations) anti-pattern in automated unit testing. A fat test attempts to test too many operations and state transitions within a single test function, violating the Single Responsibility Principle.

---

## Files in this Directory

| File | Description |
|---|---|
| [`bank.py`](./bank.py) | `BankAccount` domain model with balance initialization, deposit, and withdrawal methods with basic input validations. |
| [`test_bad_example.py`](./test_bad_example.py) | Demonstration of the "Fat Test" anti-pattern chaining multiple sequential operations. |

---

## Code Analysis: The Anti-Pattern

```python
# test_bad_example.py
from bank import BankAccount

def test_everything_at_once():
    account = BankAccount(100)
    account.deposit(50)
    account.withdraw(30)
    account.deposit(10)
    assert account.balance == 130
```

### Why is this an Anti-Pattern?

1. **Obscured Root Cause:**
   - If the assertion fails (e.g., `account.balance == 120`), it is impossible to know at a glance whether the first `deposit(50)`, the subsequent `withdraw(30)`, or the second `deposit(10)` was defective without adding debugging logs or stepping through with a debugger.
2. **Cascading Failure:**
   - If the first operation (`deposit(50)`) raises an unexpected error or fails, the subsequent operations (`withdraw` and second `deposit`) are never executed. Defects in those operations remain hidden until the earlier one is resolved.
3. **Violates Single Responsibility Principle (SRP):**
   - Each unit test function should test exactly one behavior, under one specific condition, and assert one distinct outcome.
4. **Poor Documentation:**
   - The test name `test_everything_at_once` conveys nothing about the business requirements or expected behavior of the `BankAccount` class.

> [!TIP]
> See [`Lab02-EffectiveTestCases/clear-AAA-test/`](../clear-AAA-test/README.md) for the refactored, single-responsibility version of this test.

---

## How to Run

### Run the Test Suite:
```bash
python -m pytest Lab02-EffectiveTestCases/bad-test -v
```

### Run the Standalone Bank Script:
```bash
python Lab02-EffectiveTestCases/bad-test/bank.py
```

### Expected Test Output:
```text
test_bad_example.py::test_everything_at_once PASSED
```
