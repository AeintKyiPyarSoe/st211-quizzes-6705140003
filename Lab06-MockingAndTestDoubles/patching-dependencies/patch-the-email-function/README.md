# Patching External Network Functions (Email Dispatch)

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [patching-dependencies](../README.md)

---

## Overview

Software components that send transactional emails, SMS messages, or push notifications perform real external network I/O. If executed during unit tests:
1. **Tests may spam real email inboxes.**
2. **Tests will crash or hang** when offline or if the SMTP mail server is unreachable.
3. **Execution is drastically slowed down** by socket handshakes, DNS lookups, and SMTP timeouts.

Using `unittest.mock.patch` with Python's `with` statement (the context manager pattern) lets tests isolate network functions right where they are invoked, guaranteeing safe, instantaneous, offline execution.

---

## Files in this Directory

| File | Description |
|---|---|
| [`notifications.py`](./notifications.py) | Module containing `send_email(to, subject)` (which initiates an `smtplib.SMTP` connection) and `notify_user(user_email)`. |
| [`test_notifications.py`](./test_notifications.py) | Unit test employing a `with patch(...)` context manager to intercept `send_email` and assert notification flow without triggering network calls. |

---

## Technical Deep Dive

### 1. The Real Network Collaborator (`notifications.py`)

```python
import smtplib

def send_email(to, subject):
    server = smtplib.SMTP("smtp.example.com")
    server.sendmail("noreply@app.com", to, subject)
    server.quit()
    return True

def notify_user(user_email):
    send_email(user_email, "Welcome!")
    return f"Notified {user_email}"
```

- When `notify_user()` is called, it executes `send_email()`.
- If unmocked, `smtplib.SMTP("smtp.example.com")` will attempt a socket connection on port 25, which either times out or throws an `OSError` / `gaierror` when no connection exists.

---

### 2. Context-Manager Patching (`test_notifications.py`)

```python
from unittest.mock import patch
from notifications import notify_user

def test_notify_user_without_sending_email():
    with patch("notifications.send_email") as mock_send:
        # Inside this block, notifications.send_email is a Mock object
        mock_send.return_value = True
        
        result = notify_user("student@siam.ac.th")
        
    # Outside the block, send_email is automatically restored
    assert result == "Notified student@siam.ac.th"
```

#### Why the Context Manager Pattern is Effective:
- **Pinpoint Scope:** The mock is active only within the lines indented under `with patch(...)`.
- **Automatic Cleanup:** When the `with` block finishes, `notifications.send_email` is immediately restored to the original function, preventing cross-test pollution.
- **Safety Guarantee:** No network packets leave the machine during unit test execution.

---

## How to Run the Tests

From the repository root:
```bash
python -m pytest Lab06-MockingAndTestDoubles/patching-dependencies/patch-the-email-function -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.13.1, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Siam-BSc-IT\Third Year\192-211 automated software testing\st211-quizzes-6705140003
collecting ... collected 1 item

Lab06-MockingAndTestDoubles/patching-dependencies/patch-the-email-function/test_notifications.py::test_notify_user_without_sending_email PASSED [100%]

============================== 1 passed in 0.05s ==============================
```
