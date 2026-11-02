# Verifying Calls and Interactions in Test Doubles

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab06-MockingAndTestDoubles](../README.md)

---

## Overview

In automated unit testing, verification generally falls into two distinct categories:
1. **State Verification:** Testing whether a method returned the expected value or mutated an object into the expected state (e.g., `assert result == 42`).
2. **Behavior (Interaction) Verification:** Testing whether a unit of code interacted with its collaborators in the expected manner—i.e., verifying which methods were invoked, how many times they were invoked, and what exact arguments were passed.

Python's `unittest.mock.Mock` objects act as **Spies** and **Mocks**: they record every interaction made against them. This submodule explores the core call-verification API provided by `Mock`, along with failure analysis when call expectations are not satisfied.

---

## Files in this Directory

| File | Description |
|---|---|
| [`test_verify_calls.py`](./test_verify_calls.py) | Unit test suite demonstrating `assert_called()`, `assert_called_once()`, `assert_called_with()`, `call_count`, and intentional failure diagnostics. |

---

## Technical Deep Dive

### 1. The Call Verification API

Python's `Mock` object provides specialized assertion methods designed to verify method calls:

#### A. Verifying At Least One Call (`assert_called()`)
```python
def test_was_called():
    mock = Mock()
    mock.save()
    mock.save.assert_called()
```
- Passes if `mock.save` was invoked 1 or more times during the test.
- Fails with `AssertionError: Expected 'save' to have been called.` if never invoked.

#### B. Verifying Exactly One Call (`assert_called_once()`)
```python
def test_was_called_once():
    mock = Mock()
    mock.save()
    mock.save.assert_called_once()
```
- Asserts that `mock.save` was called exactly once (`call_count == 1`).
- Fails if the method was never called, or if called multiple times (preventing duplicate payments, double database writes, or duplicate emails).

#### C. Verifying Positional & Keyword Arguments (`assert_called_with(...)`)
```python
def test_called_with_arguments():
    mock = Mock()
    mock.charge(100, currency="USD")
    mock.charge.assert_called_with(100, currency="USD")
```
- Verifies that the most recent call to `mock.charge` was executed with `100` as the first argument and `currency="USD"` as the keyword argument.
- Fails if argument types, order, or values differ from expectations.

#### D. Verifying Precise Call Counts (`mock.method.call_count`)
```python
def test_call_count():
    mock = Mock()
    mock.log()
    mock.log()
    assert mock.log.call_count == 2
```
- `mock.log.call_count` is an integer tracking the cumulative number of times the mock was invoked.
- Can be asserted directly with Python's standard `assert` statement.

---

## Failure Analysis & Diagnostics

### Intentional Failure Case (`test_was_called_twice_but_expected_once`)

```python
def test_was_called_twice_but_expected_once():
    mock = Mock()
    mock.save()
    mock.save()
    mock.save.assert_called_once()
```

#### Diagnostic Output:
When Pytest executes this test, the mock inspection engine raises a detailed `AssertionError`:
```text
FAILED Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_was_called_twice_but_expected_once - AssertionError: Expected 'save' to have been called once. Called 2 times.
Calls: [call(), call()].
```

#### Why this is Significant:
1. **Root Cause Identification:** The error message explicitly states both the expected count (`called once`) and the actual count (`Called 2 times`).
2. **Call History Recording:** Pytest displays the exact list of calls recorded (`Calls: [call(), call()]`), helping developers diagnose unexpected loops or repeated queries in their code.

---

## Summary of Interaction Assertions

| Method / Property | Description | Common Use Case |
|---|---|---|
| `mock.assert_called()` | Verifies mock was called $\ge 1$ times. | Sanity check that an auditing or logging call occurred. |
| `mock.assert_called_once()` | Verifies mock was called exactly 1 time. | Critical one-shot operations: charging a card, closing a resource. |
| `mock.assert_called_with(*args, **kwargs)` | Verifies exact arguments of the most recent invocation. | Contract validation (correct API payload, recipient email). |
| `mock.assert_not_called()` | Verifies mock was never invoked. | Error handling paths (ensure no charge occurred on invalid input). |
| `mock.call_count` | Integer count of invocations. | Verifying batch loops, retries, and pagination iterations. |

---

## How to Run the Tests

From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles/verifying-calls -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
collecting ... collected 5 items

Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_was_called PASSED [ 20%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_was_called_once PASSED [ 40%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_was_called_twice_but_expected_once FAILED [ 60%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_called_with_arguments PASSED [ 80%]
Lab06-MockingAndTestDoubles/verifying-calls/test_verify_calls.py::test_call_count PASSED [100%]

================================== FAILURES ===================================
___________________ test_was_called_twice_but_expected_once ___________________

    def test_was_called_twice_but_expected_once():
        mock = Mock()
        mock.save()
        mock.save()
>       mock.save.assert_called_once()
E       AssertionError: Expected 'save' to have been called once. Called 2 times.
E       Calls: [call(), call()].

========================= 1 failed, 4 passed in 0.45s =========================
```
