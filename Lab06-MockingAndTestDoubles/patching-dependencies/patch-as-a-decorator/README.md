# Patching as a Decorator

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [patching-dependencies](../README.md)

---

## Overview

The `@patch` decorator from Python's `unittest.mock` package provides an elegant, expressive way to intercept functions or classes for an entire test function. When a test is decorated with `@patch("target.path")`, the mock library:
1. Replaces the target in that namespace with a mock object when the test begins.
2. Injects the created mock into the test function's arguments.
3. Automatically unpatches the target when the test completes (even if an exception occurs).

This submodule covers how to use `@patch` to mock functions returning environmental values (temperatures) and temporal values (calendar years).

---

## Files in this Directory

| File | Description |
|---|---|
| [`weather.py`](./weather.py) | Defines `get_temperature()` (returns a baseline reading) and `describe_weather()` (returns `"Pleasant"` if $\ge 15$, else `"Cold"`). |
| [`test_get_temperature.py`](./test_get_temperature.py) | Unit tests using `@patch("weather.get_temperature")` to verify both `"Pleasant"` and `"Cold"` classification branches. |
| [`date_utils.py`](./date_utils.py) | Defines `get_year()` and `report_name()` which generates string formatted as `f"Report-{get_year()}"`. |
| [`test_report_name.py`](./test_report_name.py) | Unit test using `@patch("date_utils.get_year")` to simulate future years without altering calendar clocks. |

---

## Technical Deep Dive

### 1. Mocking Environmental Readings (`weather.py` & `test_get_temperature.py`)

#### Source Code (`weather.py`):
```python
def get_temperature():
    return 20

def describe_weather():
    if get_temperature() >= 15:
        return "Pleasant"
    return "Cold"
```

#### Test Code (`test_get_temperature.py`):
```python
from unittest.mock import patch
from weather import describe_weather

@patch("weather.get_temperature")
def test_pleasant_weather(mock_temp):
    mock_temp.return_value = 20
    assert describe_weather() == "Pleasant"

@patch("weather.get_temperature")
def test_cold_weather(mock_temp):
    mock_temp.return_value = 5
    assert describe_weather() == "Cold"
```

#### How it Works:
- `@patch("weather.get_temperature")`: Intercepts `get_temperature` inside `weather.py`.
- `def test_pleasant_weather(mock_temp)`: The patched mock is injected as the `mock_temp` parameter.
- `mock_temp.return_value = 20`: Sets the return value when `describe_weather()` executes `get_temperature()`.
- Both branches ($\ge 15$ and $< 15$) are verified with 100% determinism.

---

### 2. Mocking System Clocks & Temporal Functions (`date_utils.py` & `test_report_name.py`)

Functions that generate reports, timestamps, or expiration tokens depend on system time. Hardcoding assertions against `datetime.now()` or `get_year()` causes tests to fail as time progresses.

#### Source Code (`date_utils.py`):
```python
def get_year():    
    return 2026

def report_name():    
    return f"Report-{get_year()}"
```

#### Test Code (`test_report_name.py`):
```python
from unittest.mock import patch
from date_utils import report_name

@patch("date_utils.get_year")
def test_report_name(mock_year):    
    mock_year.return_value = 2030 
    assert report_name() == "Report-2030"
```

#### Key Takeaway:
By patching `date_utils.get_year` to return `2030`, we test string formatting for arbitrary future or past years without modifying host machine settings.

---

## How to Run the Tests

From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
collecting ... collected 3 items

Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_get_temperature.py::test_pleasant_weather PASSED [ 33%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_get_temperature.py::test_cold_weather PASSED [ 66%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_report_name.py::test_report_name PASSED [100%]

============================== 3 passed in 0.06s ==============================
```
