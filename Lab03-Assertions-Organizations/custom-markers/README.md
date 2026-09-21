# Custom Test Markers in Pytest

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab03-Assertions-Organizations](../README.md)

---

## Overview

This subfolder demonstrates the use of **custom test markers** in Pytest. Markers allow developers to categorize, tag, and selectively execute subsets of tests without modifying test code or moving files across directories.

By tagging tests with metadata, engineering teams can configure distinct execution pipelines—such as running fast sanity checks upon every commit, scheduling long-running tests during nightly builds, or validating critical regression scenarios before production deployments.

---

## Files in this Directory

| File | Description |
|---|---|
| [`pytest.ini`](./pytest.ini) | Configuration file registering recognized custom markers to prevent warnings and typos. |
| [`test_markers.py`](./test_markers.py) | Unit tests tagged with `@pytest.mark.smoke`, `@pytest.mark.slow`, and `@pytest.mark.regression`. |

---

## Technical Details

### 1. Marker Registration (`pytest.ini`)

Pytest allows custom markers to be applied freely, but unregistered markers produce `PytestUnknownMarkWarning` warnings and can hide accidental typos (e.g., mistyping `@pytest.mark.smok`). Registering markers in `pytest.ini` enforces schema validation and self-documents the test suite:

```ini
[pytest]
# Here we register the markers
markers =
    smoke: critical path tests
    slow: tests that take a long time
    regression: tests for previously fixed bugs
```

- **`smoke`**: High-priority sanity checks covering critical user journeys (e.g., authentication, order checkout).
- **`slow`**: Heavyweight or time-intensive tests (e.g., intensive data processing, PDF generation) that should be excluded from quick feedback loops.
- **`regression`**: Targeted tests verifying that resolved bugs and defects remain fixed.

---

### 2. Implementing Marked Tests (`test_markers.py`)

Decorate test functions using `@pytest.mark.<marker_name>`:

```python
import pytest

@pytest.mark.smoke
def test_critical_login():
    assert True
    
@pytest.mark.smoke
def test_critical_checkout():
    assert True
    
@pytest.mark.slow
def test_full_report_generation():
    assert True
    
@pytest.mark.regression
def test_old_bug_stays_fixed():
    assert True
```

---

## Marker Selection Expressions

Pytest provides the `-m <expression>` flag to filter tests dynamically based on boolean logic:

| Expression | Explanation |
|---|---|
| `-m smoke` | Runs only tests decorated with `@pytest.mark.smoke`. |
| `-m slow` | Runs only tests decorated with `@pytest.mark.slow`. |
| `-m regression` | Runs only tests decorated with `@pytest.mark.regression`. |
| `-m "not slow"` | Runs all fast tests, excluding slow ones. |
| `-m "smoke or regression"` | Runs tests matching either `smoke` or `regression`. |
| `-m "smoke and not slow"` | Runs tests that are `smoke` but not `slow`. |

---

## How to Run the Tests

### From the Repository Root:

```bash
# Run all tests in this folder
python -m pytest Lab03-Assertions-Organizations/custom-markers -v

# Run only critical smoke tests
python -m pytest Lab03-Assertions-Organizations/custom-markers -m smoke -v

# Run all fast tests excluding slow ones
python -m pytest Lab03-Assertions-Organizations/custom-markers -m "not slow" -v

# Run both smoke and regression tests
python -m pytest Lab03-Assertions-Organizations/custom-markers -m "smoke or regression" -v
```

### From within this Directory:

```bash
# Run all tests
python -m pytest -v

# Filter by marker
python -m pytest -m smoke -v

# View all registered markers with descriptions
python -m pytest --markers
```

---

## Expected Output

### Running Smoke Tests (`pytest -m smoke -v`):
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0
rootdir: .../Lab03-Assertions-Organizations/custom-markers
configfile: pytest.ini
collected 4 items / 2 deselected / 2 selected

test_markers.py::test_critical_login PASSED                             [ 50%]
test_markers.py::test_critical_checkout PASSED                          [100%]

======================= 2 passed, 2 deselected in 0.04s =======================
```

### Running Fast Suite (`pytest -m "not slow" -v`):
```text
============================= test session starts =============================
collected 4 items / 1 deselected / 3 selected

test_markers.py::test_critical_login PASSED                             [ 33%]
test_markers.py::test_critical_checkout PASSED                          [ 66%]
test_markers.py::test_old_bug_stays_fixed PASSED                       [100%]

======================= 3 passed, 1 deselected in 0.04s =======================
```
