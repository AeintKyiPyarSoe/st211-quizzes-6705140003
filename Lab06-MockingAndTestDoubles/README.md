# Lab 06: Mocking & Test Doubles

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

In automated unit testing, the primary goal is to verify that a specific unit of code behaves correctly in complete isolation from external, slow, complex, or non-deterministic dependencies. In production systems, software rarely functions in a vacuum—it frequently interacts with third-party payment gateways, relational databases, network APIs, file systems, system clocks, and pseudo-random number generators.

Testing directly against real collaborators introduces severe challenges:
1. **Non-Determinism (Flakiness):** Systems depending on random values, system clocks, or network latencies produce variable outcomes across test runs.
2. **Incomplete Branch Coverage:** Unlikely error codes, network timeouts, or specific boundary conditions are difficult or impossible to reliably trigger.
3. **Slow Execution & Fragility:** Real network or database operations drastically slow down test feedback loops and fail when external infrastructure is unavailable.
4. **Unintended Side-Effects:** Executing real charging logic against payment processors or writing to shared databases can incur costs or pollute persistent storage.

**Lab 06: Mocking & Test Doubles** explores how to isolate units under test using Python's standard `unittest.mock` library. By substituting live external dependencies with simulated **Test Doubles** (Mocks and Stubs) and utilizing `unittest.mock.patch` for namespace interception, test suites achieve 100% determinism, complete branch coverage, and rapid execution.

---

## Key Learning Objectives

1. **Test Double Concepts & Taxonomy:** Distinguishing between standard test double roles (Dummies, Stubs, Mocks, Spies, and Fakes).
2. **Mock Object Fundamentals (`Mock`):** Creating mock objects, configuring return values (`mock.method.return_value`), and leveraging dynamic attribute creation.
3. **Dynamic Method & Call Acceptance:** Understanding how `Mock` automatically generates attributes and methods upon access, enabling flexible duck-typing and interface mimicry without full implementations.
4. **Dependency Injection with Mocks:** Supplying mock collaborators into dependent classes (e.g., injecting a mock `PaymentGateway` into `OrderProcessor`) to test business logic in isolation.
5. **Namespace Patching (`unittest.mock.patch`):** Intercepting functions and module-level variables within their imported namespaces (e.g., controlling `get_temperature()` in `code-that-depends-on-randomness`).
6. **Eliminating Test Flakiness:** Replacing non-deterministic pseudo-random number outputs with fixed, predictable inputs to achieve 100% branch and boundary coverage.

---

## Directory Structure

```text
Lab06-MockingAndTestDoubles/
├── code-that-depends-on-randomness/          # Submodule: isolating pseudo-random dependencies
│   ├── weather.py                           # SUT: temperature simulation & weather classifier
│   ├── test_problem.py                      # Anti-pattern: weak unmocked test on random data
│   ├── test_solution.py                     # Solution: deterministic tests via unittest.mock.patch
│   └── README.md                            # Detailed guide on isolating randomness
│
├── payment.py                               # Domain model: PaymentGateway & OrderProcessor
├── test_mock_basics.py                      # Core Mock object mechanics & return values
└── README.md                                # Lab 06 comprehensive documentation
```

---

## Submodule & File Summaries

| Component / Submodule | Path | Key Concepts Covered | Documentation / Link |
|---|---|---|:---:|
| **Mock Basics** | [`test_mock_basics.py`](./test_mock_basics.py) | `Mock()` creation, `.return_value` configuration, arbitrary method call acceptance, mock attribute storage | [Jump to Section](#1-core-mock-object-mechanics-test_mock_basicspy) |
| **Payment Gateway Service** | [`payment.py`](./payment.py) | Dependency injection, interface contracts (`NotImplementedError`), decoupling business logic from real gateways | [Jump to Section](#2-dependency-injection--collaborator-mocking-paymentpy) |
| **Randomness Isolation** | [`code-that-depends-on-randomness/`](./code-that-depends-on-randomness/) | Namespace monkey-patching (`unittest.mock.patch`), eliminating flaky tests, deterministic 100% branch coverage | [View Submodule README](./code-that-depends-on-randomness/README.md) |

---

## Technical Deep Dive

### 1. Core Mock Object Mechanics (`test_mock_basics.py`)

Python's `unittest.mock.Mock` class is designed to stand in for real objects, functions, or classes. It dynamically creates attributes and methods as they are accessed and records all interactions.

```python
from unittest.mock import Mock

def test_mock_returs_configured_value():
    mock = Mock()  # create a mock object using Mock()
    mock.get_data.return_value = "fake data"  # configure return value for get_data()
    assert mock.get_data() == "fake data"  # verify configured value is returned

def test_mock_accepts_any_call():
    mock = Mock()
    mock.anything()  # mock automatically creates methods when they are accessed
    mock.whatever(1, 2, 3)

def test_mock_attributes():
    mock = Mock()
    mock.name = "TestUser"  # assign an attribute to the mock
    assert mock.name == "TestUser"  # attribute can be read back like a normal object
```

#### Key Capabilities Demonstrated:
- **Predefined Return Values:** `mock.get_data.return_value = "fake data"` specifies what value should be returned when the callable attribute is invoked. This allows tests to simulate successful responses, error payloads, or complex domain objects.
- **Dynamic Attribute Creation:** Accessing any attribute or method (e.g., `mock.anything()`, `mock.whatever(...)`) automatically creates a new child `Mock` instance on demand, avoiding `AttributeError` and allowing arbitrary API simulation.
- **Attribute Storage:** Attributes can be assigned directly (`mock.name = "TestUser"`) and inspected, enabling the mock to act as a lightweight data transfer object.

---

### 2. Dependency Injection & Collaborator Mocking (`payment.py`)

In production architectures, services rely on interfaces or external collaborators. `payment.py` demonstrates a payment processing domain:

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

#### The Problem:
`PaymentGateway.charge()` raises `NotImplementedError("Real gateway not available in tests.")` because in a real production system, calling a live gateway requires network connections, authentication tokens, and charges real credit cards.

#### The Testing Solution with Mocks:
Because `OrderProcessor` uses **Dependency Injection** (receiving its `gateway` in `__init__`), unit tests can instantiate a `Mock()` gateway and inject it into the processor:

```python
from unittest.mock import Mock
import pytest
from payment import OrderProcessor

def test_order_processor_success():
    # Arrange: instantiate mock gateway and configure return value
    mock_gateway = Mock()
    mock_gateway.charge.return_value = "TXN_12345"
    processor = OrderProcessor(gateway=mock_gateway)
    
    # Act: execute business logic
    response = processor.process(100)
    
    # Assert: verify outcome and ensure real gateway was never called
    assert response == "Order processed: TXN_12345"
    mock_gateway.charge.assert_called_once_with(100)

def test_order_processor_invalid_amount():
    mock_gateway = Mock()
    processor = OrderProcessor(gateway=mock_gateway)
    
    with pytest.raises(ValueError, match="Amount must be positive"):
        processor.process(-10)
        
    # Verify gateway is never called when validation fails
    mock_gateway.charge.assert_not_called()
```

This pattern guarantees:
1. **Total Isolation:** Unit tests verify only `OrderProcessor` logic without executing external gateway code.
2. **Behavior Verification:** Using `assert_called_once_with()` and `assert_not_called()` ensures that collaborator methods are invoked with the exact expected parameters and only when valid.

---

### 3. Isolating Volatile Random Dependencies (`code-that-depends-on-randomness/`)

When code calls non-deterministic internal functions directly rather than receiving them through dependency injection, `unittest.mock.patch` provides **monkey-patching** capabilities to intercept the function call at the namespace level.

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

## Test Double Taxonomy Reference

The term "mock" is often used loosely, but in software engineering, test doubles are classified according to specific responsibilities (defined by Gerard Meszaros):

| Test Double Type | Definition | Python Implementation | Primary Use Case |
|---|---|---|---|
| **Dummy** | An object passed around but never actually used or called. | `dummy = Mock()` | Fulfilling mandatory parameter signatures. |
| **Stub** | An object providing canned answers to calls made during the test. | `stub.get_value.return_value = 42` | Feeding known indirect inputs into the SUT. |
| **Spy** | A stub that also records information about how it was called. | `mock.method.assert_called_with(...)` | Verifying interaction counts, order, and arguments. |
| **Mock** | An object pre-programmed with expectations that form a specification of the expected calls. | `unittest.mock.Mock()` | Interaction-based behavior verification. |
| **Fake** | A working implementation with shortcuts unsuitable for production (e.g., in-memory DB). | In-memory `dict` or SQLite `:memory:` | Lightweight stateful simulation. |

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

### Running Specific Test Suites:
```bash
# 1. Run basic mock mechanics tests
python -m pytest Lab06-MockingAndTestDoubles/test_mock_basics.py -v

# 2. Run the randomness isolation submodule tests
python -m pytest Lab06-MockingAndTestDoubles/code-that-depends-on-randomness -v

# 3. Run individual tests within the randomness submodule
python -m pytest Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
plugins: anyio-4.14.2, flet-0.86.5, platformdirs-4.12.4, cov-7.1.0
collecting ... collected 8 items

Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_problem.py::test_get_weather PASSED [ 12%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_hot_weather PASSED [ 25%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_freezing_weather PASSED [ 37%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_cold_weather PASSED [ 50%]
Lab06-MockingAndTestDoubles/code-that-depends-on-randomness/test_solution.py::test_pleasant_weather PASSED [ 62%]
Lab06-MockingAndTestDoubles/test_mock_basics.py::test_mock_returs_configured_value PASSED [ 75%]
Lab06-MockingAndTestDoubles/test_mock_basics.py::test_mock_accepts_any_call PASSED [ 87%]
Lab06-MockingAndTestDoubles/test_mock_basics.py::test_mock_attributes PASSED [100%]

============================== 8 passed in 0.28s ==============================
```
