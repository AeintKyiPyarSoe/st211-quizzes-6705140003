# Return Values vs. Side Effects

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [mock-objects-and-return-values](../README.md)

---

## Overview

When mocking methods on Python's `unittest.mock.Mock` objects, developers have two distinct mechanisms to specify what happens when the mock method is invoked:
- **`return_value`**: Pre-configures a fixed static value returned on every single invocation.
- **`side_effect`**: Configures dynamic behavior, such as yielding a sequence of different values on successive calls, invoking an alternate callback function, or raising an exception.

This submodule demonstrates the concrete differences and use cases for both mechanisms.

---

## Files in this Directory

| File | Description |
|---|---|
| [`username.py`](./username.py) | Contains `UserService` which queries `self.database.find_user(user_id)` to retrieve user display names. |
| [`test_get_username.py`](./test_get_username.py) | Demonstrates configuring static return values with `db.find_user.return_value = "Alice"`. |
| [`test_return_values.py`](./test_return_values.py) | Demonstrates configuring successive sequential return values using `mock.next_id.side_effect = [1, 2, 3]`. |

---

## Technical Deep Dive

### 1. Static Configuration with `return_value` (`test_get_username.py`)

#### Service Implementation (`username.py`):
```python
class UserService:  
    def __init__(self, database):        
        self.database = database  
          
    def get_username(self, user_id):        
        return self.database.find_user(user_id)
```

#### Unit Test (`test_get_username.py`):
```python
from unittest.mock import Mock
from username import UserService

def test_get_username():
    # 1. Create mock database
    db = Mock()
    # 2. Configure return_value for find_user
    db.find_user.return_value = "Alice"

    # 3. Inject mock into service
    service = UserService(db)

    # 4. Assert service returns the mock's configured return value
    assert service.get_username(1) == "Alice"
```

No matter how many times or with what arguments `db.find_user(...)` is called, it will consistently return `"Alice"`.

---

### 2. Sequential Multi-Value Iteration with `side_effect` (`test_return_values.py`)

#### Unit Test (`test_return_values.py`):
```python
from unittest.mock import Mock

def test_multiple_return_values():
    mock = Mock()
    mock.next_id.side_effect = [1, 2, 3]
    
    assert mock.next_id() == 1  # 1st call returns first item
    assert mock.next_id() == 2  # 2nd call returns second item
    assert mock.next_id() == 3  # 3rd call returns third item
```

When an iterable (such as a list, tuple, or generator) is assigned to `.side_effect`:
- Each call to the mock method yields the next element in the collection.
- This is invaluable for simulating stateful sequences—such as auto-incrementing database primary keys, polling status changes (`["pending", "processing", "completed"]`), or paginated API results.
- If the mock is called after the iterable is exhausted, Python raises a `StopIteration` exception.

---

### 3. Comparison Matrix

| Property | `return_value` | `side_effect` |
|---|---|---|
| **Value Repeated?** | Yes, identical value returned on every call. | No, advances through iterable sequence or executes callback. |
| **Exception Simulation** | Cannot raise exceptions (would return the exception object itself). | Yes, setting `mock.method.side_effect = ValueError(...)` raises the error upon invocation. |
| **Callable Execution** | Returns the function object without running it. | Executes the custom function and returns its output: `mock.method.side_effect = custom_fn`. |
| **Primary Use Cases** | Fixed stubs, query lookups, constant config data. | Multi-call workflows, sequential ID generators, retry loops, error simulations. |

---

## How to Run the Tests

From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles/mock-objects-and-return-values/return_value-vs-side_effect -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
collecting ... collected 2 items

Lab06-MockingAndTestDoubles/mock-objects-and-return-values/return_value-vs-side_effect/test_get_username.py::test_get_username PASSED [ 50%]
Lab06-MockingAndTestDoubles/mock-objects-and-return-values/return_value-vs-side_effect/test_return_values.py::test_multiple_return_values PASSED [100%]

============================== 2 passed in 0.05s ==============================
```
