# Roman Numeral Converter & Automated Unit Testing

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

This directory contains a complete, bidirectional Roman numeral conversion utility written in Python, along with a comprehensive automated test suite built with `pytest`. 

The project demonstrates:
- Implementing strict business domain rules and grammar validation for Roman numerals
- Bidirectional conversion between Roman numerals and decimal integers (`roman_to_integer` and `integer_to_roman`)
- Round-trip canonical validation
- Parameterized testing with `@pytest.mark.parametrize`
- Thorough negative testing and exception handling (`pytest.raises(ValueError)`)

---

## Directory Structure

```text
RomanConversion/
├── roman.py              # Bidirectional conversion logic & interactive CLI
├── test_roman.py         # Automated test suite using pytest parametrization
└── README.md             # Project documentation
```

---

## Conversion & Validation Rules

The converter strictly enforces standard classical Roman notation for values between **1 and 3999**:

1. **Base Numeral Mapping:**
   | Symbol | Value | Category |
   |:---:|:---:|:---:|
   | `I` | 1 | 10-based |
   | `V` | 5 | 5-based |
   | `X` | 10 | 10-based |
   | `L` | 50 | 5-based |
   | `C` | 100 | 10-based |
   | `D` | 500 | 5-based |
   | `M` | 1000 | 10-based |

2. **Character Validity & Case-Insensitivity:**
   - Automatically converts input to uppercase (`roman.upper()`).
   - Rejects empty strings (`""`) and non-Roman characters (e.g., `"ABC"`).

3. **Repetition Rules:**
   - **5-based numerals (`V`, `L`, `D`) can never be repeated.** Sequences like `VV`, `LL`, and `DD` raise `ValueError("V, L, and D cannot be repeated.")`.
   - **10-based numerals (`I`, `X`, `C`, `M`) cannot repeat more than 3 consecutive times.** Sequences like `IIII`, `XXXX`, `CCCC`, and `MMMM` raise `ValueError("A Roman numeral cannot repeat more than 3 times.")`.

4. **Subtractive Combinations:**
   - Only the following **6 standard subtractive pairs** are permitted:
     - `IV` (4), `IX` (9)
     - `XL` (40), `XC` (90)
     - `CD` (400), `CM` (900)
   - Any other smaller numeral preceding a larger numeral (e.g., `VX`, `IL`, `XDD`) raises `ValueError`.

5. **Canonical Form Check via Round-Trip Encoding:**
   - After computing the decimal total, the converter re-encodes the integer back to Roman notation via `integer_to_roman(total)`.
   - If `integer_to_roman(total) != roman`, the input represents a non-standard or out-of-order sequence (e.g., `IIV`, `IIX`, `CMCC`, `MCMC`) and is rejected with `ValueError("Invalid Roman numeral format.")`.

6. **Range Boundary:**
   - Values must fall within the range `1 <= total <= 3999`.

---

## Test Suite Architecture (`test_roman.py`)

The test suite uses `pytest` parameterized tests to verify dozens of scenarios efficiently:

### 1. Happy-Path Parameterized Tests (`test_roman_to_integer`)
Tests valid Roman numeral conversions covering single digits, subtractive forms, multi-symbol numbers, and boundary values:
- `I` $\rightarrow$ `1` (minimum boundary)
- `IV` $\rightarrow$ `4` (subtractive pair)
- `VI` $\rightarrow$ `6` (additive pair)
- `IX` $\rightarrow$ `9` (subtractive pair)
- `XVI` $\rightarrow$ `16`
- `MD` $\rightarrow$ `1500`
- `MMMCMXCIX` $\rightarrow$ `3999` (maximum boundary)

### 2. Case-Insensitivity (`test_roman_to_integer_accepts_lowercase`)
Verifies that lowercase inputs such as `"mmxxvi"` are parsed correctly into integer `2026`.

### 3. Negative Testing & Exception Handling (`test_invalid_roman`)
Uses `@pytest.mark.parametrize` to confirm that all invalid input variations raise `ValueError`:
- **Empty strings:** `""`
- **Illegal repetitions (>3 times):** `"IIII"`, `"XXXX"`, `"CCCC"`, `"MMMM"`
- **Illegal duplicates of 5-based numerals:** `"VV"`, `"LL"`, `"DD"`
- **Illegal characters:** `"ABC"`
- **Double subtractions:** `"IIV"`, `"IIX"`
- **Illegal subtractive pairs:** `"VX"`, `"XDD"`
- **Non-canonical combinations:** `"CMCC"`, `"MCMC"`
- **Out of range (> 3999):** `"MMMMCMXCIX"`

---

## How to Run

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running the Interactive CLI Program
Execute `roman.py` directly to run the command-line converter:
```bash
python RomanConversion/roman.py
```

**Interactive CLI Example:**
```text
Enter a Roman numeral: XIV
Integer: 14
Do you want to continue? (yes/no): yes
Enter a Roman numeral: mmxxvi
Integer: 2026
Do you want to continue? (yes/no): yes
Enter a Roman numeral: IIII
Invalid input: A Roman numeral cannot repeat more than 3 times.
Do you want to continue? (yes/no): no
Goodbye!
```

### Running Unit Tests
Run the test suite using `pytest`:
```bash
# Run tests with verbose output
python -m pytest RomanConversion/test_roman.py -v
```
