# Lab 05: Parameterized Testing & Data-Driven Tests

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

This directory contains the laboratory exercises for **Lab 05: Parameterized Testing & Data-Driven Tests**. The core objective of this lab is to eliminate test code duplication, broaden test coverage, and improve test diagnostics by executing test assertions against wide ranges of input data and configurations using **Pytest Parameterization** and **Data-Driven Testing (DDT)**.

Rather than authoring separate test functions for each input variant—or burying assertions inside loops that abort upon the first failure—parameterization enables developers to write clean, declarative tests that Pytest multiplies into distinct, isolated test items.

### Key Learning Objectives
1. **Basic Parameterization:** Decoupling test logic from single values using `@pytest.mark.parametrize` for single-input and paired `(input, expected)` assertions.
2. **Multi-Argument & Cartesian Product Testing:** Validating business rules across multiple variables, testing exception handling with `pytest.raises`, and stacking decorators to generate full Cartesian product combinations ($M \times N$).
3. **Parameter IDs & Test Readability:** Improving test output diagnostics using custom `ids` lists, `pytest.param(..., id=...)`, and targeted per-parameter markers (`marks=pytest.mark.xfail`).
4. **Parametrized Fixtures:** Running entire test suites across multiple backend systems (databases, browsers) using `@pytest.fixture(params=...)` with automated setup/teardown via `yield`.
5. **Data-Driven Testing (DDT):** Decoupling datasets from test code by loading external CSV (`logins.csv`) and JSON (`test_cases.json`) files dynamically during test discovery.

---

## Directory Structure

```text
Lab05-Parametrization/
├── basic-parameterization/                   # Single & paired parameterization
│   ├── mathutils.py                          # is_even() and factorial() implementations
│   ├── test_factorial.py                     # Paired (n, expected) factorial tests
│   ├── test_param.py                         # Single-parameter parity tests
│   └── README.md                             # Basic parameterization guide
│
├── multiple-parameters/                      # Multi-argument & stacked parameterization
│   ├── discount.py                           # apply_discount() with boundary checks
│   ├── test_discount.py                      # Multi-parameter discount calculations
│   ├── test_discount_errors.py               # Parameterized exception testing (pytest.raises)
│   ├── test_multi.py                         # Stacked decorators (Cartesian product)
│   └── README.md                             # Multiple parameters guide
│
├── parameter-ids-and-readability/            # Test case naming & targeted marks
│   ├── test_custom_ids.py                    # Descriptive test labels via ids=[...]
│   ├── test_default_ids.py                   # Default opaque identifiers demo
│   ├── test_param_ids.py                     # Inline identifiers using pytest.param()
│   ├── test_param_marks.py                   # Per-case marking (pytest.mark.xfail)
│   └── README.md                             # Parameter IDs guide
│
├── parametrized-fixtures/                    # Fixture-level multi-environment testing
│   ├── test_browser.py                       # Multi-browser fixture with setup/teardown
│   ├── test_param_fixture.py                 # Multi-database fixture via request.param
│   └── README.md                             # Parametrized fixtures guide
│
├── data-driven-testing-from-external-files/  # External data file loaders
│   ├── logins.csv                            # External CSV credentials dataset
│   ├── test_cases.json                       # External JSON string transformation dataset
│   ├── test_csv_driven.py                    # CSV-driven login validation tests
│   ├── test_data_driven.py                   # JSON-driven string manipulation tests
│   ├── validate.py                           # is_valid_login() authentication logic
│   └── README.md                             # External DDT guide
│
└── README.md                                 # Lab 05 comprehensive guide
```

---

## Submodule Summaries

| Submodule | Directory | Key Topics Covered | Detailed Guide |
|---|---|---|:---:|
| **1. Basic Parameterization** | [`basic-parameterization/`](./basic-parameterization/) | `@pytest.mark.parametrize`, single parameters, paired `(input, expected)` tuples, boundary values | [View README](./basic-parameterization/README.md) |
| **2. Multiple Parameters** | [`multiple-parameters/`](./multiple-parameters/) | Multi-argument parameter lists, parameterized exception testing with `pytest.raises`, stacked Cartesian products ($3 \times 2 = 6$) | [View README](./multiple-parameters/README.md) |
| **3. Parameter IDs & Readability** | [`parameter-ids-and-readability/`](./parameter-ids-and-readability/) | Default vs. custom IDs, inline `pytest.param(..., id=...)`, targeted marks (`marks=pytest.mark.xfail`) | [View README](./parameter-ids-and-readability/README.md) |
| **4. Parametrized Fixtures** | [`parametrized-fixtures/`](./parametrized-fixtures/) | `@pytest.fixture(params=...)`, `request.param`, multi-environment execution, setup & teardown lifecycles via `yield` | [View README](./parametrized-fixtures/README.md) |
| **5. External Data-Driven Testing** | [`data-driven-testing-from-external-files/`](./data-driven-testing-from-external-files/) | External CSV (`csv.DictReader`) and JSON (`json.load`) parsing, dynamic parameter injection, type verification | [View README](./data-driven-testing-from-external-files/README.md) |

---

## Technical Details by Module

### 1. Basic Parameterization (`basic-parameterization/`)
Eliminates loop anti-patterns inside tests:
- **Single Argument:** `@pytest.mark.parametrize("number", [2, 4, 6, 8, 100])` generates 5 discrete test items for `is_even(number)`.
- **Paired Arguments:** `@pytest.mark.parametrize("n,expected", [(0, 1), (1, 1), (2, 2), (3, 6), (4, 24), (5, 120)])` verifies both boundary conditions ($0! = 1$) and factorial progressions.

### 2. Multiple Parameters & Cartesian Products (`multiple-parameters/`)
- **Multi-Argument Tests:** Evaluates discount rules across `(price, percent, expected)` combinations.
- **Exception Testing:** Verifies boundary infractions (`-1`, `-50`, `101`, `200`) raise `ValueError` using `with pytest.raises(ValueError)`.
- **Stacked Decorators:** Stacking `@pytest.mark.parametrize("x", [1, 2, 3])` and `@pytest.mark.parametrize("y", [10, 20])` automatically yields all $3 \times 2 = 6$ combinations.

### 3. Parameter IDs & Readability (`parameter-ids-and-readability/`)
- **Custom IDs:** Replaces generic indexes (`user0`, `user1`) with informative names (`alice-adult`, `bob-adult`) using `ids=[...]`.
- **Inline `pytest.param`:** Associates data directly with its ID and optional markers:
  ```python
  pytest.param(5, 20, id="known_bug", marks=pytest.mark.xfail)
  ```
  Allows tracking open bugs without failing the CI pipeline.

### 4. Parametrized Fixtures (`parametrized-fixtures/`)
- Injects configurations at the fixture level using `@pytest.fixture(params=[...])` and `request.param`.
- Automatically executes all dependent tests across each fixture parameter (e.g., testing `test_page_load` and `test_browser_clickable` across Chrome, Firefox, and Safari for a total of $2 \times 3 = 6$ tests).
- Manages setup and teardown per parameter using Python's `yield` construct.

### 5. External Data-Driven Testing (`data-driven-testing-from-external-files/`)
- Dynamically loads `logins.csv` to test authentication credentials against `is_valid_login`.
- Loads `test_cases.json` for string manipulation tests, illustrating how external datasets expose type-mismatch vulnerabilities early (`AttributeError` when an integer is passed to `.upper()`).

---

## How to Run Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running Individual Submodules:

```bash
# 1. Basic Parameterization
python -m pytest Lab05-Parametrization/basic-parameterization -v

# 2. Multiple Parameters
python -m pytest Lab05-Parametrization/multiple-parameters -v

# 3. Parameter IDs & Readability (with PYTHONPATH for discount module)
# PowerShell:
$env:PYTHONPATH="Lab05-Parametrization/multiple-parameters"; python -m pytest Lab05-Parametrization/parameter-ids-and-readability -v
# Linux/macOS:
PYTHONPATH=Lab05-Parametrization/multiple-parameters python -m pytest Lab05-Parametrization/parameter-ids-and-readability -v

# 4. Parametrized Fixtures (with setup/teardown tracing)
python -m pytest Lab05-Parametrization/parametrized-fixtures -v --setup-show

# 5. External Data-Driven Testing (run from its directory to resolve file paths)
cd "Lab05-Parametrization/data-driven-testing-from-external-files"
python -m pytest . -v
```
