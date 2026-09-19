# Positive and Negative Testing

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab02-EffectiveTestCases](../README.md)

---

## Overview

This subfolder demonstrates **Positive and Negative Testing Methodologies**. A well-architected test suite does not only verify that a program produces the correct output when fed ideal data; it must equally verify that the program detects invalid inputs and rejects them gracefully with appropriate error types.

- **Positive Testing (Happy Path):** Validates that the system functions correctly when provided valid, well-formed input.
- **Negative Testing (Error Path):** Validates that the system responds predictably, raising expected exceptions (e.g., `ValueError`, `TypeError`), when provided malformed, out-of-range, or unexpected input.

---

## Files in this Directory

| File | Description |
|---|---|
| [`validators.py`](./validators.py) | Input validation functions: `validate_email(email)` using regex and `validate_age(age)` with type and range checking. |
| [`test_positive.py`](./test_positive.py) | Suite of positive test cases checking standard valid emails, subdomain emails, normal ages, and boundary ages. |
| [`test_negative.py`](./test_negative.py) | Suite of negative test cases verifying that invalid emails, negative ages, and incorrect data types trigger expected exceptions. |

---

## Implementation Details

### Domain Logic (`validators.py`)
```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email address: {email}")
    return True

def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer.")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150.")
    return True
```

---

## Positive Tests (`test_positive.py`)

Verifies that valid data returns `True` without raising errors:

```python
from validators import validate_email, validate_age

def test_valid_email_accepted():
    assert validate_email("student@siam.edu") is True

def test_valid_email_with_subdomain():
    assert validate_email("user@mail.example.com") is True

def test_valid_age_accepted():
    assert validate_age(25) is True

def test_boundary_ages_accepted():
    assert validate_age(0) is True    # Valid minimum boundary
    assert validate_age(150) is True  # Valid maximum boundary
```

---

## Negative Tests (`test_negative.py`)

Verifies error handling using `pytest.raises`:

```python
import pytest
from validators import validate_email, validate_age

def test_email_without_at_rejected():
    with pytest.raises(ValueError):
        validate_email("invalidemail.com")

def test_email_without_domain_rejected():
    with pytest.raises(ValueError):
        validate_email("user@.com")

def test_negative_age_rejected():
    with pytest.raises(ValueError):
        validate_age(-5)

def test_age_as_string_rejected():
    with pytest.raises(TypeError):
        validate_age("twenty-five")
```

---

## Comparison Summary

| Aspect | Positive Testing (`test_positive.py`) | Negative Testing (`test_negative.py`) |
|---|---|---|
| **Goal** | Ensure feature works as intended | Ensure system fails safely and predictably |
| **Input Type** | Valid, anticipated, boundary inputs | Malformed, unexpected, illegal inputs |
| **Assertion Style** | `assert result is True` | `with pytest.raises(ExpectedException):` |
| **Exceptions Checked** | None (no exceptions should occur) | `ValueError`, `TypeError` |

---

## How to Run the Tests

### From the Repository Root:
```bash
# Run both positive and negative suites
python -m pytest Lab02-EffectiveTestCases/postive-negative-testing -v

# Run only positive tests
python -m pytest Lab02-EffectiveTestCases/postive-negative-testing/test_positive.py -v

# Run only negative tests
python -m pytest Lab02-EffectiveTestCases/postive-negative-testing/test_negative.py -v
```

### Expected Output:
```text
test_negative.py::test_email_without_at_rejected PASSED
test_negative.py::test_email_without_domain_rejected PASSED
test_negative.py::test_negative_age_rejected PASSED
test_negative.py::test_age_as_string_rejected PASSED
test_positive.py::test_valid_email_accepted PASSED
test_positive.py::test_valid_email_with_subdomain PASSED
test_positive.py::test_valid_age_accepted PASSED
test_positive.py::test_boundary_ages_accepted PASSED
```
