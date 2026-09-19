# Lab 01: Testing Fundamentals in Python with Pytest

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

This directory contains the laboratory exercises for **Lab 01: Testing Fundamentals**. The primary objective of this lab is to establish a solid foundation in automated software testing using Python and the `pytest` framework. 

Key testing fundamentals introduced in this lab include:
- Understanding basic assertions (`assert`)
- Writing simple, discoverable test functions
- The **Arrange-Act-Assert (AAA)** pattern
- Observing test execution output and print statements
- Testing exception handling and failure conditions using `pytest.raises`

---

## Directory Structure

```text
Lab01-TestingFundamentals/
├── AAA-pattern-calculator/
│   ├── calculator.py            # Basic arithmetic operations (add, divide)
│   └── test_aaa_calculator.py   # Unit tests explicitly following the AAA pattern
├── calculator/
│   ├── calculator.py            # Arithmetic operations with zero-division handling
│   └── test_calculator.py       # Basic test cases for addition and division
├── failing-test/
│   ├── calculator.py            # Arithmetic operations raising ValueError on zero division
│   └── test_raise_error.py      # Exception testing with pytest.raises and regex matching
├── test_first.py                # Introductory tests (arithmetic, strings, lists)
├── test_with_print.py           # Testing assertions alongside standard output
└── README.md                    # Lab 01 documentation
```

---

## Exercises & Core Concepts

### 1. Introductory Tests (`test_first.py`)
Demonstrates how `pytest` automatically discovers and executes functions prefixed with `test_`:
- **Arithmetic Assertions:** Verifies numerical equality (`assert 1 + 1 == 2`).
- **String Manipulations:** Asserts string methods return expected transformations (`assert "hello".upper() == "HELLO"`).
- **Collection Inspection:** Tests list lengths using Python's built-in `len()` (`assert len(fruits) == 3`).

### 2. Output and Assertions (`test_with_print.py`)
Demonstrates how `pytest` handles standard output during test execution:
- By default, `pytest` captures stdout and only displays `print()` statements if a test fails.
- Passing the `-s` (or `--capture=no`) flag allows print output to be visible in the console during execution.

### 3. The AAA Pattern (`AAA-pattern-calculator/`)
The **Arrange-Act-Assert (AAA)** pattern is a universal standard for structuring clean, readable unit tests:
1. **Arrange:** Set up all test preconditions, inputs, and test data.
2. **Act:** Invoke the target function or method under test.
3. **Assert:** Verify that the returned value matches the expected outcome.

**Example from `test_aaa_calculator.py`:**
```python
from calculator import add

def test_add():
    # Arrange: set up the data for the test
    a, b = 2, 3

    # Act: call the function being tested
    result = add(a, b)

    # Assert: check that the result is as expected
    assert result == 5
```

### 4. Basic Function Testing (`calculator/`)
Tests standard mathematical operations across multiple input scenarios:
- Verifying positive addition, negative addition, and identity operations (`add(0, 0)`).
- Verifying basic division logic (`divide(10, 2) == 5`).

### 5. Exception Testing & Failure Analysis (`failing-test/`)
Automated tests must verify not only that code works under valid conditions, but also that it fails gracefully and predictably when supplied invalid inputs.
- **Exception Verification:** `pytest.raises(ValueError)` asserts that invalid operations (e.g., dividing by zero) raise the expected exception type.
- **Error Message Matching:** `pytest.raises(ValueError, match="...")` validates that the raised exception message matches a specific regular expression.
- **Failure Traceback Demonstration:** In `test_raise_error.py`, `test_divide_by_zero_raises_with_message` intentionally checks for `"Cannot be divided by zero"` against the implementation's `"Cannot divide by zero"`, demonstrating how `pytest` clearly highlights mismatches between expected and actual error messages.

---

## How to Run Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running All Lab 01 Tests
From the repository root:
```bash
# Using pytest
pytest Lab01-TestingFundamentals -v

# Or using the Python launcher
python -m pytest Lab01-TestingFundamentals -v
```

### Running Specific Tests
```bash
# Run first tests
python -m pytest Lab01-TestingFundamentals/test_first.py -v

# Run with print statements displayed (-s flag)
python -m pytest Lab01-TestingFundamentals/test_with_print.py -v -s

# Run AAA pattern calculator tests
python -m pytest Lab01-TestingFundamentals/AAA-pattern-calculator -v

# Run exception and failure tests
python -m pytest Lab01-TestingFundamentals/failing-test -v
```
