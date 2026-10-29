# Code That Depends on Randomness: Isolating Non-Deterministic Behavior

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab06-MockingAndTestDoubles](../README.md)

---

## Overview

In automated unit testing, software components frequently interact with non-deterministic or volatile external dependencies—such as pseudo-random number generators, real-time system clocks, external hardware sensors, network endpoints, or remote web services.

When unit tests directly execute code that relies on uncontrolled randomness:
1. **Tests become non-deterministic (flaky):** A test suite may pass during one run and fail during the next without any code change, eroding trust in CI/CD pipelines.
2. **Branch coverage is incomplete:** Infrequent or extreme branches (such as freezing cold or catastrophic failure states) are executed only by chance and remain unverified in most test runs.
3. **Defect localization is compromised:** When a test fails intermittently, reproducing the precise failure conditions becomes difficult.

This submodule demonstrates how to isolate non-deterministic dependencies using **test doubles** and **monkey-patching** via Python's standard library `unittest.mock.patch`. By intercepting calls to the random number generator and substituting controlled return values, tests achieve complete determinism, 100% branch coverage, and instantaneous execution.

---

## Directory Structure

```text
code-that-depends-on-randomness/
├── weather.py         # System Under Test: temperature simulation & weather classifier
├── test_problem.py    # Anti-pattern: weak, non-deterministic test asserting against random output
├── test_solution.py   # Refactored solution: deterministic unit tests using unittest.mock.patch
└── README.md          # Submodule comprehensive guide
```

---

## Files in this Directory

| File | Description |
|---|---|
| [`weather.py`](./weather.py) | System Under Test (SUT) featuring `get_temperature()` (simulated random Celsius readings) and `describe_weather()` (multi-branch temperature classifier). |
| [`test_problem.py`](./test_problem.py) | Anti-pattern demonstration: unmocked test asserting against random outcomes that fails to verify branch correctness or boundary logic. |
| [`test_solution.py`](./test_solution.py) | Robust, deterministic test suite utilizing `unittest.mock.patch` as a context manager to isolate each temperature branch. |

---

## Technical Deep Dive

### 1. The System Under Test (`weather.py`)

The module defines a temperature sampling function and a multi-branch classifier:

```python
import random

def get_temperature():
    """Simulate getting the current temperature in Celsius."""
    return random.randint(-10, 40)  # Random temperature between -10 and 40 degrees Celsius, mock data for testing purposes

def describe_weather():
    temp = get_temperature()
    if temp < 0:
        return "Freezing"
    elif temp < 15:
        return "Cold"
    elif temp < 25:
        return "Pleasant"
    else:
        return "Hot"
```

#### Classification Rules:
| Condition | Return Value | Category |
|---|---|---|
| $\text{temp} < 0$ | `"Freezing"` | Sub-zero temperatures |
| $0 \le \text{temp} < 15$ | `"Cold"` | Low positive temperatures |
| $15 \le \text{temp} < 25$ | `"Pleasant"` | Moderate comfortable temperatures |
| $\text{temp} \ge 25$ | `"Hot"` | Elevated temperatures |

Because `describe_weather()` calls `get_temperature()`, which generates pseudo-random numbers via `random.randint(-10, 40)`, its return value changes on every invocation.

---

### 2. The Anti-Pattern: Non-Deterministic "Weak" Testing (`test_problem.py`)

```python
from weather import describe_weather

def test_get_weather():
    result = describe_weather()  # call the function to get the weather description
    assert result in ["Freezing", "Cold", "Pleasant", "Hot"]  # check that the result is one of the expected weather descriptions
```

#### Why This Test is Ineffective:
1. **Zero Branch Logic Verification:** The assertion only verifies that the returned string belongs to the whitelist of expected labels. If a bug in `describe_weather()` mapped $-5\,^\circ\text{C}$ to `"Hot"`, the test would still pass.
2. **Untested Code Paths:** In any single test execution, only **one** random branch is executed ($\approx 25\%$ coverage). The other three branches are left unexercised.
3. **Masked Regressions & False Confidence:** The test passes consistently on CI, masking severe regressions in classification thresholds and boundary conditions.

---

### 3. The Solution: Deterministic Patching with `unittest.mock.patch` (`test_solution.py`)

Python's `unittest.mock.patch` temporarily replaces a target callable or object within a specified namespace for the duration of a test block.

```python
from unittest.mock import patch
from weather import describe_weather

def test_hot_weather():
    with patch('weather.get_temperature', return_value=30):  # Mock get_temperature to return 30
        assert describe_weather() == "Hot"

def test_freezing_weather():
    with patch('weather.get_temperature', return_value=-5):  # Mock get_temperature to return -5
        assert describe_weather() == "Freezing"

def test_cold_weather():
    with patch('weather.get_temperature', return_value=5):  # Mock get_temperature to return 5
        assert describe_weather() == "Cold"

def test_pleasant_weather():
    with patch('weather.get_temperature', return_value=20):  # Mock get_temperature to return 20
        assert describe_weather() == "Pleasant"
```

#### Mechanics of `unittest.mock.patch`:
- **Namespace Interception (`'weather.get_temperature'`):** The `patch` function targets `get_temperature` inside the `weather` module namespace where `describe_weather` looks it up.
- **Fixed Output (`return_value=...`):** Instead of executing `random.randint`, the patched stub immediately returns the configured scalar value.
- **Context Management (`with patch(...)`):** When the `with` block exits, the patcher automatically restores the original function, ensuring zero side-effects or leakage across other test cases.
- **100% Branch Coverage:** Each test deterministically feeds a known temperature, guaranteeing that every conditional branch (`Freezing`, `Cold`, `Pleasant`, `Hot`) is verified independently.

---

## Comparison: Weak Testing vs. Mocked Testing

| Criterion | Weak Testing (`test_problem.py`) | Mocked Testing (`test_solution.py`) |
|---|---|---|
| **Determinism** | **Non-deterministic:** Output depends on pseudo-random generator state. | **100% Deterministic:** Controlled input values guarantee identical outcomes on every run. |
| **Branch Coverage** | Only 1 random branch tested per execution ($\approx 25\%$). | Guarantees 100% branch coverage across all 4 classification paths. |
| **Defect Detection** | Cannot detect boundary mistakes or inverted conditional logic. | Fails immediately if threshold logic or return values deviate. |
| **Boundary Testing** | Impossible to reliably test specific boundary points (e.g., $0, 14, 15, 24, 25$). | Easily tests exact boundary values by setting specific `return_value`s. |
| **Test Independence** | Inherently coupled to uncontrollable Python runtime randomness. | Fully decoupled, repeatable, and self-contained. |

---

## How to Run the Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running All Tests in this Subdirectory:
From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles/code-that-depends-on-randomness -v
```

### Running Weak Anti-Pattern vs. Deterministic Solution Individually:
```bash
# Run the weak problem test
python -m pytest Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_problem.py -v

# Run the deterministic mocked solution
python -m pytest Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
plugins: anyio-4.14.2, flet-0.86.5, platformdirs-4.12.4, cov-7.1.0
collecting ... collected 5 items

Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_problem.py::test_get_weather PASSED [ 20%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_hot_weather PASSED [ 40%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_freezing_weather PASSED [ 60%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_cold_weather PASSED [ 80%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_pleasant_weather PASSED [100%]

============================== 5 passed in 0.05s ==============================
```
