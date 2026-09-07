# Week 3: Unit Testing Best Practices & Boundary Value Analysis

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  

---

## Overview

This repository contains the exercises and test suites for **Week 3** of the Automated Software Testing course. The primary focus of this week's lab is to learn and demonstrate core unit testing principles in Python using `pytest`, including:

- **Isolated Unit Testing vs. Comprehensive Test Functions**
- **Boundary Value Analysis (BVA) & Equivalence Partitioning**
- **Test Independence vs. Test Dependency (Shared State Anti-Pattern)**
- **Exception Testing (`pytest.raises`)**

---

## Exercise Details & Concepts

### 1. Bank Account Operations (`bank.py` & `test_bank.py`)
- **Implementation (`bank.py`):**
  - Defines the `BankAccount` class with `deposit(amount)` and `withdraw(amount)` methods.
  - Enforces domain rules: non-positive deposits raise `ValueError("Deposit amount must be positive.")`, and withdrawals exceeding the balance raise `ValueError("Insufficient funds.")`.
- **Testing Approach (`test_bank.py`):**
  - Demonstrates focused unit tests (`test_deposit_increases_balance`, `test_withdraw_decreases_balance`) testing one single action/behavior at a time.
  - Identifies the test smell in `test_everything_at_once`, where multiple actions are chained together in a single test case, coupling the test outcome to multiple sequential operations.

### 2. Grade Classification & Boundary Testing (`grades.py` & `test_grades.py`)
- **Implementation (`grades.py`):**
  - Defines `letter_grade(score)` returning `"A"` (>= 80), `"B"` (>= 70), `"C"` (>= 60), or `"F"` (< 60).
  - Validates score input range (0–100) and raises a `ValueError` for invalid scores.
- **Testing Approach (`test_grades.py`):**
  - **Boundary Value Analysis (BVA):** Tests critical edge thresholds rather than arbitrary middle values:
    - Upper grade boundary: `80` ("A") vs. `79` ("B")
    - Pass/Fail threshold: `60` ("C", lowest pass) vs. `59` ("F", just failed)
    - Valid domain limits: `0` (minimum valid) and `100` (maximum valid)
  - **Negative Testing:** Verifies exception raising for out-of-bound inputs (`letter_grade(-1)`) using `pytest.raises(ValueError)`.

### 3. Test Independence vs. Shared State (`test_dependent.py` vs. `test_independent.py`)
- **Anti-Pattern (`test_dependent.py`):**
  - Uses a shared module-level instance (`shared_account = BankAccount(100)`).
  - The outcome of `test_b_withdraw` depends on `test_a_deposit` having already run, making tests fragile and order-dependent.
- **Best Practice (`test_independent.py`):**
  - Each test instantiates its own clean instance of `BankAccount(100)`.
  - Ensures tests are fully isolated, reproducible, and executable in any arbitrary order or in parallel.

---

## Project Structure

```text
Week3Exercise/
├── bank.py               # BankAccount class implementation
├── test_bank.py          # Unit tests for bank operations
├── grades.py             # Grade calculation logic
├── test_grades.py        # Boundary value analysis & exception tests
├── test_dependent.py     # Demonstration of dependent tests (anti-pattern)
├── test_independent.py   # Demonstration of independent tests (best practice)
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

Run a specific test suite:
```bash
# Test bank account logic
python -m pytest test_bank.py -v

# Test grade boundaries
python -m pytest test_grades.py -v

# Run independent tests
python -m pytest test_independent.py -v
```

### Test Suite Execution Output
```text
============================= test session starts =============================
collected 12 items

test_bank.py::test_deposit_increases_balance PASSED                      [  8%]
test_bank.py::test_withdraw_decreases_balance PASSED                     [ 16%]
test_bank.py::test_everything_at_once PASSED                             [ 25%]
test_dependent.py::test_a_deposit PASSED                                 [ 33%]
test_dependent.py::test_b_withdraw PASSED                                [ 41%]
test_grades.py::test_boundary_a_grade PASSED                             [ 50%]
test_grades.py::test_boundary_pass_fail PASSED                           [ 58%]
test_grades.py::test_minmal_valid PASSED                                 [ 66%]
test_grades.py::test_maximum_valid PASSED                                [ 75%]
test_grades.py::test_below_minimal_invalid PASSED                        [ 83%]
test_independent.py::test_deposit_independent PASSED                     [ 91%]
test_independent.py::test_withdraw_independent PASSED                    [100%]

============================= 12 passed in 0.14s ==============================
```
