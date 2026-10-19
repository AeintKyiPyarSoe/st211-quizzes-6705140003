# Lab 04: Fixtures & Test Data Management

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

This directory contains the laboratory exercises for **Lab 04: Fixtures & Test Data Management**. The primary focus of this lab is mastering how to structure, inject, and lifecycle-manage test dependencies, eliminate boilerplate setup code, and enforce strict test isolation using **Pytest Fixtures**.

In automated testing, test suites rarely operate on static or isolated variables alone. Real-world applications require pre-configured objects, database handles, network stubs, or simulated environments. Pytest solves this through a flexible dependency injection architecture centered around `@pytest.fixture`.

### Key Learning Objectives
1. **Core Fixtures & Dependency Injection:** Decoupling object creation from test logic, eliminating "Arrange bloat", and relying on Pytest's automatic injection by argument name.
2. **Setup and Teardown Lifecycles:** Managing temporary files and stateful resources using the `yield` statement to guarantee clean disposal regardless of test outcomes.
3. **Fixture Scopes:** Controlling fixture execution boundaries (`function`, `class`, `module`, `package`, `session`) to balance execution speed with test isolation.
4. **Global Fixture Sharing with `conftest.py`:** Centralizing reusable fixtures across multiple test modules without manual import statements.
5. **Factory Fixtures:** Implementing inner builder closures to generate customized objects on demand and perform batch teardown.

---

## Directory Structure

```text
Lab04-FixturesAndTestDataManagement/
├── factory-fixtures/                        # Dynamic object generation & batch teardown
│   ├── bank.py                              # BankAccount domain model implementation
│   ├── test_factory.py                      # Basic factory fixture with parameter passing
│   ├── test_factory_advanced.py             # Advanced factory with yield cleanup tracking
│   └── README.md                            # Factory fixtures guide
│
├── fixture-scope/                           # Fixture lifecycles & sharing scopes
│   ├── test_scope.py                        # Function vs. Module scope comparison
│   ├── test_session.py                      # Session-scoped expensive setup demo
│   └── README.md                            # Fixture scope guide
│
├── fixtures/                                # Core fixture definitions and refactoring
│   ├── bank.py                              # BankAccount domain model implementation
│   ├── test_after.py                        # Test suite refactored with @pytest.fixture
│   └── README.md                            # Core fixtures documentation
│
├── setup-and-teardown/                      # Resource allocation & guaranteed cleanup
│   ├── test_db_style.py                     # Database connection/disconnection lifecycle
│   ├── test_teardown.py                     # File creation & deletion via yield
│   └── README.md                            # Setup and teardown guide
│
├── sharing-fixtures-with-conftest.py/       # Global directory-level fixture discovery
│   ├── bank.py                              # BankAccount domain model implementation
│   ├── conftest.py                          # Global fixtures (empty_account, funded_account, sample_users)
│   ├── test_shared_a.py                     # Account initialization tests using conftest fixtures
│   ├── test_shared_b.py                     # User & withdrawal tests using conftest fixtures
│   └── README.md                            # Conftest sharing guide
│
└── README.md                                # Lab 04 comprehensive guide
```

---

## Submodule Summaries

| Submodule | Directory | Key Topics Covered | Detailed Guide |
|---|---|---|:---:|
| **1. Core Fixtures** | [`fixtures/`](./fixtures/) | `@pytest.fixture`, dependency injection, eliminating Arrange duplication, test isolation | [View README](./fixtures/README.md) |
| **2. Setup & Teardown** | [`setup-and-teardown/`](./setup-and-teardown/) | `yield` statement, file lifecycle cleanup, database connect/disconnect management | [View README](./setup-and-teardown/README.md) |
| **3. Fixture Scope** | [`fixture-scope/`](./fixture-scope/) | `scope="function"`, `scope="module"`, `scope="session"`, execution boundaries, caching | [View README](./fixture-scope/README.md) |
| **4. Sharing Fixtures (`conftest.py`)** | [`sharing-fixtures-with-conftest.py/`](./sharing-fixtures-with-conftest.py/) | Automatic fixture discovery, eliminating import anti-patterns, cross-file sharing | [View README](./sharing-fixtures-with-conftest.py/README.md) |
| **5. Factory Fixtures** | [`factory-fixtures/`](./factory-fixtures/) | Callable fixtures, dynamic runtime parameters, multiple objects per test, tracked teardown | [View README](./factory-fixtures/README.md) |

---

## Technical Details by Module

### 1. Core Fixtures (`fixtures/`)
- Eliminates manual instantiation duplication in tests.
- Replaces repetitive setup code with declarative parameters:
  ```python
  @pytest.fixture
  def account():
      return BankAccount(100)

  def test_deposit(account):
      account.deposit(50)
      assert account.balance == 150
  ```
- Each test receives a freshly created `BankAccount` instance, ensuring full test isolation.

### 2. Setup and Teardown (`setup-and-teardown/`)
- Utilizes Python's generator mechanism (`yield`) to manage two-phase setup and teardown within a single function:
  ```python
  @pytest.fixture
  def temp_file():
      # Setup: executed before test
      filename = "test_data.txt"
      with open(filename, "w") as f:
          f.write("test content")
      yield filename
      # Teardown: guaranteed to execute after test completes
      os.remove(filename)
  ```
- Ensures external resources (files, mock servers, database connections) are never leaked.

### 3. Fixture Scopes (`fixture-scope/`)
- Provides precise control over resource lifecycles:
  - **`function` (default):** Runs once per test function.
  - **`module`:** Runs once per `.py` file, shared across tests in that file.
  - **`session`:** Runs once per entire test run, ideal for heavy configurations.
- Demonstrates how `module` and `session` fixtures cache instances to optimize execution speed without redundant setup overhead.

### 4. Sharing Fixtures with `conftest.py` (`sharing-fixtures-with-conftest.py/`)
- Pytest automatically discovers fixtures in `conftest.py` without requiring explicit Python `import` statements.
- Allows test suites to define common models (`empty_account`, `funded_account`, `sample_users`) once and share them across multiple test files (`test_shared_a.py`, `test_shared_b.py`) while preserving individual test isolation.

### 5. Factory Fixtures (`factory-fixtures/`)
- Resolves scenarios where tests need parameterized object creation or multiple instances in a single test:
  ```python
  @pytest.fixture
  def make_account():
      def _make(balance):
          return BankAccount(balance)
      return _make

  def test_multiple_accounts(make_account):
      a = make_account(100)
      b = make_account(200)
      assert a.balance != b.balance
  ```
- Advanced factories combine closures with `yield` to track all generated objects and perform unified cleanup.

---

## How to Run Tests

### Running the Entire Lab 04 Suite:

From the repository root:
```bash
# Run all 20 tests across all 5 submodules
python -m pytest Lab04-FixturesAndTestDataManagement -v
```

### Running Individual Submodules:

```bash
# 1. Core fixtures
python -m pytest Lab04-FixturesAndTestDataManagement/fixtures -v

# 2. Setup and teardown (with stdout prints)
python -m pytest Lab04-FixturesAndTestDataManagement/setup-and-teardown -v -s

# 3. Fixture scope (with stdout prints)
python -m pytest Lab04-FixturesAndTestDataManagement/fixture-scope -v -s

# 4. Sharing fixtures with conftest.py
python -m pytest Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py -v

# 5. Factory fixtures (with cleanup prints)
python -m pytest Lab04-FixturesAndTestDataManagement/factory-fixtures -v -s
```

### Tracing Fixture Execution Hierarchy:

Pytest includes the `--setup-show` flag to trace exactly when fixtures are created, cached, and destroyed:
```bash
python -m pytest Lab04-FixturesAndTestDataManagement -v --setup-show
```

---

## Expected Output

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: .../st211-quizzes-6705140003
collecting ... collected 20 items

Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory.py::test_small_account PASSED [  5%]
Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory.py::test_large_account PASSED [ 10%]
Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory.py::test_multiple_accounts PASSED [ 15%]
Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory_advanced.py::test_default_role PASSED [ 20%]
Lab04-FixturesAndTestDataManagement/factory-fixtures/test_factory_advanced.py::test_custom_role PASSED [ 25%]
Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_one PASSED [ 30%]
Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_two PASSED [ 35%]
Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_three PASSED [ 40%]
Lab04-FixturesAndTestDataManagement/fixture-scope/test_session.py::test_a PASSED [ 45%]
Lab04-FixturesAndTestDataManagement/fixture-scope/test_session.py::test_b PASSED [ 50%]
Lab04-FixturesAndTestDataManagement/fixtures/test_after.py::test_deposit PASSED [ 55%]
Lab04-FixturesAndTestDataManagement/fixtures/test_after.py::test_withdraw PASSED [ 60%]
Lab04-FixturesAndTestDataManagement/setup-and-teardown/test_db_style.py::test_database_connected PASSED [ 65%]
Lab04-FixturesAndTestDataManagement/setup-and-teardown/test_teardown.py::test_file_exists PASSED [ 70%]
Lab04-FixturesAndTestDataManagement/setup-and-teardown/test_teardown.py::test_file_content PASSED [ 75%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_a.py::test_empty_account_starts_at_zero PASSED [ 80%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_a.py::test_funded_account_has_money PASSED [ 85%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_b.py::test_user_count PASSED [ 90%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_b.py::test_first_user_is_admin PASSED [ 95%]
Lab04-FixturesAndTestDataManagement/sharing-fixtures-with-conftest.py/test_shared_b.py::test_funded_can_withdraw PASSED [100%]

============================= 20 passed in 0.12s ==============================
```
