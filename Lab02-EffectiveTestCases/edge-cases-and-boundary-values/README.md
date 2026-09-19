# Boundary Value Analysis (BVA) & Edge Cases

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab02-EffectiveTestCases](../README.md)

---

## Overview

This subfolder demonstrates **Boundary Value Analysis (BVA)** and **Edge Case Testing**. 

In software engineering, defects cluster disproportionately around the boundaries of input domains (e.g., threshold comparisons using `<`, `>`, `<=`, `>=`). Testing interior values often misses off-by-one errors, whereas testing the exact boundary values systematically uncovers these defects.

---

## Files in this Directory

| File | Description |
|---|---|
| [`grades.py`](./grades.py) | Implementation of `letter_grade(score)` which classifies scores $0 \le score \le 100$ into grades A, B, C, or F. |
| [`test_grades.py`](./test_grades.py) | Test suite targeting partition boundaries, minimum/maximum valid extremes, and out-of-range values. |

---

## Domain Logic & Equivalence Partitions

In `grades.py`, scores are partitioned into the following ranges:

```python
def letter_grade(score):
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0-100.")
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    return "F"
```

| Grade Partition | Valid Score Range | Boundary Values to Test |
|:---:|:---:|:---:|
| **A** | $80 \le \text{score} \le 100$ | $80$ (boundary minimum for A), $100$ (maximum valid) |
| **B** | $70 \le \text{score} < 80$ | $79$ (just below A), $70$ (boundary minimum for B) |
| **C** | $60 \le \text{score} < 70$ | $60$ (lowest passing score) |
| **F** | $0 \le \text{score} < 60$ | $59$ (highest failing score), $0$ (minimum valid score) |
| **Invalid Domain** | $\text{score} < 0$ or $\text{score} > 100$ | $-1$ (just below minimum valid), $101$ (just above maximum valid) |

---

## Boundary Values Tested in `test_grades.py`

```python
import pytest
from grades import letter_grade

def test_boundary_a_grade():
    assert letter_grade(80) == "A"
    # Why not test with 85? Because 80 is the actual boundary threshold!
    # Testing the boundary value ensures off-by-one errors (e.g. `> 80` instead of `>= 80`) are caught.
    assert letter_grade(79) == "B"

def test_boundary_pass_fail():
    assert letter_grade(60) == "C"  # Lowest passing score
    assert letter_grade(59) == "F"  # Highest failing score (just failed)

def test_minmal_valid():
    assert letter_grade(0) == "F"   # Absolute minimum valid input

def test_maximum_valid():
    assert letter_grade(100) == "A" # Absolute maximum valid input

def test_below_minimal_invalid():
    with pytest.raises(ValueError):
        letter_grade(-1)           # Negative out-of-bounds boundary
```

### Why Test Boundaries Instead of Arbitrary Middle Values?
- If a developer accidentally writes `if score > 80:` instead of `if score >= 80:`, a test using `85` will still pass, hiding the defect!
- A test specifically evaluating `80` immediately catches the error.

---

## How to Run

### Run Unit Tests with Pytest:
```bash
python -m pytest Lab02-EffectiveTestCases/edge-cases-and-boundary-values -v
```

### Run Standalone Script:
```bash
python Lab02-EffectiveTestCases/edge-cases-and-boundary-values/grades.py
```

### Expected Test Output:
```text
test_grades.py::test_boundary_a_grade PASSED
test_grades.py::test_boundary_pass_fail PASSED
test_grades.py::test_minmal_valid PASSED
test_grades.py::test_maximum_valid PASSED
test_grades.py::test_below_minimal_invalid PASSED
```
