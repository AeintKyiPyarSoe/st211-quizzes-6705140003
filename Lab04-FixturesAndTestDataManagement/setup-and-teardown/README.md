# Setup and Teardown with Fixtures (`yield` Statement)

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab04-FixturesAndTestDataManagement](../README.md)

---

## Overview

In automated testing, test suites frequently interact with external or stateful resources—such as temporary files, database connections, mock servers, or hardware stubs. Leaving these resources dangling after tests complete causes disk clutter, connection pool exhaustion, and intermittent test contamination.

In classical xUnit frameworks (like `unittest`), setup and teardown are implemented using separate `setUp()` and `tearDown()` methods. Pytest modernizes this lifecycle management through **generator fixtures** utilizing Python's `yield` statement.

With a `yield` fixture:
1. **Setup logic** executes before the `yield` statement.
2. The yielded value is passed directly to the test function.
3. **Teardown logic** executes immediately after the test completes—even if the test fails or raises an assertion error.

---

## Files in this Directory

| File | Description |
|---|---|
| [`test_teardown.py`](./test_teardown.py) | Temporary file lifecycle fixture (`temp_file`) demonstrating creation before test execution and guaranteed cleanup (`os.remove`) after `yield`. |
| [`test_db_style.py`](./test_db_style.py) | Database connection lifecycle fixture (`database`) managing connection (`connect()`) and disconnection (`disconnect()`) around a `FakeDatabase` instance. |

---

## Technical Details

### 1. Anatomy of a `yield` Fixture

Pytest transforms any fixture containing a `yield` statement into a two-phase context manager:

```python
import pytest

@pytest.fixture
def managed_resource():
    # ---------------- [SETUP PHASE] ----------------
    # Executed before the test function runs
    resource = allocate_resource()
    print("\n[setup] resource acquired")

    # Hand over the resource to the test function
    yield resource

    # --------------- [TEARDOWN PHASE] --------------
    # Executed after the test completes (PASS or FAIL)
    resource.release()
    print("\n[teardown] resource released")
```

#### Key Execution Characteristics:
- **Linear Readability:** Setup and teardown code reside in the exact same function, keeping resource acquisition and release logically co-located.
- **Guaranteed Cleanup:** If an assertion inside the test fails, Pytest catches the exception, runs the teardown code after `yield`, and then marks the test as failed.
- **Clean Test Signatures:** Tests simply request the fixture parameter without worrying about resource disposal.

---

### 2. Temporary File Lifecycle (`test_teardown.py`)

File operations require strict cleanup to prevent orphan files on disk:

```python
import pytest
import os

@pytest.fixture
def temp_file():
    filename = "test_data.txt"
    with open(filename, "w") as f:
        f.write("test content") 
    print("\n[setup] file created")
    
    yield filename # hand the filename to the test
    
    os.remove(filename)
    print("\n[teardown] file removed")

def test_file_exists(temp_file):
    assert os.path.exists(temp_file)
    
def test_file_content(temp_file):
    with open(temp_file) as f:
        content = f.read()
        assert content == "test content"
```

#### Lifecycle Trace:
1. Pytest collects `test_file_exists`.
2. Pytest detects dependency on `temp_file`.
3. Fixture creates `test_data.txt` and writes `"test content"`.
4. Fixture yields `filename` to `test_file_exists`.
5. `test_file_exists` verifies `os.path.exists(temp_file)` is `True`.
6. Control returns to fixture; `os.remove(filename)` deletes the file.
7. Pytest moves to `test_file_content`, repeating the exact same isolated lifecycle.

---

### 3. Database Connection Style (`test_db_style.py`)

Managing stateful services like database handles or network sessions:

```python
import pytest

class FakeDatabase:
    def __init__(self):
        self.connected = False
        self.data = []
    def connect(self):
        self.connected = True
    def disconnect(self):
        self.connected = False
        
@pytest.fixture
def database():
    db = FakeDatabase()
    db.connect() # setup
    yield db
    db.disconnect() # teardown

def test_database_connected(database):
    assert database.connected is True
```

#### Benefits:
- Ensures connections are never leaked.
- Guarantees each test starts with an active connection without manual `connect()` / `disconnect()` calls in every test function.

---

## Classical `setUp`/`tearDown` vs. Pytest `yield` Fixtures

| Feature | xUnit `setUp()` / `tearDown()` | Pytest `yield` Fixture |
|---|---|---|
| **Structure** | Split across two separate class methods | Single cohesive function |
| **Granularity** | Applies indiscriminately to all tests in a class | Applied only to tests requesting the fixture |
| **Composability** | Hard to combine multiple setups cleanly | Multiple fixtures can be combined and nested |
| **State Storage** | Relies on `self.resource` attribute mutation | Pure dependency injection via return/yield value |

---

## How to Run the Tests

### From the Repository Root:

```bash
# Run all tests in setup-and-teardown
python -m pytest Lab04-FixturesAndTestDataManagement/setup-and-teardown -v

# Run with stdout printing (-s) to observe setup and teardown messages
python -m pytest Lab04-FixturesAndTestDataManagement/setup-and-teardown -v -s
```

### From within this Directory:

```bash
# Run tests with output capturing disabled
python -m pytest -v -s

# Run with fixture lifecycle tracing
python -m pytest -v --setup-show
```

---

## Expected Output

```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: .../st211-quizzes-6705140003
collecting ... collected 3 items

Lab04-FixturesAndTestDataManagement/setup-and-teardown/test_db_style.py::test_database_connected PASSED
Lab04-FixturesAndTestDataManagement/setup-and-teardown/test_teardown.py::test_file_exists 
[setup] file created
PASSED
[teardown] file removed

Lab04-FixturesAndTestDataManagement/setup-and-teardown/test_teardown.py::test_file_content 
[setup] file created
PASSED
[teardown] file removed


============================== 3 passed in 0.05s ==============================
```
