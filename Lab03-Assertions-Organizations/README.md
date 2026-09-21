# Lab 03: Advanced Assertions, Organization & Configuration

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

This directory contains the laboratory exercises for **Lab 03: Advanced Assertions, Organization & Pytest Configuration**. The lab covers advanced assertion methods, structured test design using classes, custom metadata markers, selective test execution, skip/xfail handling, and framework configuration via `pytest.ini`.

### Key Learning Objectives
1. **Specialized Assertions:** Handling IEEE 754 floating-point inaccuracies using `pytest.approx()` and validating complex collections (lists, dictionaries, sets).
2. **Class-Based Test Organization:** Structuring related test cases into `Test*` classes for encapsulation, clean reporting, and class-level fixture scoping.
3. **Custom Test Markers:** Tagging tests with metadata (`@pytest.mark.<name>`) and filtering test runs with `-m` expressions.
4. **Skipping & Expected Failures:** Gracefully managing incomplete features, environment-specific requirements (`@pytest.mark.skip`, `@pytest.mark.skipif`), and tracking known bugs (`@pytest.mark.xfail`).
5. **Configuration Management:** Using `pytest.ini` to set runner options, define discovery roots, and enforce marker safety with `--strict-markers`.

---

## Directory Structure

```text
Lab03-Assertions-Organizations/
├── assertion-types/                         # Floating-point approx & deep collection assertions
│   ├── test_collections.py                 # List, dictionary, and set operations
│   ├── test_floats.py                      # IEEE 754 precision & pytest.approx()
│   └── README.md                           # Detailed assertion types documentation
│
├── configuration-with-pytest.ini/          # Global configuration & strict marker enforcement
│   ├── pytest.ini                          # Registered markers definition
│   ├── shopping.py                         # ShoppingCart domain implementation
│   ├── test_shopping.py                    # Class-based shopping test suite
│   ├── test_strict.py                      # Unregistered marker strict validation demo
│   └── README.md                           # Configuration guide
│
├── custom-markers/                          # Test categorization and selective execution
│   ├── pytest.ini                          # Marker registration (smoke, slow, regression)
│   ├── test_markers.py                     # Tests tagged with custom marks
│   └── README.md                           # Custom markers guide
│
├── organizing-tests-in-classes/            # Structuring test suites inside Python classes
│   ├── shopping.py                         # ShoppingCart model
│   ├── test_shopping.py                    # TestShoppingCart class suite
│   └── README.md                           # Class-based tests documentation
│
├── skipping-and-expected-failures/         # Skip conditions and known bug handling
│   ├── pytest.ini                          # Discovery rules & short traceback configuration
│   ├── test_conditional.py                # OS/path conditional skipping (skipif)
│   ├── test_skips.py                       # Unconditional and Python-version skipping
│   ├── test_xfail.py                       # Expected failure (XFAIL) and unexpected pass (XPASS)
│   └── README.md                           # Skipping & xfail guide
│
└── README.md                               # Lab 03 comprehensive documentation
```

---

## Submodule Summaries

| Submodule | Directory | Key Topics Covered | Guide |
|---|---|---|:---:|
| **1. Assertion Types** | [`assertion-types/`](./assertion-types/) | IEEE 754 float precision, `pytest.approx()`, list equality, dictionary equivalence, set operations | [View README](./assertion-types/README.md) |
| **2. Test Organization in Classes** | [`organizing-tests-in-classes/`](./organizing-tests-in-classes/) | `Test*` class conventions, encapsulation, hierarchical reporting, no `__init__` rule | [View README](./organizing-tests-in-classes/README.md) |
| **3. Custom Markers** | [`custom-markers/`](./custom-markers/) | `@pytest.mark.<name>`, marker registration in `pytest.ini`, `-m` boolean filters | [View README](./custom-markers/README.md) |
| **4. Skipping & Expected Failures** | [`skipping-and-expected-failures/`](./skipping-and-expected-failures/) | `@pytest.mark.skip`, `@pytest.mark.skipif`, `@pytest.mark.xfail`, `XFAIL` vs `XPASS` | [View README](./skipping-and-expected-failures/README.md) |
| **5. Pytest Configuration** | [`configuration-with-pytest.ini/`](./configuration-with-pytest.ini/) | `pytest.ini` structure, `--strict-markers`, preventing marker typos | [View README](./configuration-with-pytest.ini/README.md) |

---

## Technical Details by Module

### 1. Assertion Types (`assertion-types/`)

#### A. Floating-Point Precision (`test_floats.py`)
Because binary floating-point representation (IEEE 754) cannot represent certain base-10 fractions exactly, `0.1 + 0.2` equals `0.30000000000000004` rather than `0.3`.
- Exact equality checks (`0.1 + 0.2 == 0.3`) fail in Python.
- `pytest.approx(0.3)` solves this by validating values within a default relative tolerance ($1 \times 10^{-6}$):
  ```python
  from pytest import approx

  def test_float_precision():
      assert 0.1 + 0.2 == approx(0.3)
  ```

#### B. Collection Assertions (`test_collections.py`)
Pytest performs deep structural diffing across complex data structures:
- **Lists:** Evaluates element equivalence and strict ordering (`[1, 2, 3] == [1, 2, 3]`). Use `sorted(result)` for order-independent assertions.
- **Dictionaries:** Compares key-value pairs regardless of key order (`{"a": 1, "b": 2} == {"b": 2, "a": 1}`).
- **Sets:** Asserts set intersection (`&`), union (`|`), and difference (`-`).

---

### 2. Organizing Tests in Classes (`organizing-tests-in-classes/`)

Grouping test methods within classes provides clear namespacing and structured test reports:

```python
from shopping import ShoppingCart

class TestShoppingCart:
    def test_new_cart_is_empty(self):
        cart = ShoppingCart()
        assert cart.count() == 0

    def test_add_item_increases_count(self):
        cart = ShoppingCart()
        cart.add("Book", 20)
        assert cart.count() == 1
```

**Conventions:**
1. Class names must start with `Test` (PascalCase).
2. Never implement an `__init__()` constructor in test classes.
3. Test methods must start with `test_` and accept `self`.

---

### 3. Custom Test Markers (`custom-markers/`)

Markers allow tagging test functions for selective execution across different environments or testing stages.

#### Registration (`pytest.ini`):
```ini
[pytest]
markers =
    smoke: critical path tests
    slow: tests that take a long time
    regression: tests for previously fixed bugs
```

#### Application (`test_markers.py`):
```python
import pytest

@pytest.mark.smoke
def test_critical_login():
    assert True

@pytest.mark.slow
def test_full_report_generation():
    assert True
```

#### Filtering via CLI:
- Run only smoke tests: `pytest -m smoke`
- Exclude slow tests: `pytest -m "not slow"`
- Combine markers: `pytest -m "smoke or regression"`

---

### 4. Skipping and Expected Failures (`skipping-and-expected-failures/`)

Manages test scenarios that cannot or should not pass immediately:

- **Unconditional Skip (`@pytest.mark.skip`):** Bypasses execution of pending or unfinished features:
  ```python
  @pytest.mark.skip(reason="Feature not implemented yet")
  def test_future_feature():
      assert False
  ```
- **Conditional Skip (`@pytest.mark.skipif`):** Bypasses tests based on environment checks:
  ```python
  @pytest.mark.skipif(sys.version_info < (3, 8), reason="Require Python 3.8+")
  def test_needs_modern_python():
      assert True
  ```
- **Expected Failure (`@pytest.mark.xfail`):** Tracks known bugs without breaking CI:
  ```python
  @pytest.mark.xfail(reason="Known bug #123, fix pending")
  def test_known_broken_feature():
      assert 1 == 2  # Reported as XFAIL (suite passes)

  @pytest.mark.xfail(reason="Might pass sometimes")
  def test_actually_works_now():
      assert 1 == 1  # Reported as XPASS (unexpected pass)
  ```

---

### 5. Configuration with `pytest.ini` (`configuration-with-pytest.ini/`)

Centralizes project-wide settings and prevents subtle errors:
- **`markers` list:** Declares allowed markers.
- **`--strict-markers`:** When enabled, using an unregistered marker (e.g., `@pytest.mark.nonexistent_marker` in `test_strict.py`) raises an immediate collection error instead of an easily overlooked warning.

---

## How to Run Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running Individual Submodules

```bash
# 1. Assertion Types
python -m pytest Lab03-Assertions-Organizations/assertion-types -v

# 2. Organizing Tests in Classes
python -m pytest Lab03-Assertions-Organizations/organizing-tests-in-classes -v

# 3. Custom Markers (all tests)
python -m pytest Lab03-Assertions-Organizations/custom-markers -v

# 3a. Custom Markers (smoke tests only)
python -m pytest Lab03-Assertions-Organizations/custom-markers -m smoke -v

# 4. Skipping and Expected Failures (with summary reasons)
python -m pytest Lab03-Assertions-Organizations/skipping-and-expected-failures -v -rsxX

# 5. Configuration with pytest.ini
python -m pytest Lab03-Assertions-Organizations/configuration-with-pytest.ini -v

# 5a. Strict marker check (demonstrates error collection)
python -m pytest Lab03-Assertions-Organizations/configuration-with-pytest.ini/test_strict.py --strict-markers
```
