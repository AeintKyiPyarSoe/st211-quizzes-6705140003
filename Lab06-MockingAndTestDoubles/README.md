# Lab 06: Mocking & Test Doubles

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

In automated unit testing, the primary objective is to verify that a specific unit of code behaves correctly in complete isolation from external, slow, complex, or non-deterministic collaborators. In production systems, software rarely functions in isolation—it frequently interacts with payment gateways, relational databases, email servers, external APIs, system clocks, and pseudo-random number generators.

Testing directly against real collaborators introduces severe challenges:
1. **Non-Determinism (Flakiness):** Systems depending on random values, system clocks, or network latencies produce variable outcomes across test runs.
2. **Incomplete Branch Coverage:** Unlikely error codes, network timeouts, or specific boundary conditions are difficult or impossible to reliably trigger.
3. **Slow Execution & Fragility:** Real network or database operations drastically slow down test feedback loops and fail when external infrastructure is unavailable or offline.
4. **Unintended Side-Effects:** Executing real charging logic against payment processors, sending real emails to users, or writing to shared databases incurs costs and pollutes persistent storage.

**Lab 06: Mocking & Test Doubles** provides hands-on mastery over Python's standard `unittest.mock` library. By substituting live external collaborators with simulated **Test Doubles** (Mocks, Stubs, and Spies) and utilizing `unittest.mock.patch` for namespace interception, test suites achieve 100% determinism, complete branch coverage, safe execution, and rapid feedback.

---

## Key Learning Objectives

1. **Test Double Concepts & Taxonomy:** Distinguishing between standard test double roles (Dummies, Stubs, Mocks, Spies, and Fakes).
2. **Core Mock Mechanics (`Mock`):** Creating mock objects, configuring static return values (`mock.method.return_value`), and leveraging dynamic attribute creation.
3. **Dependency Injection with Mocks:** Supplying mock collaborators directly into dependent classes (e.g., injecting a mock `PaymentGateway` into `OrderProcessor`) without monkey-patching.
4. **Configured Return Values vs. Dynamic Side Effects:** Using `return_value` for static stubbing and `side_effect` for sequential return values (`[1, 2, 3]`), custom callbacks, or exception throwing.
5. **Namespace Patching (`unittest.mock.patch`):** 
   - Intercepting module-level dependencies using `@patch` as a decorator.
   - Using `with patch(...)` as a context manager to isolate external network operations (e.g., `smtplib.SMTP`).
   - Mastering the rule of patching where objects are *looked up*, not where they are *defined*.
6. **Eliminating Test Flakiness:** Replacing non-deterministic pseudo-random number outputs (`random.randint`) with fixed values to achieve 100% branch coverage.
7. **Behavior & Interaction Verification:** Verifying method invocations using `assert_called()`, `assert_called_once()`, `assert_called_with(...)`, inspecting `call_count`, and diagnosing call expectation failures.

---

## Directory Structure

```text
Lab06-MockingAndTestDoubles/
├── code-that-depends-on-randomness/          # Submodule 1: Isolating non-deterministic dependencies
│   ├── weather.py                           # SUT: temperature simulation & weather classifier
│   ├── test_problem.py                      # Anti-pattern: weak unmocked test on random data
│   ├── test_solution.py                     # Solution: deterministic tests via patch context manager
│   └── README.md                            # Detailed guide on isolating randomness
│
├── mock-objects-and-return-values/           # Submodule 2: Mock mechanics, DI & return values
│   ├── dependency/                          # Dependency injection with mocks
│   │   ├── payment.py                       # PaymentGateway interface & OrderProcessor SUT
│   │   ├── test_payment.py                  # Injected mock gateway test
│   │   └── README.md                        # Guide on dependency injection
│   ├── return_value-vs-side_effect/         # Static return values vs dynamic side effects
│   │   ├── username.py                      # UserService domain class
│   │   ├── test_get_username.py             # Single return value via return_value
│   │   ├── test_return_values.py            # Sequential return values via side_effect
│   │   └── README.md                        # Guide on return_value vs side_effect
│   ├── test_mock_basics.py                  # Core Mock creation, dynamic attributes, return_value
│   └── README.md                            # Guide on mock objects and return values
│
├── patching-dependencies/                   # Submodule 3: Monkey-patching namespaces & external services
│   ├── patch-as-a-decorator/                # Function-level patching via @patch
│   │   ├── date_utils.py                    # get_year() and report_name()
│   │   ├── weather.py                       # get_temperature() and describe_weather()
│   │   ├── test_get_temperature.py          # @patch("weather.get_temperature")
│   │   ├── test_report_name.py              # @patch("date_utils.get_year")
│   │   └── README.md                        # Guide on decorator-based patching
│   ├── patch-the-email-function/            # Block-level patching via context manager
│   │   ├── notifications.py                 # send_email() via smtplib & notify_user()
│   │   ├── test_notifications.py            # with patch("notifications.send_email")
│   │   └── README.md                        # Guide on patching network/email functions
│   └── README.md                            # Comprehensive guide on patching dependencies
│
├── verifying-calls/                         # Submodule 4: Interaction & behavior verification
│   ├── test_verify_calls.py                 # assert_called, assert_called_once, assert_called_with, call_count
│   └── README.md                            # Guide on call verification & failure analysis
│
└── README.md                                # Lab 06 master documentation
```

---

## Submodule Summaries

| Submodule | Directory | Key Concepts Covered | Detailed Guide |
|---|---|---|:---:|
| **1. Code That Depends on Randomness** | [`code-that-depends-on-randomness/`](./code-that-depends-on-randomness/) | Eliminating flakiness, monkey-patching `random.randint`, achieving 100% branch and boundary coverage with `unittest.mock.patch` | [View README](./code-that-depends-on-randomness/README.md) |
| **2. Mock Objects and Return Values** | [`mock-objects-and-return-values/`](./mock-objects-and-return-values/) | `Mock()` instantiation, dynamic attribute creation, Dependency Injection (`PaymentGateway`), `return_value` vs `side_effect` sequences | [View README](./mock-objects-and-return-values/README.md) |
| **3. Patching Dependencies** | [`patching-dependencies/`](./patching-dependencies/) | `@patch` decorator vs `with patch(...)` context manager, mocking system time (`date_utils`), mocking network protocols (`smtplib.SMTP`) | [View README](./patching-dependencies/README.md) |
| **4. Verifying Calls** | [`verifying-calls/`](./verifying-calls/) | Behavior verification, `assert_called()`, `assert_called_once()`, `assert_called_with(...)`, `call_count`, call failure diagnostics | [View README](./verifying-calls/README.md) |

---

## Technical Deep Dive

### 1. Isolating Volatile Random Dependencies (`code-that-depends-on-randomness/`)

When code calls non-deterministic internal functions directly rather than receiving them through dependency injection, `unittest.mock.patch` provides monkey-patching capabilities to intercept the function call at the namespace level.

#### The System Under Test (`weather.py`):
```python
import random

def get_temperature():
    return random.randint(-10, 40)

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

#### The Anti-Pattern (`test_problem.py`):
```python
from weather import describe_weather

def test_get_weather():
    result = describe_weather()
    assert result in ["Freezing", "Cold", "Pleasant", "Hot"]
```
*Why this fails:* The test only validates that the output matches one of the labels. It cannot verify whether the threshold logic is correct, and it executes only one random path per run ($\approx 25\%$ coverage).

#### The Deterministic Solution (`test_solution.py`):
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

Each test intercepts `'weather.get_temperature'` inside the `weather` module namespace and substitutes a deterministic value, guaranteeing 100% test coverage across all branches without flakiness.

---

### 2. Mock Objects, Return Values & Dependency Injection (`mock-objects-and-return-values/`)

#### A. Core Mock Mechanics (`test_mock_basics.py`):
Python's `unittest.mock.Mock` class is designed to stand in for real objects, functions, or classes:
- **`mock.get_data.return_value = "fake data"`:** Pre-programs a static response.
- **Dynamic Method Creation:** Calling `mock.anything()` or `mock.whatever(1, 2, 3)` works out-of-the-box without `AttributeError`.
- **Attribute Assignment:** `mock.name = "TestUser"` stores attributes like a standard object.

#### B. Dependency Injection with Mocks (`dependency/`):
```python
class PaymentGateway:
    def charge(self, amount):
        raise NotImplementedError("Real gateway not available in tests.")
    
class OrderProcessor:
    def __init__(self, gateway):
        self.gateway = gateway
        
    def process(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        result = self.gateway.charge(amount)
        return f"Order processed: {result}"
```
In `test_payment.py`, we instantiate `fake_gateway = Mock()`, configure `fake_gateway.charge.return_value = "SUCCESS-12345"`, and inject it into `OrderProcessor(fake_gateway)`. This completely decouples business logic from external payment infrastructure.

#### C. `return_value` vs `side_effect` (`return_value-vs-side_effect/`):
- **`return_value`:** In `test_get_username.py`, `db.find_user.return_value = "Alice"` returns `"Alice"` every time `get_username()` is invoked.
- **`side_effect`:** In `test_return_values.py`, `mock.next_id.side_effect = [1, 2, 3]` returns successive values across consecutive calls:
  - Call 1: returns `1`
  - Call 2: returns `2`
  - Call 3: returns `3`

---

### 3. Patching Dependencies & Namespaces (`patching-dependencies/`)

#### A. Decorator Pattern (`patch-as-a-decorator/`):
Using `@patch` injects a mock directly into the test arguments:
```python
@patch("weather.get_temperature")
def test_pleasant_weather(mock_temp):
    mock_temp.return_value = 20
    assert describe_weather() == "Pleasant"

@patch("date_utils.get_year")
def test_report_name(mock_year):
    mock_year.return_value = 2030
    assert report_name() == "Report-2030"
```
The mock is automatically torn down after each test function completes.

#### B. Context Manager Pattern (`patch-the-email-function/`):
Using `with patch(...)` isolates patching to a single block, preventing real network calls (`smtplib.SMTP`):
```python
def test_notify_user_without_sending_email():
    with patch("notifications.send_email") as mock_send:
        mock_send.return_value = True
        result = notify_user("student@siam.ac.th")
        
    assert result == "Notified student@siam.ac.th"
```

---

### 4. Verifying Invocations & Behavior (`verifying-calls/`)

Rather than only inspecting returned data, **Behavior Verification** verifies interaction contracts between collaborators:

```python
# 1. Assert called at least once
mock.save.assert_called()

# 2. Assert called exactly once
mock.save.assert_called_once()

# 3. Assert called with specific arguments
mock.charge.assert_called_with(100, currency="USD")

# 4. Verify call count property directly
assert mock.log.call_count == 2
```

#### Diagnostic Failure Analysis:
If `mock.save()` is called twice and asserted with `mock.save.assert_called_once()`, Pytest raises:
```text
AssertionError: Expected 'save' to have been called once. Called 2 times.
Calls: [call(), call()].
```
This precise failure trace enables rapid debugging of unintentional duplicate invocations.

---

## Test Double Taxonomy Reference

In automated testing, test doubles are classified according to specific responsibilities (defined by Gerard Meszaros):

| Test Double Type | Definition | Python Implementation | Primary Use Case in Lab 06 |
|---|---|---|---|
| **Dummy** | An object passed around but never actually used or called. | `dummy = Mock()` | Fulfilling mandatory parameter signatures. |
| **Stub** | An object providing canned answers to calls made during the test. | `mock.find_user.return_value = "Alice"` | Feeding known indirect inputs into `UserService`. |
| **Spy** | A stub that also records information about how it was called. | `mock.charge.assert_called_with(...)` | Verifying invocation counts, order, and parameters. |
| **Mock** | An object pre-programmed with expectations forming a specification. | `fake_gateway = Mock()` | Injecting simulated collaborators into `OrderProcessor`. |
| **Fake** | A working implementation with shortcuts unsuitable for production. | In-memory `dict` or SQLite `:memory:` | Lightweight stateful simulation. |

---

## How to Run the Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running All Lab 06 Tests:
From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles -v
```

### Running Specific Submodules:
```bash
# 1. Run randomness isolation tests
python -m pytest Lab06-MockingAndTestDoubles/code-that-depends-on-randomness -v

# 2. Run mock objects and return values tests
python -m pytest Lab06-MockingAndTestDoubles/mock-objects-and-return-values -v

# 3. Run patching dependencies tests
python -m pytest Lab06-MockingAndTestDoubles/patching-dependencies -v

# 4. Run verifying calls tests
python -m pytest Lab06-MockingAndTestDoubles/verifying-calls -v
```

### Full Test Suite Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
collected 20 items

Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_problem.py::test_get_weather PASSED [  5%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_hot_weather PASSED [ 10%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_freezing_weather PASSED [ 15%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_cold_weather PASSED [ 20%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_pleasant_weather PASSED [ 25%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/dependency/test_payment.py::test_order_processing PASSED [ 30%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/return_value-vs-side_effect/test_get_username.py::test_get_username PASSED [ 35%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/return_value-vs-side_effect/test_return_values.py::test_multiple_return_values PASSED [ 40%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/test_mock_basics.py::test_mock_returs_configured_value PASSED [ 45%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/test_mock_basics.py::test_mock_accepts_any_call PASSED [ 50%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/test_mock_basics.py::test_mock_attributes PASSED [ 55%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_get_temperature.py::test_pleasant_weather PASSED [ 60%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_get_temperature.py::test_cold_weather PASSED [ 65%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-as-a-decorator/test_report_name.py::test_report_name PASSED [ 70%]
Lab06-MockingAndTestDoubles/patching-dependencies/patch-the-email-function/test_notifications.py::test_notify_user_without_sending_email PASSED [ 75%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_was_called PASSED [ 80%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_was_called_once PASSED [ 85%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_was_called_twice_but_expected_once FAILED [ 90%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_called_with_arguments PASSED [ 95%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_call_count PASSED [100%]

================================== FAILURES ===================================
___________________ test_was_called_twice_but_expected_once ___________________

    def test_was_called_twice_but_expected_once():
        mock = Mock()
        mock.save()
        mock.save()
>       mock.save.assert_called_once()
E       AssertionError: Expected 'save' to have been called once. Called 2 times.
E       Calls: [call(), call()].

======================== 1 failed, 19 passed in 0.45s =========================
```
> [!NOTE]
> `test_was_called_twice_but_expected_once` in `verifying-calls/` is designed intentionally to fail to illustrate Pytest failure reporting and `assert_called_once()` contract enforcement. The remaining 19 test cases pass successfully.
