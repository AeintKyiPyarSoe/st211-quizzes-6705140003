# Configuration with pytest.ini & Strict Marker Validation

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab03-Assertions-Organizations](../README.md)

---

## Overview

In test automation, configuration files define the runtime parameters, directory search paths, command-line arguments, and custom metadata tags across a project.

This directory illustrates how to configure Pytest using `pytest.ini` and demonstrates the crucial distinction between default marker warnings and enforced validation using `--strict-markers`.

---

## Files in this Directory

| File | Description |
|---|---|
| [`pytest.ini`](./pytest.ini) | Primary configuration file declaring registered custom markers. |
| [`test_strict.py`](./test_strict.py) | Test containing an unregistered marker (`@pytest.mark.nonexistent_marker`) to demonstrate strict validation. |
| [`shopping.py`](./shopping.py) | Domain model for `ShoppingCart`. |
| [`test_shopping.py`](./test_shopping.py) | Class-based test suite verifying `ShoppingCart` operations. |

---

## Technical Details

### 1. Pytest Configuration File (`pytest.ini`)

The `pytest.ini` file sits at the project or module root and sets global options for the test engine:

```ini
[pytest]
# Here we register the markers
markers =
    smoke: critical path tests
    slow: tests that take a long time
    regression: tests for previously fixed bugs
```

Registering markers serves two vital purposes:
1. **Self-Documentation:** Clearly outlines all categories and tags used across test suites.
2. **Typo Prevention:** Allows Pytest to detect misspelled markers (e.g., `@pytest.mark.smok` instead of `smoke`).

---

### 2. Default Warning vs. Strict Marker Enforcement (`test_strict.py`)

```python
import pytest

@pytest.mark.nonexistent_marker
def test_bad_marker():
    assert True
```

When Pytest encounters `@pytest.mark.nonexistent_marker`, it cannot find it in the registered `markers` list inside `pytest.ini`.

#### Scenario A: Default Execution (Warning)
When run normally without strict enforcement:
```bash
python -m pytest Lab03-Assertions-Organizations/configuration-with-pytest.ini/test_strict.py
```
Pytest executes the test successfully, but issues a `PytestUnknownMarkWarning`:
```text
PytestUnknownMarkWarning: Unknown pytest.mark.nonexistent_marker - is this a typo? 
You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
```

#### Scenario B: Strict Enforcement (`--strict-markers`)
When run with the `--strict-markers` flag (or when `addopts = --strict-markers` is set in `pytest.ini`):
```bash
python -m pytest Lab03-Assertions-Organizations/configuration-with-pytest.ini/test_strict.py --strict-markers
```
Pytest immediately halts collection and raises a fatal error:
```text
=================================== ERRORS ====================================
_______________________ ERROR collecting test_strict.py _______________________
'nonexistent_marker' not found in `markers` configuration option
=========================== short test summary info ===========================
ERROR test_strict.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
============================== 1 error in 0.25s ===============================
```

> [!IMPORTANT]
> In production CI/CD pipelines, always enable `--strict-markers` to guarantee that tests intended to be included under specific marker filters (like `smoke` or `regression`) are not silently bypassed due to typographical errors.

---

### 3. Domain Model & Tests (`shopping.py`, `test_shopping.py`)

Contains standard unit tests organized inside the `TestShoppingCart` class:
- `test_new_cart_is_empty`
- `test_new_cart_total_is_zero`
- `test_add_item_increases_count`
- `test_total_sum_prices`

These tests verify that standard class-based tests run harmoniously under configured environments.

---

## How to Run the Tests

### From the Repository Root:

```bash
# Run all tests in this folder
python -m pytest Lab03-Assertions-Organizations/configuration-with-pytest.ini -v

# Run test_strict.py and observe the warning
python -m pytest Lab03-Assertions-Organizations/configuration-with-pytest.ini/test_strict.py -v

# Run with strict markers to enforce validation
python -m pytest Lab03-Assertions-Organizations/configuration-with-pytest.ini/test_strict.py --strict-markers
```

### From within this Directory:

```bash
# Run the shopping cart tests
python -m pytest test_shopping.py -v

# Run strict marker check
python -m pytest test_strict.py --strict-markers
```
