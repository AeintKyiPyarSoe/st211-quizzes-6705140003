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
├── Lab04-FixturesAndTestDataManagement/ # Lab 04: Fixtures & test data management
│   ├── factory-fixtures/                # Dynamic object generation & batch teardown
│   ├── fixture-scope/                   # Fixture lifecycles & sharing scopes
│   ├── fixtures/                        # Reusable test dependencies & dependency injection
│   ├── setup-and-teardown/              # Resource allocation & guaranteed cleanup
│   ├── sharing-fixtures-with-conftest.py/ # Global directory-level fixture discovery
│   └── README.md                        # Lab 04 detailed documentation
│
├── Lab05-Parametrization/               # Lab 05: Parameterized testing & data-driven tests
│   ├── basic-parameterization/          # Single & paired @pytest.mark.parametrize
│   ├── data-driven-testing-from-external-files/ # CSV & JSON external data loaders
│   ├── multiple-parameters/            # Multi-argument & Cartesian product combinations
│   ├── parameter-ids-and-readability/   # Custom test IDs & per-parameter xfail marks
│   ├── parametrized-fixtures/           # Multi-environment fixtures via request.param
│   └── README.md                        # Lab 05 detailed documentation
│
├── Mock Lab/                            # Mock Lab: Test doubles & dependency isolation
│   ├── test_problem.py                  # Weak non-deterministic test anti-pattern
│   ├── test_solution.py                 # Deterministic testing with unittest.mock.patch
│   ├── weather.py                       # Random weather simulation domain model
│   └── README.md                        # Mock Lab detailed documentation
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
| **Lab 04** | [`Lab04-FixturesAndTestDataManagement/`](./Lab04-FixturesAndTestDataManagement/) | Pytest fixtures (`@pytest.fixture`), dependency injection, setup/teardown (`yield`), fixture scopes, global sharing (`conftest.py`), factory fixtures | [View README](./Lab04-FixturesAndTestDataManagement/README.md) |
| **Lab 05** | [`Lab05-Parametrization/`](./Lab05-Parametrization/) | Parameterized testing (`@pytest.mark.parametrize`), Cartesian products, custom parameter IDs, per-test xfail marks, parametrized fixtures, data-driven testing (JSON/CSV) | [View README](./Lab05-Parametrization/README.md) |
| **Mock Lab** | [`Mock Lab/`](./Mock%20Lab/) | Test doubles, deterministic testing with `unittest.mock.patch`, isolating random dependencies, 100% branch coverage | [View README](./Mock%20Lab/README.md) |
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
9. **Fixtures & Dependency Injection:** Centralizing test object creation and state management using `@pytest.fixture`, injecting fresh dependencies per test to eliminate Arrange duplication and ensure isolation.
10. **Test Doubles & Mocking:** Intercepting non-deterministic, slow, or volatile dependencies using `unittest.mock.patch` to guarantee reproducible test outcomes and complete branch coverage.
11. **External Data-Driven Testing (DDT):** Decoupling datasets from test code by loading external CSV and JSON data files dynamically at test collection time.

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

# 4. Run Lab 04 (Fixtures & Test Data Management)
python -m pytest Lab04-FixturesAndTestDataManagement/fixtures -v

# 5. Run Lab 05 (Parameterized Testing & Data-Driven Tests)
python -m pytest Lab05-Parametrization/basic-parameterization -v
python -m pytest Lab05-Parametrization/multiple-parameters -v
python -m pytest Lab05-Parametrization/parametrized-fixtures -v

# 6. Run Mock Lab (Deterministic Mocking with unittest.mock)
python -m pytest "Mock Lab" -v

# 7. Run Roman Numeral Converter Tests
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
