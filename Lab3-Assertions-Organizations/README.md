# Lab 03: Advanced Assertions & Test Organization

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  

---

## Overview

This directory contains the laboratory exercises for **Lab 03: Advanced Assertions & Test Organization**. The primary focus of this lab is mastering specialized assertion techniques in `pytest` and structuring test suites cleanly using test classes.

Key topics covered include:
- **Collection Assertions:** Comparing sequential and associative structures (lists, dictionaries, sets).
- **Floating-Point Arithmetic Testing:** Dealing with IEEE 754 floating-point inaccuracies using `pytest.approx`.
- **Test Organization via Classes:** Structuring related test methods into test classes (`Test*`) for readability, encapsulation, and scalable organization.

---

## Directory Structure

```text
Lab3-Assertions-Organizations/
├── assertion-types/
│   ├── test_collections.py              # List, dictionary, and set equality assertions
│   └── test_floats.py                   # Floating-point precision & approx() comparisons
├── organizing-tests-in-classes/
│   ├── shopping.py                      # ShoppingCart domain implementation
│   └── test_shopping.py                 # TestShoppingCart test class suite
└── README.md                            # Lab 03 documentation
```

---

## Modules & Core Concepts

### 1. Assertion Types (`assertion-types/`)

#### A. Floating-Point Precision (`test_floats.py`)
Computers represent decimal numbers in binary floating-point format (IEEE 754 standard). Certain decimal fractions cannot be represented with exact precision in binary:
```python
# In standard Python:
0.1 + 0.2 == 0.30000000000000004  # Not exactly 0.3!
```
- **The Problem:** Naive assertions like `assert 0.1 + 0.2 == 0.3` fail due to minute precision errors (demonstrated in `test_float_without_approx_fails`).
- **The Solution:** Pytest provides `pytest.approx()`, which performs tolerance-based relative and absolute comparisons:
  ```python
  from pytest import approx

  def test_float_precision():
      assert 0.1 + 0.2 == approx(0.3)
  ```

#### B. Collection Assertions (`test_collections.py`)
Python's `assert` statement in `pytest` performs deep structural comparisons on collections:
- **Sequential List Equality:** `assert [1, 2, 3] == [1, 2, 3]` verifies identical elements in identical order.
- **Order-Independent Comparison:** `assert sorted([3, 2, 1]) == [1, 2, 3]` allows order-insensitive validation without altering original data.
- **Dictionary Equivalence:** Asserts key-value correspondence regardless of insertion order:
  ```python
  expected = {"Name": "Alice", "Age": 30}
  actual = {"Age": 30, "Name": "Alice"}
  assert actual == expected
  ```
- **Set Operations:** Tests mathematical set logic:
  - Intersection (`&`): Common elements
  - Union (`|`): Combined unique elements
  - Difference (`-`): Elements in first set but not second

---

### 2. Organizing Tests in Classes (`organizing-tests-in-classes/`)

#### A. Domain Implementation (`shopping.py`)
Defines the `ShoppingCart` class:
- `__init__()`: Initializes an empty item list.
- `add(name, price)`: Appends an item record with name and price.
- `total()`: Computes total price across all items.
- `count()`: Returns the number of items in the cart.

#### B. Class-Based Test Organization (`test_shopping.py`)
While standalone test functions are common, grouping related tests inside a class provides several advantages:
- **Logical Namespacing:** Keeps related tests grouped together under the tested domain entity.
- **Clean Test Reporting:** Pytest displays test results nested under the class name: `test_shopping.py::TestShoppingCart::test_add_item_increases_count`.
- **Scoped Fixtures:** Enables class-level setup and teardown when necessary.

**Pytest Test Class Conventions:**
1. Class name must start with `Test` (e.g., `TestShoppingCart`).
2. Do **not** define an `__init__` constructor on test classes.
3. Test methods must start with `test_` and accept `self` as the first parameter.

```python
from shopping import ShoppingCart

class TestShoppingCart:
    def test_new_cart_is_empty(self):
        cart = ShoppingCart()
        assert cart.count() == 0
        
    def test_new_cart_total_is_zero(self):
        cart = ShoppingCart()
        assert cart.total() == 0
 
    def test_add_item_increases_count(self):
        cart = ShoppingCart()
        cart.add("Book", 20)
        assert cart.count() == 1
    
    def test_total_sum_prices(self):
        cart = ShoppingCart()
        cart.add("Book", 20)
        cart.add("Pen", 5)
        assert cart.total() == 25
```

---

## How to Run Tests

### Prerequisites
- Python 3.8+
- `pytest` installed (`pip install pytest`)

### Running All Lab 03 Tests
```bash
# Run all tests in Lab 03
python -m pytest Lab3-Assertions-Organizations -v
```

### Running Specific Test Suites
```bash
# Run floating-point assertion tests
python -m pytest Lab3-Assertions-Organizations/assertion-types/test_floats.py -v

# Run collection assertion tests
python -m pytest Lab3-Assertions-Organizations/assertion-types/test_collections.py -v

# Run shopping cart test class suite
python -m pytest Lab3-Assertions-Organizations/organizing-tests-in-classes -v
```
