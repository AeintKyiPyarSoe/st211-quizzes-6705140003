# Assertion Testing: Floating Points & Collections

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  

---

## Overview

This module demonstrates advanced assertion patterns in `pytest`, focusing on:
1. Handling binary floating-point representation limitations using `pytest.approx`.
2. Verifying equalities across data structures including lists, dictionaries, and sets.

---

## Files

- **`test_floats.py`**:
  - `test_float_precision`: Verifies `0.1 + 0.2 == approx(0.3)` using pytest's tolerance comparison to account for floating-point inaccuracy under IEEE 754 standard.
  - `test_float_without_approx_fails`: Demonstrates that `0.1 + 0.2 != 0.3` in standard Python arithmetic due to precision limits (`0.30000000000000004`).
- **`test_collections.py`**:
  - `test_list_equality`: Asserts element-by-element equality preserving exact sequence order (`[1, 2, 3] == [1, 2, 3]`).
  - `test_list_contents`: Demonstrates testing list contents regardless of initial order using `sorted()`.
  - `test_dict_equality`: Checks that key-value dictionaries match regardless of key order definition.
  - `test_set_operations`: Demonstrates mathematical set operators:
    - Intersection (`&`): `{1, 2, 3} & {2, 3, 4} == {2, 3}`
    - Union (`|`): `{1, 2, 3} | {2, 3, 4} == {1, 2, 3, 4}`
    - Difference (`-`): `{1, 2, 3} - {2, 3, 4} == {1}`

---

## How to Run

Run the tests inside this folder:
```bash
python -m pytest test_floats.py test_list_equality.py -v
```
