# Mock Lab: Test Doubles & Isolation with Mocking

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

In automated unit testing, code under test often depends on non-deterministic, slow, or volatile external dependencies—such as random number generators, network web services, system clocks, third-party APIs, or databases.

When tests rely directly on uncontrollable dependencies:
1. **Tests become non-deterministic (flaky):** The same test suite may pass or fail intermittently without any code changes.
2. **Branch coverage is incomplete:** Infrequent edge cases or error branches may never trigger during test execution.
3. **Execution is slowed:** Real network or I/O calls increase test runtimes significantly.

This lab explores **Mocking and Test Doubles** in Python using `unittest.mock.patch`. By intercepting and substituting non-deterministic dependencies with controlled mock objects, tests achieve complete determinism, 100% branch coverage, and fast execution.

---

## Directory Structure

```text
Mock Lab/
├── weather.py         # System Under Test: weather classification with random temperature simulation
├── test_problem.py    # Anti-pattern: weak, non-deterministic test asserting against random output
├── test_solution.py   # Refactored solution: deterministic unit tests using unittest.mock.patch
└── README.md          # Mock Lab comprehensive guide
```

---

## Files in this Directory

| File | Description |
|---|---|
| [`weather.py`](./weather.py) | Weather classification module with `get_temperature()` (random integer generator) and `describe_weather()` (multi-branch temperature threshold classifier). |
| [`test_problem.py`](./test_problem.py) | Problem demonstration: unmocked test that passes trivially on random outcomes but fails to verify branch correctness or boundary logic. |
| [`test_solution.py`](./test_solution.py) | High-quality unit test suite using `unittest.mock.patch` to isolate `describe_weather()` and test each branch deterministically. |

---

## Technical Deep Dive

### 1. The System Under Test (`weather.py`)

```python
import random

def get_temperature():
    """Simulate getting the current temperature in Celsius."""
    return random.randint(-10, 40)  # Random temperature between -10 and 40 °C

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

The `describe_weather()` function classifies ambient temperatures into four distinct bands:
- $\text{temp} < 0 \rightarrow$ `"Freezing"`
- $0 \le \text{temp} < 15 \rightarrow$ `"Cold"`
- $15 \le \text{temp} < 25 \rightarrow$ `"Pleasant"`
- $\text{temp} \ge 25 \rightarrow$ `"Hot"`

Because `describe_weather()` calls `get_temperature()`, which generates random numbers via `random.randint(-10, 40)`, its output changes on every invocation.

---

### 2. The Anti-Pattern: Non-Deterministic "Weak" Testing (`test_problem.py`)

```python
from weather import describe_weather

def test_get_weather():
    result = describe_weather()
    assert result in ["Freezing", "Cold", "Pleasant", "Hot"]
```

#### Why This Test is Ineffective:
1. **Zero Branch Verification:** The test merely asserts that the output belongs to the list of possible labels. If `describe_weather()` returned `"Hot"` when the temperature was $-10\,^\circ\text{C}$, the assertion would still evaluate to `True`.
2. **Untested Scenarios:** In any single test run, only **one** random branch is executed. The other three branches are left completely unexercised.
3. **False Confidence:** The test suite reports green (passing), giving the false impression that temperature logic is thoroughly verified when defects could easily slip into production.

---

### 3. The Solution: Deterministic Mocking with `unittest.mock.patch` (`test_solution.py`)

Python's standard library provides `unittest.mock.patch` to temporarily replace a target function or object during the scope of a test.

```python
from unittest.mock import patch
from weather import describe_weather

def test_hot_weather():
    with patch('weather.get_temperature', return_value=30):
        assert describe_weather() == "Hot"

def test_freezing_weather():
    with patch('weather.get_temperature', return_value=-5):
        assert describe_weather() == "Freezing"

def test_cold_weather():
    with patch('weather.get_temperature', return_value=5):
        assert describe_weather() == "Cold"

def test_pleasant_weather():
    with patch('weather.get_temperature', return_value=20):
        assert describe_weather() == "Pleasant"
```

#### How `patch` Works:
1. `patch('weather.get_temperature', return_value=...)`: Intercepts calls to `get_temperature` inside the `weather` module namespace.
2. Instead of executing `random.randint`, the patched function immediately returns the specified `return_value`.
3. When the `with` block exits, the original `get_temperature` function is restored automatically, preventing cross-test pollution.

---

## Comparison: Weak Testing vs. Mocked Testing

| Criterion | Weak Testing (`test_problem.py`) | Mocked Testing (`test_solution.py`) |
|---|---|---|
| **Determinism** | **Non-deterministic:** Output depends on PRNG seed. | **100% Deterministic:** Same inputs always yield same outputs. |
| **Branch Coverage** | Executes only 1 random branch per run ($\approx 25\%$). | Guarantees 100% branch coverage across all conditions. |
| **Defect Detection** | Cannot detect boundary errors or wrong branch returns. | Catches logic errors immediately if classification changes. |
| **Test Independence** | Couples test results to external randomness. | Completely isolated from external dependencies. |

---

## How to Run the Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running All Tests in Mock Lab:
```bash
python -m pytest "Mock Lab" -v
```

### Running Weak Problem vs. Robust Solution Separately:
```bash
# Run the weak problem test
python -m pytest "Mock Lab/test_problem.py" -v

# Run the deterministic mocked solution
python -m pytest "Mock Lab/test_solution.py" -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: .../Mock Lab
collected 5 items

test_problem.py::test_get_weather PASSED                                 [ 20%]
test_solution.py::test_hot_weather PASSED                                [ 40%]
test_solution.py::test_freezing_weather PASSED                           [ 60%]
test_solution.py::test_cold_weather PASSED                               [ 80%]
test_solution.py::test_pleasant_weather PASSED                           [100%]

============================== 5 passed in 0.32s ==============================
```
