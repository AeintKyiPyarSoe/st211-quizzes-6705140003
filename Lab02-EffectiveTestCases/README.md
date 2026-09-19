# Lab 02: Writing Effective Test Cases & Test Design Techniques

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

This directory contains the laboratory exercises for **Lab 02: Writing Effective Test Cases**. The primary focus of this lab is understanding the qualities of robust, maintainable, and deterministic test suites. It explores key unit testing principles, anti-patterns to avoid, and essential test design techniques:

- **Single Responsibility in Tests vs. The "Fat Test" Anti-Pattern**
- **Test Independence vs. Shared Mutable State**
- **Intention-Revealing Test Naming Conventions** (`test_<action>_<condition>_<expected_result>`)
- **Boundary Value Analysis (BVA) & Edge Case Testing**
- **Positive vs. Negative Testing Methodologies**

---

## Directory Structure

```text
Lab02-EffectiveTestCases/
├── bad-test/
│   ├── bank.py                          # BankAccount domain model
│   └── test_bad_example.py              # Demonstration of chained / "fat" test anti-pattern
├── clear-AAA-test/
│   ├── bank.py                          # BankAccount domain model
│   └── test_bank.py                     # Clean, single-responsibility test following AAA
├── dependent-independent-tests/
│   ├── bank.py                          # BankAccount domain model
│   ├── test_dependent.py                # Anti-pattern: tests sharing mutable state & order dependent
│   └── test_independent.py              # Best practice: isolated tests with fresh instances
├── descriptive-test-names/
│   ├── bank.py                          # BankAccount domain model
│   └── test_named.py                    # Living documentation with descriptive test names
├── edge-cases-and-boundary-values/
│   ├── grades.py                        # Grade classifier with range validation
│   └── test_grades.py                   # Boundary value analysis & negative out-of-range testing
├── postive-negative-testing/
│   ├── validators.py                    # Email regex validator & age domain validator
│   ├── test_positive.py                 # Happy-path test cases (valid formats and boundary ages)
│   └── test_negative.py                 # Error handling tests (invalid emails, negative/string ages)
└── README.md                            # Lab 02 documentation
```

---

## Exercise Details & Core Concepts

### 1. The "Fat Test" Anti-Pattern vs. Clear AAA Testing (`bad-test/` & `clear-AAA-test/`)

#### The Anti-Pattern (`bad-test/test_bad_example.py`)
```python
def test_everything_at_once():
    account = BankAccount(100)
    account.deposit(50)
    account.withdraw(30)
    account.deposit(10)
    assert account.balance == 130
```
- **Why this is problematic:**
  - **Obscured Failure Causes:** If the test fails, it is unclear whether `deposit()` or `withdraw()` caused the defect without debugging.
  - **Cascading Interruption:** If the first action fails, subsequent operations are never executed.
  - **Violates Single Responsibility:** A test should verify one specific behavior under one specific condition.

#### The Best Practice (`clear-AAA-test/test_bank.py`)
```python
def test_deposit_increases_balance():
    account = BankAccount(balance=100)
    new_balance = account.deposit(50)
    assert new_balance == 150
```
- Focuses strictly on a single state transition.
- Explicit, predictable, and easy to diagnose if broken.

---

### 2. Test Independence vs. Shared State (`dependent-independent-tests/`)

#### The Anti-Pattern (`test_dependent.py`)
- Defines a global `shared_account = BankAccount(100)`.
- `test_a_deposit` modifies `shared_account` balance to `150`.
- `test_b_withdraw` depends on `test_a_deposit` running first, expecting balance `120`.
- **Dangers:**
  - Tests fail if executed out of alphabetical order, randomized, or in isolation.
  - Cannot run tests safely in parallel.
  - Failure in test A causes false failures in test B.

#### The Best Practice (`test_independent.py`)
- Each test creates its own independent `BankAccount(100)` instance.
- Tests are completely isolated, idempotent, and can run in any sequence.

---

### 3. Descriptive Test Naming (`descriptive-test-names/`)
Test names serve as executable specifications and living documentation. When a test fails in CI/CD, the test name alone should indicate what went wrong.

- **Naming Pattern:** `test_<action>_<condition>_<expected_result>`
- **Examples in `test_named.py`:**
  - `test_deposit_positive_amount_increases_balance`
  - `test_deposit_negative_amount_raises_value_error`
  - `test_withdraw_more_than_balance_raises_value_error`
  - `test_withdraw_exact_balance_leaves_zero`

---

### 4. Boundary Value Analysis (BVA) (`edge-cases-and-boundary-values/`)
Defects cluster predominantly at the boundaries between equivalence partitions rather than in interior ranges.

- **System Under Test (`grades.py`):**
  - Score range: `0 <= score <= 100` (outside raises `ValueError`)
  - `80 <= score <= 100` $\rightarrow$ `"A"`
  - `70 <= score < 80` $\rightarrow$ `"B"`
  - `60 <= score < 70` $\rightarrow$ `"C"`
  - `0 <= score < 60` $\rightarrow$ `"F"`

- **Boundary Values Tested in `test_grades.py`:**
  - **A/B Threshold:** Tests `80` ("A") and `79` ("B") rather than arbitrary values like `85`.
  - **Pass/Fail Threshold:** Tests `60` ("C", minimum pass) and `59` ("F", maximum fail).
  - **Valid Domain Extremes:** Tests `0` (minimum valid) and `100` (maximum valid).
  - **Invalid Extreme:** Tests `-1` to ensure `ValueError` is raised.

---

### 5. Positive and Negative Testing (`postive-negative-testing/`)
A comprehensive test suite verifies both valid behavior and robust error handling.

- **Domain Model (`validators.py`):**
  - `validate_email(email)`: Validates format against regex pattern.
  - `validate_age(age)`: Checks integer type and range between `0` and `150`.

- **Positive Tests (`test_positive.py`):**
  - Standard valid email (`student@siam.edu`)
  - Subdomain email (`user@mail.example.com`)
  - Interior age (`25`)
  - Boundary ages (`0` and `150`)

- **Negative Tests (`test_negative.py`):**
  - Missing `@` symbol (`invalidemail.com` $\rightarrow$ `ValueError`)
  - Missing domain (`user@.com` $\rightarrow$ `ValueError`)
  - Negative age (`-5` $\rightarrow$ `ValueError`)
  - Invalid type (`"twenty-five"` $\rightarrow$ `TypeError`)

---

## Summary of Testing Principles

| Principle | Anti-Pattern | Best Practice Applied |
|---|---|---|
| **Scope of Test** | Chained operations (`test_everything_at_once`) | Single behavior per test function |
| **State Isolation** | Shared global objects (`shared_account`) | Fresh instance created per test |
| **Naming Clarity** | Vague names (`test1`, `test_bank`) | Descriptive names (`test_withdraw_exact_balance_leaves_zero`) |
| **Input Selection** | Testing only arbitrary middle values | Boundary Value Analysis (edge thresholds) |
| **Validation Paths** | Happy path only | Positive and negative testing with `pytest.raises` |

---

## How to Run Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running All Lab 02 Tests
```bash
# Run all Lab 02 tests with verbose output
python -m pytest Lab02-EffectiveTestCases -v
```

### Running Specific Modules
```bash
# Run clear AAA tests
python -m pytest Lab02-EffectiveTestCases/clear-AAA-test -v

# Run independent tests
python -m pytest Lab02-EffectiveTestCases/dependent-independent-tests/test_independent.py -v

# Run descriptive named tests
python -m pytest Lab02-EffectiveTestCases/descriptive-test-names -v

# Run boundary value analysis tests
python -m pytest Lab02-EffectiveTestCases/edge-cases-and-boundary-values -v

# Run positive and negative validation tests
python -m pytest Lab02-EffectiveTestCases/postive-negative-testing -v
```
