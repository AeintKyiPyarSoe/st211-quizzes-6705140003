# Skipping Tests and Expected Failures (`skip`, `skipif`, `xfail`)

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab03-Assertions-Organizations](../README.md)

---

## Overview

In real-world software engineering, test suites must accommodate incomplete features, platform-specific constraints, and known unresolved defects without breaking continuous integration (CI) pipelines.

Pytest provides built-in mechanisms to handle these scenarios gracefully:
1. **Unconditional Skipping (`@pytest.mark.skip`):** Completely bypasses execution of a test (e.g., pending feature completion).
2. **Conditional Skipping (`@pytest.mark.skipif`):** Skips tests dynamically when specific runtime conditions or environmental requirements are met (e.g., minimum Python version, missing configuration files, specific operating systems).
3. **Expected Failures (`@pytest.mark.xfail`):** Executes a test that is known to fail due to an existing bug. If it fails, Pytest reports `XFAIL` without failing the build. If it passes unexpectedly, Pytest reports `XPASS`.

---

## Files in this Directory

| File | Description |
|---|---|
| [`pytest.ini`](./pytest.ini) | Configuration file configuring default runner flags (`addopts = -v --tb=short --strict-markers`), discovery patterns, and registered markers. |
| [`test_skips.py`](./test_skips.py) | Demonstrates unconditional skipping (`@pytest.mark.skip`) and version-based conditional skipping (`@pytest.mark.skipif`). |
| [`test_conditional.py`](./test_conditional.py) | Demonstrates file/path availability conditional skipping (`os.path.exists`). |
| [`test_xfail.py`](./test_xfail.py) | Demonstrates expected failure behavior (`XFAIL`) and unexpected pass behavior (`XPASS`). |

---

## Technical Details

### 1. Unconditional & Version-Based Skipping (`test_skips.py`)

Rather than commenting out unfinished tests—which loses visibility—mark them with `@pytest.mark.skip` and provide a clear `reason`:

```python
import pytest
import sys

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    assert False # would fail if run, but is skipped
    
@pytest.mark.skipif(sys.version_info < (3,8), reason="Require Python 3.8+")
def test_needs_modern_python():
    assert True
```

- `test_future_feature`: Pytest detects the `@pytest.mark.skip` decorator and bypasses execution, preventing `assert False` from triggering a build failure.
- `test_needs_modern_python`: Uses `@pytest.mark.skipif` to evaluate Python's runtime version. Since current environments use Python 3.8+, the condition evaluates to `False` and the test runs and passes normally.

---

### 2. Environment & OS Conditional Skipping (`test_conditional.py`)

Conditional skips can evaluate filesystem existence, operating system platform, or environment variables:

```python
import pytest
import os

@pytest.mark.skipif(not os.path.exists("/etc/hosts"), reason="No hosts file")
def test_hosts_file():
    assert os.pa.exists("/etc/hosts")
```

- On Windows machines where `/etc/hosts` does not exist, `not os.path.exists("/etc/hosts")` evaluates to `True`. Pytest skips this test immediately, reporting `SKIPPED` with the reason `"No hosts file"`.
- On Linux/macOS systems where `/etc/hosts` exists, the test executes.

---

### 3. Expected Failures (`test_xfail.py`)

When tracking a known bug that cannot be fixed immediately, mark the test with `@pytest.mark.xfail`. This keeps the test enabled and monitored in the suite without causing false alarms in CI:

```python
import pytest

@pytest.mark.xfail(reason="Known bug #123, fix pending")
def test_known_broken_feature():
    assert 1 == 2 # currently broken
    
@pytest.mark.xfail(reason="Might pass sometimes")
def test_actually_works_now():
    assert 1 == 1 # this will XPASS
```

#### Outcome Definitions:

| Outcome | Code Condition | Meaning | Suite Status |
|---|---|---|:---:|
| **`XFAIL`** (Expected Failure) | Marked `@pytest.mark.xfail`, assertion fails (`assert 1 == 2`) | The test failed as anticipated due to a documented bug. | **Success (Exit 0)** |
| **`XPASS`** (Unexpected Pass) | Marked `@pytest.mark.xfail`, assertion passes (`assert 1 == 1`) | The test passed despite expectations. Indicates the bug may have been resolved. | **Success (Exit 0)** |

---

### 4. Pytest Configuration (`pytest.ini`)

```ini
[pytest]
# Here we register the markers

testpaths = .
# which folders it should search for tests in by default

addopts = -v --tb=short --strict-markers

markers =
    smoke: critical path tests
    slow: tests that take a long time
    regression: tests for previously fixed bugs

python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

- `addopts = -v --tb=short --strict-markers`:
  - `-v`: Verbose output showing each test item and outcome.
  - `--tb=short`: Concise traceback format for failure diagnostics.
  - `--strict-markers`: Disallows unregistered markers, raising errors on typos.

---

## How to Run the Tests

### From the Repository Root:

```bash
# Run all tests in this folder
python -m pytest Lab03-Assertions-Organizations/skipping-and-expected-failures -v

# Display detailed summary reasons for skipped, xfailed, and xpassed tests
python -m pytest Lab03-Assertions-Organizations/skipping-and-expected-failures -v -rsxX
```

### From within this Directory:

```bash
# Run tests with default flags from pytest.ini
python -m pytest

# Run with full summary details
python -m pytest -rsxX
```

---

## Expected Output

Running with `python -m pytest -rsxX`:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0
rootdir: .../Lab03-Assertions-Organizations/skipping-and-expected-failures
configfile: pytest.ini
collected 5 items

test_conditional.py::test_hosts_file SKIPPED                             [ 20%]
test_skips.py::test_future_feature SKIPPED                               [ 40%]
test_skips.py::test_needs_modern_python PASSED                           [ 60%]
test_xfail.py::test_known_broken_feature XFAIL                          [ 80%]
test_xfail.py::test_actually_works_now XPASS                             [100%]

=================================== XPASSES ===================================
=========================== short test summary info ===========================
SKIPPED [1] test_conditional.py:4: No hosts file
SKIPPED [1] test_skips.py:4: Feature not implemented yet
XFAIL test_xfail.py::test_known_broken_feature - Known bug #123, fix pending
XPASS test_xfail.py::test_actually_works_now - Might pass sometimes
============= 1 passed, 2 skipped, 1 xfailed, 1 xpassed in 0.19s ==============
```
