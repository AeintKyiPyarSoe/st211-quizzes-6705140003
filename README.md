# 192-211 Automated Software Testing

**Student:** Aeint Kyi Pyar Soe  
**Student ID:** 6705140003  
**Program:** Bachelor of Science in Information Technology (BSc IT), 3rd Year  
**Institution:** Siam University  
**Repository:** [st211-quizzes-6705140003](https://github.com/AeintKyiPyarSoe/st211-quizzes-6705140003)  

---

## Overview

This repository contains the laboratory exercises, assignments, and test suites completed for the **192-211 Automated Software Testing** course. The codebase focuses on practical automated testing using Python and the `pytest` framework, demonstrating modern software verification methodologies, test design techniques, boundary value analysis, test isolation, and parameterized testing.

---

## Repository Structure

```text
st211-quizzes-6705140003/
├── Lab01-TestingFundamentals/           # Lab 01: Core testing basics & AAA pattern
│   ├── AAA-pattern-calculator/          # Arrange-Act-Assert demonstration
│   ├── calculator/                      # Unit testing basic arithmetic functions
│   ├── failing-test/                    # Failure inspection & regex error matching
│   ├── test_first.py                    # Introductory assertions (math, strings, lists)
│   ├── test_with_print.py               # Assertion verification with print statements
│   └── README.md                        # Lab 01 detailed documentation
│
├── Lab02-EffectiveTestCases/            # Lab 02: Test design, isolation & boundary analysis
│   ├── bad-test/                        # "Fat test" anti-pattern demonstration
│   ├── clear-AAA-test/                  # Refactored single-responsibility test
│   ├── dependent-independent-tests/     # Shared state anti-pattern vs. test isolation
│   ├── descriptive-test-names/          # Intention-revealing test naming conventions
│   ├── edge-cases-and-boundary-values/  # Boundary Value Analysis (BVA) on grading logic
│   ├── postive-negative-testing/        # Positive and negative validation testing
│   └── README.md                        # Lab 02 detailed documentation
│
├── Lab03-Assertions-Organizations/      # Lab 03: Advanced assertions, organization & configuration
│   ├── assertion-types/                 # Collection assertions & float precision (approx)
│   ├── configuration-with-pytest.ini/   # pytest.ini configuration & strict marker validation
│   ├── custom-markers/                  # Custom markers (smoke, slow, regression) & -m filters
│   ├── organizing-tests-in-classes/     # Grouping tests under TestShoppingCart classes
│   ├── skipping-and-expected-failures/  # Skip (unconditional/conditional) & xfail/xpass
│   └── README.md                        # Lab 03 detailed documentation
│
├── RomanConversion/                     # Roman Numeral Converter & Test Suite
│   ├── roman.py                         # Bidirectional converter & interactive CLI
│   ├── test_roman.py                    # Parameterized unit & negative test suite
│   └── README.md                        # Roman conversion detailed documentation
│
└── README.md                            # Main repository documentation
```

---

## Modules & Lab Summaries

| Module | Directory | Key Topics & Concepts | Detailed Guide |
|---|---|---|:---:|
| **Lab 01** | [`Lab01-TestingFundamentals/`](./Lab01-TestingFundamentals/) | Testing fundamentals, Pytest discovery, AAA pattern, basic assertions, exception assertions (`pytest.raises`) | [View README](./Lab01-TestingFundamentals/README.md) |
| **Lab 02** | [`Lab02-EffectiveTestCases/`](./Lab02-EffectiveTestCases/) | "Fat test" anti-patterns, test independence vs. shared state, descriptive test naming, Boundary Value Analysis (BVA), positive & negative testing | [View README](./Lab02-EffectiveTestCases/README.md) |
| **Lab 03** | [`Lab03-Assertions-Organizations/`](./Lab03-Assertions-Organizations/) | Deep collection comparisons, IEEE 754 float precision, class-based tests, custom markers, skipping & xfail, `pytest.ini` configuration | [View README](./Lab03-Assertions-Organizations/README.md) |
| **Roman Converter** | [`RomanConversion/`](./RomanConversion/) | Bidirectional Roman-to-Integer converter, classical grammar rules, round-trip canonical validation, `@pytest.mark.parametrize` suite | [View README](./RomanConversion/README.md) |

---

## Summary of Testing Principles & Techniques

1. **Arrange-Act-Assert (AAA) Pattern:** Standardizing unit test layout across three distinct phases: setting up data (Arrange), executing the action under test (Act), and verifying the outcome (Assert).
2. **Test Independence & Isolation:** Preventing tests from sharing mutable state (e.g., global object instances). Each test instantiates fresh dependencies to ensure determinism and arbitrary execution order.
3. **Descriptive Test Naming:** Structuring test names according to the `test_<action>_<condition>_<expected_result>` pattern so test results serve as living specifications.
4. **Boundary Value Analysis (BVA):** Focusing test cases on partition boundaries (e.g., minimum valid, maximum valid, just-above, just-below, and out-of-range thresholds) where defects most frequently occur.
5. **Positive & Negative Testing:** Validating both the happy path (valid inputs) and error handling paths (raising expected exceptions such as `ValueError` and `TypeError`).
6. **Floating-Point Arithmetic Verification:** Utilizing `pytest.approx()` to prevent false failures caused by IEEE 754 binary floating-point representation limits (`0.1 + 0.2 != 0.3`).
7. **Class-Based Organization:** Organizing related test functions inside `Test*` classes without constructors to namespace test suites and enable clean reporting.
8. **Parameterized Testing:** Leveraging `@pytest.mark.parametrize` to execute identical assertion logic against diverse datasets, boundary conditions, and invalid inputs without duplicating test code.

---

## Prerequisites & Installation

### Environment Requirements
- **Python:** Version 3.8 or higher
- **Pytest:** Version 7.0 or higher

### Installing Dependencies
Ensure `pytest` is installed in your Python environment:
```bash
pip install pytest
```

---

## How to Run Tests

### Running All Tests Across the Repository
From the root of the repository:
```bash
# Run all tests
python -m pytest -v

# Run all tests with standard print output enabled
python -m pytest -v -s
```

### Running Tests by Lab / Directory
```bash
# 1. Run Lab 01 (Testing Fundamentals)
python -m pytest Lab01-TestingFundamentals -v

# 2. Run Lab 02 (Effective Test Cases)
python -m pytest Lab02-EffectiveTestCases -v

# 3. Run Lab 03 (Assertions, Organizations & Configuration)
python -m pytest Lab03-Assertions-Organizations -v

# 4. Run Roman Numeral Converter Tests
python -m pytest RomanConversion/test_roman.py -v
```

### Running Interactive Programs
```bash
# Run Roman Numeral Converter CLI
python RomanConversion/roman.py

# Run Grade Classifier Demo
python Lab02-EffectiveTestCases/edge-cases-and-boundary-values/grades.py

# Run Bank Account Demo
python Lab02-EffectiveTestCases/bad-test/bank.py
```
