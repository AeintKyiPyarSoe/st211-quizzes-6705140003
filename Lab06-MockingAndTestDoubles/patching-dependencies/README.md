# Patching Dependencies: Decorators and Context Managers

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab06-MockingAndTestDoubles](../README.md)

---

## Overview

In many software architectures, units of code directly invoke external functions, third-party libraries, system clocks, or network APIs rather than receiving them via Dependency Injection. In such cases, we cannot simply pass a `Mock()` into a constructor.

Instead, we must intercept the dependency dynamically in its namespace using **Monkey Patching**. Python's standard library provides `unittest.mock.patch`, which temporarily replaces an object or function in a specified module namespace with a mock object for the duration of a test, restoring the original target afterward.

This directory demonstrates the two primary ways to apply `unittest.mock.patch`:
1. **As a Function Decorator (`@patch(...)`):** Clean and declarative for entire test functions.
2. **As a Context Manager (`with patch(...)`):** Tightly scoped to specific code blocks within a test.

---

## Directory Structure

```text
patching-dependencies/
├── patch-as-a-decorator/
│   ├── date_utils.py                   # Date utility functions: get_year() and report_name()
│   ├── weather.py                      # Weather functions: get_temperature() and describe_weather()
│   ├── test_get_temperature.py         # Patching get_temperature with @patch
│   ├── test_report_name.py             # Patching get_year with @patch
│   └── README.md                       # Guide on decorator-based patching
│
├── patch-the-email-function/
│   ├── notifications.py                # Notification service triggering real smtplib.SMTP
│   ├── test_notifications.py           # Context manager patching with patch() as mock
│   └── README.md                       # Guide on context-manager patching for external I/O
│
└── README.md                           # Comprehensive guide on patching dependencies
```

---

## Submodules Summary

| Submodule | Directory | Key Topics Covered |
|---|---|---|
| **1. Patch as a Decorator** | [`patch-as-a-decorator/`](./patch-as-a-decorator/) | `@patch("module.function")` syntax, injecting mock parameters (`mock_fn`), mocking system dates and sensor readings. |
| **2. Patch Email / I/O Function** | [`patch-the-email-function/`](./patch-the-email-function/) | `with patch(...) as mock_send:` context manager, intercepting network protocols (`smtplib.SMTP`), preventing side-effects. |

---

## Core Principles of Patching

### 1. Where to Patch: The Namespace Rule
A common pitfall with `unittest.mock.patch` is specifying the wrong import path. 

> [!IMPORTANT]
> **The Golden Rule:** Always patch where the object is **looked up (used)**, not where it is **defined**.

For example, if `report_name()` in `date_utils.py` calls `get_year()`:
- Correct target: `"date_utils.get_year"`
- If another module `service.py` does `from date_utils import get_year` and calls `get_year()`, you must patch `"service.get_year"`, because `service` holds its own local reference to the function!

---

### 2. Method 1: Decorator Pattern (`@patch`)

When the entire test relies on a mocked dependency, the `@patch` decorator is clean and idiomatic:

```python
from unittest.mock import patch
from weather import describe_weather

@patch("weather.get_temperature")
def test_pleasant_weather(mock_temp):
    mock_temp.return_value = 20
    assert describe_weather() == "Pleasant"
```

- `@patch("weather.get_temperature")` intercepts `get_temperature` inside `weather.py`.
- It automatically passes the instantiated mock as an argument (`mock_temp`) to the decorated test function.
- When the test exits, Python automatically un-patches `weather.get_temperature`.

---

### 3. Method 2: Context Manager Pattern (`with patch(...)`)

When only a specific statement requires patching, or to avoid adding arguments to the test signature, use `with patch(...)`:

```python
from unittest.mock import patch
from notifications import notify_user

def test_notify_user_without_sending_email():
    with patch("notifications.send_email") as mock_send:
        result = notify_user("student@siam.ac.th")
        
    assert result == "Notified student@siam.ac.th"
```

- `with patch(...) as mock_send` isolates the patch strictly to the indented block.
- Prevents expensive or dangerous operations (such as attempting real SMTP connections across port 25).
- Restores original functionality immediately upon exiting the block, even if an exception occurs.

---

## How to Run the Tests

From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles/patching-dependencies -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
collecting ... collected 4 items

Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_get_temperature.py::test_pleasant_weather PASSED [ 25%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_get_temperature.py::test_cold_weather PASSED [ 50%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_report_name.py::test_report_name PASSED [ 75%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-the-email-function/test_notifications.py::test_notify_user_without_sending_email PASSED [100%]

============================== 4 passed in 0.37s ==============================
```
