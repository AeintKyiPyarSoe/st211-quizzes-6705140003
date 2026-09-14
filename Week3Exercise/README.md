# Week 3: Unit Testing Best Practices & Boundary Value Analysis

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  

---

## Overview

This repository contains the exercises and test suites for **Week 3** of the Automated Software Testing course. The primary focus of this week's lab is to learn and demonstrate fundamental unit testing principles and test design techniques in Python using `pytest`, including:

- **Isolated Unit Testing vs. Comprehensive ("Fat") Test Functions** (Single Responsibility Principle in Tests)
- **Descriptive & Intention-Revealing Test Naming Conventions** (`test_<action>_<condition>_<expected_outcome>`)
- **Boundary Value Analysis (BVA) & Equivalence Partitioning** (Edge cases vs. interior values)
- **Test Independence vs. Shared State Anti-Patterns** (Avoiding test coupling and ordering dependencies)
- **Exception Testing & Negative Testing** (`pytest.raises(ValueError)`)

---

## Exercise Details & Concepts

### 1. Bank Account Operations (`bank.py` & `test_bank.py`)
- **Implementation (`bank.py`):**
  - Defines the `BankAccount` class with `__init__(self, balance=0)`, `deposit(amount)`, and `withdraw(amount)`.
  - **Business Rules & Invariants:**
    - Non-positive deposits (`amount <= 0`) are disallowed and raise `ValueError("Deposit amount must be positive.")`.
    - Withdrawals exceeding the balance (`amount > self.balance`) are disallowed and raise `ValueError("Insufficient funds.")`.
- **Testing Approach (`test_bank.py`):**
  - **Focused Unit Tests:** `test_deposit_positive_amount_increases_balance` and `test_withdraw_decreases_balance` test one isolated behavior per test function.
  - **The "Fat Test" Smell (`test_everything_at_once`):**
    - Chaining multiple deposits and withdrawals in one test function creates tight coupling: if an early step fails, subsequent behaviors are never tested, making defect localization difficult.
    - Demonstrates why each test should verify a single, discrete unit of functionality.

---

### 2. Descriptive Test Naming & Error Case Coverage (`test_named.py`)
- **Concept:** Test function names should act as executable specifications and living documentation. A well-named test immediately communicates what behavior was executed, under what conditions, and what the expected outcome is.
- **Naming Pattern:** `test_<unit_or_action>_<condition_or_input>_<expected_result>()`
- **Test Scenarios Covered:**
  | Test Function | Input / Action | Expected Outcome |
  |---|---|---|
  | `test_deposit_positive_amount_increases_balance` | Deposit `50` into account with balance `100` | Balance becomes `150` |
  | `test_deposit_negative_amount_raises_value_error` | Deposit `-10` into account with balance `100` | Raises `ValueError` ("Deposit amount must be positive.") |
  | `test_withdraw_more_than_balance_raises_value_error` | Withdraw `200` from account with balance `100` | Raises `ValueError` ("Insufficient funds.") |
  | `test_withdraw_exact_balance_leaves_zero` | Withdraw `100` from account with balance `100` | Balance becomes `0` (boundary condition) |

---

### 3. Grade Classification & Boundary Value Analysis (`grades.py` & `test_grades.py`)
- **Implementation (`grades.py`):**
  - Function `letter_grade(score)` maps a numeric score (0–100) to letter grades:
    - `80 <= score <= 100`: `"A"`
    - `70 <= score < 80`: `"B"`
    - `60 <= score < 70`: `"C"`
    - `0 <= score < 60`: `"F"`
  - Validates range constraint: scores `< 0` or `> 100` raise `ValueError("Score must be between 0-100.")`.
- **Boundary Value Analysis (BVA):**
  - Defects tend to cluster at boundaries between partitions rather than within interior values. BVA tests the exact edge values on either side of each boundary:
    - **A/B Grade Boundary:** Tests `80` ("A") and `79` ("B"). Rather than testing an arbitrary score like `85`, testing `80` and `79` directly verifies the `>= 80` condition.
    - **Pass/Fail Boundary:** Tests `60` ("C", minimum passing grade) and `59` ("F", maximum failing grade).
    - **Domain Extremes (Valid Boundaries):** Tests `0` (minimum valid score -> `"F"`) and `100` (maximum valid score -> `"A"`).
  - **Negative Testing:** Verifies that out-of-range inputs like `-1` raise `ValueError` using `pytest.raises(ValueError)`.

---

### 4. Test Independence vs. Shared State (`test_dependent.py` vs. `test_independent.py`)
- **The Shared State Anti-Pattern (`test_dependent.py`):**
  - Uses a single module-level instance: `shared_account = BankAccount(100)`.
  - `test_a_deposit` modifies `shared_account` to balance `150`.
  - `test_b_withdraw` withdraws `30` and asserts balance is `120`.
  - **Problems with this anti-pattern:**
    - **Order Dependency:** Tests only pass if executed alphabetically / in a specific order. If run in reverse or randomized order, `test_b_withdraw` fails.
    - **Cascading Failures:** If `test_a_deposit` fails, `test_b_withdraw` fails as a side effect even if the withdrawal logic is completely correct.
    - **Concurrency Issues:** Shared mutable state prevents running tests in parallel.
- **Independent Testing Best Practice (`test_independent.py`):**
  - Each test function instantiates its own fresh `BankAccount(100)` instance.
  - `test_deposit_independent` and `test_withdraw_independent` have zero shared state.
  - Guarantees test isolation, determinism, and arbitrary execution order.

---

## Project Structure

```text
Week3Exercise/
├── bank.py               # BankAccount class implementation
├── test_bank.py          # Unit tests for bank operations (single vs multi-action)
├── test_named.py         # Intention-revealing test naming & error handling
├── grades.py             # Grade calculation logic with range validation
├── test_grades.py        # Boundary value analysis (BVA) & negative tests
├── test_dependent.py     # Anti-pattern demonstration (shared state & order dependence)
├── test_independent.py   # Best practice demonstration (isolated tests)
└── README.md             # Documentation
```

---

## How to Run

### Prerequisites
- Python 3.8+
- `pytest`

If needed, install `pytest`:
```bash
pip install pytest
```

### Running Programs Directly
```bash
python bank.py
python grades.py
```

### Running Unit Tests

Run all tests in the `Week3Exercise` directory:
```bash
python -m pytest -v
```

Run specific test suites:
```bash
# Run descriptive named tests
python -m pytest test_named.py -v

# Run boundary value analysis tests
python -m pytest test_grades.py -v

# Run isolated independent tests
python -m pytest test_independent.py -v

# Run bank tests
python -m pytest test_bank.py -v
```

---

## Summary of Testing Principles Demonstrated

| Principle | Anti-Pattern | Best Practice Applied |
|---|---|---|
| **Test Naming** | Vague names (`test1`, `test_bank`) | Descriptive names (`test_deposit_positive_amount_increases_balance`) |
| **Test Scope** | Chaining multiple actions (`test_everything_at_once`) | Single assertion / single behavior per test |
| **Boundary Values** | Only testing interior values (`85`, `50`) | Testing exact boundary thresholds (`80`, `79`, `60`, `59`, `0`, `100`) |
| **State Management** | Shared mutable objects across tests (`shared_account`) | Fresh instance initialized in each test |
| **Error Handling** | Ignoring exceptions or unhandled failures | Asserting expected exceptions with `pytest.raises(ValueError)` |
