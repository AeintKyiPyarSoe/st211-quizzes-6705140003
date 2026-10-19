# Pytest Fixture Scopes & Lifecycle Management

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab04-FixturesAndTestDataManagement](../README.md)

---

## Overview

By default, Pytest fixtures are created and destroyed once per test function (`scope="function"`). While this guarantees absolute test isolation, real-world automated testing often involves expensive setup operations—such as:
- Initializing a database engine or applying migrations
- Starting a headless browser (Chromium/Firefox)
- Parsing large configuration files or compiling test fixtures
- Spinning up test containers or mock HTTP servers

Re-running these heavy operations before every individual test leads to slow, sluggish test suites. Pytest solves this performance dilemma through **Fixture Scopes**, allowing engineers to control the lifespan and sharing boundary of fixture instances across tests.

---

## Files in this Directory

| File | Description |
|---|---|
| [`test_scope.py`](./test_scope.py) | Compares `scope="function"` against `scope="module"`. Shows that a module-scoped fixture executes once per test file, while function-scoped fixtures execute for each test. |
| [`test_session.py`](./test_session.py) | Demonstrates `scope="session"`, where an expensive setup operation executes exactly once across the entire test session and is reused by all requesting tests. |

---

## Technical Details

### 1. Pytest Scope Hierarchy

Pytest provides five fixture scopes, listed from narrowest to widest:

| Scope | Lifetime | Typical Use Cases |
|---|---|---|
| **`function`** *(default)* | Created & destroyed once per test function | Mutable objects, stateful domain models, isolated transactions |
| **`class`** | Created once per test class | Setup shared across methods of a `Test*` class |
| **`module`** | Created once per `.py` module file | Read-only database snapshots, shared file handles within a file |
| **`package`** | Created once per package/directory | Shared environment setup across a package of test files |
| **`session`** | Created once per entire Pytest execution | Database connection pools, configuration loaders, Docker containers |

> [!IMPORTANT]
> **Scope Rule:** A fixture can only depend on fixtures of the **same or broader scope**. For example, a `module`-scoped fixture cannot depend on a `function`-scoped fixture, because a module-level object cannot be recreated on every function call.

---

### 2. Function vs. Module Scope (`test_scope.py`)

```python
import pytest

@pytest.fixture(scope="function")
def function_fixture():
    print("\n [function fixture] running")
    return "function"

@pytest.fixture(scope="module")
def module_fixture():
    print("\n [module fixture] running")
    return "module"

def test_one(function_fixture, module_fixture):
    assert function_fixture == "function"
    
def test_two(function_fixture, module_fixture):
    assert module_fixture == "module"
    
def test_three(function_fixture, module_fixture):
    assert True
```

#### Execution Analysis:
- When running `pytest -s`:
  - `module_fixture` runs **1 time** (before `test_one`).
  - `function_fixture` runs **3 times** (once before `test_one`, once before `test_two`, and once before `test_three`).
- `test_two` and `test_three` receive the cached result of `module_fixture` without re-executing its setup.

---

### 3. Session Scope for Heavy Setup (`test_session.py`)

```python
import pytest

@pytest.fixture(scope="session")
def expensive_setup():
    print("\n[session] expensive setup runs ONCE")
    return {"config": "loaded"}

def test_a(expensive_setup):
    assert expensive_setup["config"] == "loaded"
    
def test_b(expensive_setup):
    assert "config" in expensive_setup
```

#### Execution Analysis:
- `expensive_setup` executes once when `test_a` requests it.
- When `test_b` runs, Pytest injects the identical dictionary instance without calling the fixture body again.
- If this test suite had 1,000 tests requesting `expensive_setup`, the initialization cost would still be paid only **once**.

---

## Best Practices & Isolation Warnings

> [!WARNING]
> **Beware of Shared Mutable State:**
> If a fixture with a scope broader than `function` (`module` or `session`) returns a mutable object (e.g., a list, dictionary, or database table), modifying that object in one test will affect all subsequent tests.
> - **Read-only data:** Safe for `module` or `session` scope.
> - **Mutable state:** Must use `function` scope, or use a cleanup teardown / transaction rollback to restore clean state.

---

## How to Run the Tests

### From the Repository Root:

```bash
# Run all tests in fixture-scope
python -m pytest Lab04-FixturesAndTestDataManagement/fixture-scope -v

# Run with stdout printing (-s) to observe fixture execution counts
python -m pytest Lab04-FixturesAndTestDataManagement/fixture-scope -v -s

# Trace fixture creation/destruction with --setup-show
python -m pytest Lab04-FixturesAndTestDataManagement/fixture-scope -v --setup-show
```

### From within this Directory:

```bash
# Run tests with output printing
python -m pytest test_scope.py test_session.py -v -s
```

---

## Expected Output

### With Print Statements (`-s`):

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: .../st211-quizzes-6705140003
collecting ... collected 5 items

Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_one 
 [module fixture] running

 [function fixture] running
PASSED
Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_two 
 [function fixture] running
PASSED
Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_three 
 [function fixture] running
PASSED
Lab04-FixturesAndTestDataManagement/fixture-scope/test_session.py::test_a 
[session] expensive setup runs ONCE
PASSED
Lab04-FixturesAndTestDataManagement/fixture-scope/test_session.py::test_b PASSED

============================== 5 passed in 0.05s ==============================
```

### With `--setup-show`:

```text
Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_one 
    SETUP    M module_fixture
      SETUP    F function_fixture
        Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_one (fixtures used: function_fixture, module_fixture) PASSED
      TEARDOWN F function_fixture
Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_two 
      SETUP    F function_fixture
        Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_two (fixtures used: function_fixture, module_fixture) PASSED
      TEARDOWN F function_fixture
Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_three 
      SETUP    F function_fixture
        Lab04-FixturesAndTestDataManagement/fixture-scope/test_scope.py::test_three (fixtures used: function_fixture, module_fixture) PASSED
      TEARDOWN F function_fixture
    TEARDOWN M module_fixture
Lab04-FixturesAndTestDataManagement/fixture-scope/test_session.py::test_a 
SETUP    S expensive_setup
        Lab04-FixturesAndTestDataManagement/fixture-scope/test_session.py::test_a (fixtures used: expensive_setup) PASSED
Lab04-FixturesAndTestDataManagement/fixture-scope/test_session.py::test_b 
        Lab04-FixturesAndTestDataManagement/fixture-scope/test_session.py::test_b (fixtures used: expensive_setup) PASSED
TEARDOWN S expensive_setup
```
