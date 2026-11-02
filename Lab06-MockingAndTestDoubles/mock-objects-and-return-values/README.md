# Mock Objects and Return Values

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab06-MockingAndTestDoubles](../README.md)

---

## Overview

In unit testing, units under test frequently depend on other software components—such as database repositories, payment gateways, authentication providers, or remote services. If we test with live implementations of these collaborators, our tests become slow, fragile, state-dependent, and prone to unintended side effects.

Python's `unittest.mock.Mock` class solves this by providing simulated **Test Doubles** that mimic the behavior of real objects. A `Mock` object can:
1. **Imitate Any Interface Dynamically:** Accessing any attribute or method on a mock automatically generates a new child `Mock`, eliminating `AttributeError`.
2. **Pre-program Return Values:** Return values can be configured statically (`return_value`) or dynamically across invocations (`side_effect`).
3. **Facilitate Dependency Injection:** Mocks can be passed directly into dependent classes during instantiation, cleanly decoupling business logic from infrastructure.

---

## Directory Structure

```text
mock-objects-and-return-values/
├── dependency/
│   ├── payment.py                      # Domain model: PaymentGateway interface & OrderProcessor
│   ├── test_payment.py                 # Dependency injection test using Mock gateway
│   └── README.md                       # Submodule guide on dependency injection with mocks
│
├── return_value-vs-side_effect/
│   ├── username.py                     # UserService domain class with database dependency
│   ├── test_get_username.py            # Single return value configuration via return_value
│   ├── test_return_values.py           # Sequential return values configuration via side_effect
│   └── README.md                       # Submodule guide on return_value vs side_effect
│
├── test_mock_basics.py                 # Core Mock object mechanics & dynamic attributes
└── README.md                           # Mock objects and return values comprehensive guide
```

---

## Files in this Directory

| File / Subfolder | Description |
|---|---|
| [`test_mock_basics.py`](./test_mock_basics.py) | Unit tests demonstrating core `Mock` instantiation, `.return_value` configuration, arbitrary method call acceptance, and attribute storage. |
| [`dependency/`](./dependency/) | Subfolder showcasing **Dependency Injection**, passing a mock `PaymentGateway` into `OrderProcessor` to verify business rules without contacting a live payment provider. |
| [`return_value-vs-side_effect/`](./return_value-vs-side_effect/) | Subfolder comparing static return values (`return_value`) against sequential multi-value responses (`side_effect = [1, 2, 3]`). |

---

## Technical Deep Dive

### 1. Core Mock Object Mechanics (`test_mock_basics.py`)

The `Mock` class dynamically creates attributes and callable methods on demand:

```python
from unittest.mock import Mock

def test_mock_returs_configured_value():
    mock = Mock()
    mock.get_data.return_value = "fake data"
    assert mock.get_data() == "fake data"

def test_mock_accepts_any_call():
    mock = Mock()
    mock.anything()       # Automatically creates 'anything' method
    mock.whatever(1, 2, 3) # Accepts any arguments without error

def test_mock_attributes():
    mock = Mock()
    mock.name = "TestUser"
    assert mock.name == "TestUser"
```

#### Key Mechanisms:
- **`mock.get_data.return_value = "fake data"`:** Configures what the callable returns upon invocation.
- **Dynamic Attribute Creation:** Accessing `mock.anything` or `mock.whatever` returns a child `Mock`. It will accept any arguments (`*args`, `**kwargs`) without raising errors.
- **Attribute Assignment:** Arbitrary properties (`mock.name = "TestUser"`) can be attached and read back, making mocks suitable as lightweight data containers (stubs/dummies).

---

### 2. Dependency Injection with Mocks (`dependency/`)

When a class accepts its collaborators through its constructor (`__init__`), it follows the **Dependency Injection (DI)** design pattern. This allows tests to substitute mock collaborators effortlessly without monkey-patching.

#### Domain Model (`dependency/payment.py`):
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

#### Test with Injected Mock (`dependency/test_payment.py`):
```python
from unittest.mock import Mock
from payment import OrderProcessor

def test_order_processing():
    fake_gateway = Mock()
    fake_gateway.charge.return_value = "SUCCESS-12345"
    
    processor = OrderProcessor(fake_gateway)
    result = processor.process(100)
    
    assert result == "Order processed: SUCCESS-12345"
```

Because `OrderProcessor` operates against the interface rather than a hardcoded gateway class, injecting `fake_gateway` allows us to verify order processing safely in complete isolation.

---

### 3. `return_value` vs `side_effect` (`return_value-vs-side_effect/`)

In `unittest.mock`, controlling what a mock call produces is achieved through two primary attributes: `return_value` and `side_effect`.

| Feature | `return_value` | `side_effect` |
|---|---|---|
| **Behavior** | Returns the exact same canned value on **every** invocation. | Executes dynamic behavior: yields sequential items from an iterable, invokes a custom function, or raises an exception. |
| **Typical Use Case** | Fixed stub data (e.g., username, fixed temperature, status code). | Simulating sequences (e.g., auto-incrementing IDs, polling retry attempts), or testing error handling (raising exceptions). |
| **Example** | `mock.find_user.return_value = "Alice"` | `mock.next_id.side_effect = [1, 2, 3]` |

#### Example 1: Static Return Value (`test_get_username.py`)
```python
from unittest.mock import Mock
from username import UserService

def test_get_username():
    db = Mock()
    db.find_user.return_value = "Alice"

    service = UserService(db)
    assert service.get_username(1) == "Alice"
```

#### Example 2: Sequential Values with `side_effect` (`test_return_values.py`)
```python
from unittest.mock import Mock

def test_multiple_return_values():
    mock = Mock()
    mock.next_id.side_effect = [1, 2, 3]
    assert mock.next_id() == 1
    assert mock.next_id() == 2
    assert mock.next_id() == 3
```
Each call to `mock.next_id()` advances to the next element in the iterable list until exhausted.

---

## How to Run the Tests

### Running All Tests in this Subdirectory:
From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles/mock-objects-and-return-values -v
```

### Running Individual Test Suites:
```bash
# 1. Run core mock mechanics tests
python -m pytest Lab06-MockingAndTestDoubles/mock-objects-and-return-values/test_mock_basics.py -v

# 2. Run dependency injection tests
python -m pytest Lab06-MockingAndTestDoubles/mock-objects-and-return-values/dependency/test_payment.py -v

# 3. Run return_value and side_effect tests
python -m pytest Lab06-MockingAndTestDoubles/mock-objects-and-return-values/return_value-vs-side_effect -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
collecting ... collected 6 items

Lab06-MockingAndTestDoubles/mock-objects-and-return-values/dependency/test_payment.py::test_order_processing PASSED [ 16%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/return_value-vs-side_effect/test_get_username.py::test_get_username PASSED [ 33%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/return_value-vs-side_effect/test_return_values.py::test_multiple_return_values PASSED [ 50%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/test_mock_basics.py::test_mock_returs_configured_value PASSED [ 66%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/test_mock_basics.py::test_mock_accepts_any_call PASSED [ 83%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/test_mock_basics.py::test_mock_attributes PASSED [100%]

============================== 6 passed in 0.34s ==============================
```
