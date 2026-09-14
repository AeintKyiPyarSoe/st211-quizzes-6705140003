# Week 4: Advanced Assertions, Test Organization, & Validation Testing

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  

---

## Overview

This repository contains the exercises and test suites for **Week 4** of the Automated Software Testing course. The primary focus of this week's lab is mastering advanced assertion techniques in `pytest`, structuring test suites using test classes, and applying positive and negative testing methodologies.

The exercises are structured into three distinct modules:
1. **Assertion Testing (`assertion-test/`):** Handling floating-point arithmetic precision issues with `pytest.approx` and asserting equality across Python collections (lists, dictionaries, sets).
2. **Organized Tests (`organized-tests/`):** Structuring unit tests inside test classes (`TestShoppingCart`) to maintain clean, scalable, and readable test suites.
3. **Positive & Negative Testing (`postive-negative/`):** Testing both the "happy path" (valid inputs accepted) and error handling / edge cases (invalid types and out-of-range inputs raising exceptions).

---

## Exercise Details & Concepts

### 1. Assertion Testing (`assertion-test/`)

#### A. Floating Point Precision (`test_floats.py`)
- **Concept:** Computers use binary floating-point representation (IEEE 754), which cannot represent numbers like `0.1` and `0.2` with exact precision. As a result, `0.1 + 0.2` evaluates to `0.30000000000000004` rather than exactly `0.3`.
- **Testing Approach:**
  - Standard equality `assert 0.1 + 0.2 == 0.3` fails in Python.
  - `pytest.approx(0.3)` provides tolerance-based float comparison, ensuring assertions evaluate based on acceptable numerical precision.
  - Demonstrated via `test_float_precision` and `test_float_without_approx_fails`.

#### B. Collection & Data Structure Equality (`test_list_equality.py`)
- **Sequential Equality:** `test_list_equality` asserts that two lists contain identical elements in the exact same sequence.
- **Order-Independent Comparison:** `test_list_contents` tests lists regardless of initial element ordering using `sorted()`.
- **Dictionary Assertions:** `test_dict_equality` tests key-value equivalence between dictionaries independent of insertion key order.
- **Set Operations:** `test_set_operations` validates set mathematics including intersection (`&`), union (`|`), and difference (`-`).

---

### 2. Organized Tests (`organized-tests/`)

#### A. Implementation (`shopping.py`)
- Defines the `ShoppingCart` class with methods:
  - `add(name, price)`: Adds item dictionary to cart.
  - `total()`: Computes total price across all items.
  - `count()` : Returns current item count in the cart.

#### B. Test Class Structure (`test_shopping.py`)
- **Concept:** Grouping related tests inside a class (`TestShoppingCart`) improves readability, namespaces test cases, and simplifies running specific test subsets.
- **Rules Followed:**
  - Class name starts with `Test` (e.g., `TestShoppingCart`).
  - No `__init__` constructor used within test classes.
  - Each test method starts with `test_` and takes `self`.
- **Test Scenarios Covered:**
  - `test_new_cart_is_empty`: Validates newly initialized cart count is 0.
  - `test_new_cart_total_is_zero`: Validates newly initialized cart total is 0.
  - `test_add_item_increases_count`: Validates adding items increments item count.
  - `test_total_sum_prices`: Validates total reflects the accumulated item prices.

---

### 3. Positive & Negative Testing (`postive-negative/`)

#### A. Validator Implementation (`validators.py`)
- `validate_email(email)`: Uses regular expressions (`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`) to validate email formatting. Raises `ValueError` for invalid email formats.
- `validate_age(age)`: Enforces that `age` is an integer (`isinstance(age, int)`) and lies within the valid human age domain `0 <= age <= 150`. Raises `TypeError` for non-integer types and `ValueError` for out-of-range values.

#### B. Positive Tests (`test_positive.py`)
- Tests the **Happy Path** where inputs conform to business specifications:
  - Valid institutional email (`student@siam.edu`).
  - Valid email with subdomains (`user@mail.example.com`).
  - Standard valid age (`25`).
  - Boundary valid ages (`0` and `150`).

#### C. Negative Tests (`test_negative.py`)
- Tests **Error Handling & Failure Modes** using `pytest.raises`:
  - Missing `@` symbol (`invalidemail.com`) raises `ValueError`.
  - Incomplete domain (`user@.com`) raises `ValueError`.
  - Negative age (`-5`) raises `ValueError`.
  - Invalid age data type (`"twenty-five"`) raises `TypeError`.

---

## Project Structure

```text
Week4Exercise/
├── assertion-test/
│   ├── test_floats.py           # Float precision & approx tests
│   ├── test_list_equality.py    # List, dict, and set equality assertions
│   └── README.md                # Module documentation
├── organized-tests/
│   ├── shopping.py              # ShoppingCart model implementation
│   ├── test_shopping.py         # TestShoppingCart test class suite
│   └── README.md                # Module documentation
├── postive-negative/
│   ├── validators.py            # Email and age validation logic
│   ├── test_positive.py         # Positive / happy-path test cases
│   ├── test_negative.py         # Negative / exception test cases
│   └── README.md                # Module documentation
└── README.md                    # Main Week 4 documentation
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

### Running All Week 4 Tests

From the `Week4Exercise/` directory:
```bash
python -m pytest -v
```

Or from the project root directory:
```bash
python -m pytest Week4Exercise -v
```

### Running Specific Test Modules

```bash
# 1. Run assertion tests
python -m pytest Week4Exercise/assertion-test -v

# 2. Run organized shopping cart tests
python -m pytest Week4Exercise/organized-tests -v

# 3. Run positive and negative validation tests
python -m pytest Week4Exercise/postive-negative -v
```

---

### Test Suite Execution Output

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\Siam BSc IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003\Week4Exercise
plugins: anyio-4.14.2, flet-0.86.5
collected 18 items

assertion-test/test_floats.py::test_float_precision PASSED               [  5%]
assertion-test/test_floats.py::test_float_without_approx_fails PASSED    [ 11%]
assertion-test/test_list_equality.py::test_list_equality PASSED          [ 16%]
assertion-test/test_list_equality.py::test_list_contents PASSED          [ 22%]
assertion-test/test_list_equality.py::test_dict_equality PASSED          [ 27%]
assertion-test/test_list_equality.py::test_set_operations PASSED         [ 33%]
organized-tests/test_shopping.py::TestShoppingCart::test_new_cart_is_empty PASSED [ 38%]
organized-tests/test_shopping.py::TestShoppingCart::test_new_cart_total_is_zero PASSED [ 44%]
organized-tests/test_shopping.py::TestShoppingCart::test_add_item_increases_count PASSED [ 50%]
organized-tests/test_shopping.py::TestShoppingCart::test_total_sum_prices PASSED [ 55%]
postive-negative/test_negative.py::test_email_without_at_rejected PASSED [ 61%]
postive-negative/test_negative.py::test_email_without_domain_rejected PASSED [ 66%]
postive-negative/test_negative.py::test_negative_age_rejected PASSED     [ 72%]
postive-negative/test_negative.py::test_age_as_string_rejected PASSED    [ 77%]
postive-negative/test_positive.py::test_valid_email_accepted PASSED      [ 83%]
postive-negative/test_positive.py::test_valid_email_with_subdomain PASSED [ 88%]
postive-negative/test_positive.py::test_valid_age_accepted PASSED        [ 94%]
postive-negative/test_positive.py::test_boundary_ages_accepted PASSED    [100%]

============================= 18 passed in 0.12s ==============================
```
