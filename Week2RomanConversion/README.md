# Week 2: Roman Numeral Conversion & Unit Testing

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  

---

## Overview

This project implements a Roman numeral converter and validator in Python. It includes logic to convert Roman numerals to decimal integers (`roman_to_integer`) and back (`integer_to_roman`), accompanied by an automated unit test suite using `pytest`.

## Features & Validation Rules

The converter strictly validates Roman numerals according to standard classical Roman notation (numbers 1 to 3999):

1. **Character Validity:** Accepts standard Roman numeral symbols (`I`, `V`, `X`, `L`, `C`, `D`, `M`) and handles case-insensitivity.
2. **Repetition Rules:**
   - `V`, `L`, and `D` (5-based values) can never be repeated (e.g., `VV` is invalid).
   - `I`, `X`, `C`, and `M` can never be repeated more than 3 consecutive times (e.g., `IIII` is invalid).
3. **Subtractive Combinations:** Only the 6 standard subtractive pairs are allowed:
   - `IV` (4), `IX` (9)
   - `XL` (40), `XC` (90)
   - `CD` (400), `CM` (900)
4. **Canonical Form Check:** Re-encodes computed integers back to Roman notation to reject non-canonical / invalid sequences such as `IIV`, `IIX`, `CMCC`, or `MCMC`.
5. **Range Constraints:** Supports values between 1 and 3999 inclusive.

---

## Project Structure

```text
Week2RomanConversion/
├── roman.py          # Main implementation & interactive CLI loop
├── test_roman.py     # Automated unit tests using pytest
└── README.md         # Documentation
```

---

## How to Run

### Prerequisites

- Python 3.8+
- `pytest` (for running tests)

Install pytest if not already installed:
```bash
pip install pytest
```

### Running the Interactive Program

Run `roman.py` directly to enter Roman numerals in the command line:

```bash
python roman.py
```

**Example Usage:**
```text
Enter a Roman numeral: XIV
Integer: 14
Do you want to continue? (yes/no): yes
Enter a Roman numeral: mmxxvi
Integer: 2026
Do you want to continue? (yes/no): no
Goodbye!
```

---

## Running Unit Tests

Run the automated test suite with `pytest`:

```bash
# Using pytest directly
pytest test_roman.py -v

# Or via Python module
python -m pytest test_roman.py -v
```

The test suite covers:
- Standard conversions and boundary values (e.g., `I` = 1, `MMMCMXCIX` = 3999).
- Lowercase input handling (e.g., `mmxxvi` = 2026).
- Negative testing and exception handling (`ValueError`) for empty inputs, invalid characters, illegal repetitions, invalid subtractive pairs, and non-canonical strings.
