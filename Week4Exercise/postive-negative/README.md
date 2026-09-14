# Positive & Negative Testing: Input Validation

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  

---

## Overview

This module demonstrates the principles of **Positive Testing** (verifying expected behavior with valid inputs) and **Negative Testing** (verifying graceful error handling and exception raising with invalid/malformed inputs).

---

## Implementation & Test Suite

### 1. `validators.py`
Provides input validation functions:
- `validate_email(email)`: Uses regular expressions to ensure standard email format (`user@domain.tld`). Raises a `ValueError` for malformed email addresses.
- `validate_age(age)`: Checks that age is an integer and within the valid domain `[0, 150]`. Raises `TypeError` for non-integer inputs and `ValueError` for out-of-range values.

### 2. `test_positive.py` (Happy Path Testing)
Validates that legitimate, conforming inputs succeed and return `True`:
- `test_valid_email_accepted`: Standard email format (`student@siam.edu`).
- `test_valid_email_with_subdomain`: Email with subdomains (`user@mail.example.com`).
- `test_valid_age_accepted`: Typical valid age (`25`).
- `test_boundary_ages_accepted`: Minimum (`0`) and maximum (`150`) valid boundary ages.

### 3. `test_negative.py` (Unhappy Path & Exception Testing)
Validates that invalid inputs trigger the expected exceptions using `pytest.raises`:
- `test_email_without_at_rejected`: Missing `@` raises `ValueError`.
- `test_email_without_domain_rejected`: Missing domain name (`user@.com`) raises `ValueError`.
- `test_negative_age_rejected`: Negative age (`-5`) raises `ValueError`.
- `test_age_as_string_rejected`: String passed instead of integer (`"twenty-five"`) raises `TypeError`.

---

## How to Run

Run both positive and negative test suites:
```bash
python -m pytest test_positive.py test_negative.py -v
```
