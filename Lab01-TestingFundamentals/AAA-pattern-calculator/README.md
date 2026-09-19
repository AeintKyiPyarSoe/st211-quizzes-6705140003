# AAA Pattern Calculator

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab01-TestingFundamentals](../README.md)

---

## Overview

This subfolder demonstrates the **Arrange-Act-Assert (AAA)** pattern, which is the industry-standard structure for writing clear, readable, and maintainable unit tests. 

By dividing every test case into three explicit, sequential phases, the AAA pattern ensures tests remain focused and self-explanatory:
1. **Arrange:** Set up test prerequisites, inputs, and environment.
2. **Act:** Execute the target function or method under test.
3. **Assert:** Verify that the actual output matches the expected outcome.

---

## Files in this Directory

| File | Description |
|---|---|
| [`calculator.py`](./calculator.py) | Mathematical utility module implementing `add(a, b)` and `divide(a, b)` with zero-division validation. |
| [`test_aaa_calculator.py`](./test_aaa_calculator.py) | Pytest test suite demonstrating explicit AAA phase separation using inline comments. |

---

## Code Demonstration

In [`test_aaa_calculator.py`](./test_aaa_calculator.py), the structure is visibly separated into the three steps:

```python
from calculator import add, divide

def test_add():
    # Arrange: set up the data for the test
    a, b = 2, 3

    # Act: call the function being tested
    result = add(a, b)

    # Assert: check that the result is as expected
    assert result == 5

def test_divide():
    # Arrange
    a, b = 10, 2

    # Act
    result = divide(a, b)

    # Assert
    assert result == 5
```

### Benefits of the AAA Pattern:
- **Clarity:** Anyone reading the test can immediately identify what data is being prepared, what operation is under test, and what condition determines success.
- **Maintainability:** Isolates changes—modifying inputs only touches the Arrange block; changes in API only touch the Act line.
- **Debugging Speed:** When a test fails on an assertion, the Arrange and Act steps make reproduction straightforward.

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab01-TestingFundamentals/AAA-pattern-calculator -v
```

### From within this Directory:
```bash
python -m pytest test_aaa_calculator.py -v
```

### Expected Output:
```text
test_aaa_calculator.py::test_add PASSED
test_aaa_calculator.py::test_divide PASSED
```
