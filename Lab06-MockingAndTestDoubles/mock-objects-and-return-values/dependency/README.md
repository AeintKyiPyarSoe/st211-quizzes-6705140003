# Dependency Injection with Mocks

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [mock-objects-and-return-values](../README.md)

---

## Overview

In real-world software architecture, components frequently interact with critical external systems, such as third-party payment gateways (Stripe, PayPal), relational databases, or message queues.

Testing these components directly against production dependencies introduces severe hazards:
1. **Real-World Side Effects:** Accidentally charging real credit cards or polluting production databases.
2. **Infrastructure Requirements:** Requiring live network connections and active API credentials during local development and CI runs.
3. **Flakiness & Latency:** Network latency, downtime, or rate-limiting destabilize the test suite.

**Dependency Injection (DI)** solves this architectural challenge. By supplying collaborators into a class through its constructor rather than hardcoding them, tests can effortlessly supply simulated **Test Doubles** (Mocks) in place of real implementations.

---

## Files in this Directory

| File | Description |
|---|---|
| [`payment.py`](./payment.py) | Defines the `PaymentGateway` interface (which raises `NotImplementedError`) and the `OrderProcessor` service under test. |
| [`test_payment.py`](./test_payment.py) | Unit test suite verifying `OrderProcessor` by injecting a mocked payment gateway. |

---

## Technical Analysis

### 1. The Domain Model (`payment.py`)

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

- `PaymentGateway`: Represents an external interface. Calling `charge()` directly raises `NotImplementedError`, reflecting an unavailable real-world system during unit testing.
- `OrderProcessor`: Depends on a gateway instance passed in via `__init__(self, gateway)`. It validates input (`amount > 0`), delegates charging to `self.gateway.charge(amount)`, and formats the final confirmation string.

---

### 2. The Test Implementation (`test_payment.py`)

```python
from unittest.mock import Mock
from payment import OrderProcessor

def test_order_processing():
    # 1. Arrange: Create a mock payment gateway and define expected return value
    fake_gateway = Mock()
    fake_gateway.charge.return_value = "SUCCESS-12345"
    
    # 2. Inject the mock into the OrderProcessor constructor
    processor = OrderProcessor(fake_gateway)
    
    # 3. Act: Process an order
    result = processor.process(100)
    
    # 4. Assert: Verify the transaction ID is correctly incorporated into the output
    assert result == "Order processed: SUCCESS-12345"
```

#### Why this Pattern is Superior:
1. **Zero Monkey-Patching Needed:** Because `OrderProcessor` accepts its dependency through DI, we do not need `unittest.mock.patch`. We simply pass `fake_gateway` as a regular argument.
2. **Deterministic Outcomes:** We precisely dictate that `charge(100)` returns `"SUCCESS-12345"`.
3. **Safe Execution:** No network calls or real payment transactions take place.

---

## How to Run the Tests

From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles/mock-objects-and-return-values/dependency/test_payment.py -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
collecting ... collected 1 item

Lab06-MockingAndTestDoubles/mock-objects-and-return-values/dependency/test_payment.py::test_order_processing PASSED [100%]

============================== 1 passed in 0.05s ==============================
```
