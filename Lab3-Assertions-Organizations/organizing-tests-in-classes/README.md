# Organizing Tests in Classes

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  
**Institution:** Siam University  
**Parent Directory:** [Lab3-Assertions-Organizations](../README.md)

---

## Overview

This subfolder demonstrates how to structure and organize automated unit tests into **test classes** (`Test*`) using Pytest.

Grouping related tests into classes improves code readability, namespaces test scenarios by target component, provides hierarchical test runner reports, and enables class-level fixture scoping.

---

## Files in this Directory

| File | Description |
|---|---|
| [`shopping.py`](./shopping.py) | `ShoppingCart` domain class tracking item records, item counts, and total price calculation. |
| [`test_shopping.py`](./test_shopping.py) | Test suite organized inside the `TestShoppingCart` class. |

---

## Pytest Test Class Rules & Conventions

When creating test classes in Pytest, adhere to the following rules:
1. **Class Naming:** The class name must begin with `Test` (in PascalCase), e.g., `class TestShoppingCart:`.
2. **No Constructor:** Never implement an `__init__()` method in a Pytest test class. Pytest handles class instantiation dynamically.
3. **Method Naming:** Every test method inside the class must begin with `test_` and accept `self` as its first parameter.

---

## Implementation Details

### Domain Implementation (`shopping.py`)
```python
class ShoppingCart:
    def __init__(self):
        self.items = []
    
    def add(self, name, price):
        self.items.append({"name": name, "price": price})
        
    def total(self):
        return sum(item["price"] for item in self.items)
    
    def count(self):
        return len(self.items)
```

---

### Class-Based Test Suite (`test_shopping.py`)
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

## Advantages of Class-Based Organization

| Advantage | Benefit |
|---|---|
| **Logical Grouping** | All tests for `ShoppingCart` are encapsulated in one namespace. |
| **Clear Reporting** | Pytest outputs hierarchical identifiers: `test_shopping.py::TestShoppingCart::test_add_item_increases_count`. |
| **Selective Execution** | Run only this class using `pytest -k TestShoppingCart`. |
| **Class Scoping** | Easily share class-scoped setup/teardown fixtures (`@pytest.fixture(scope="class")`) if required. |

---

## How to Run the Tests

### From the Repository Root:
```bash
python -m pytest Lab3-Assertions-Organizations/organizing-tests-in-classes -v
```

### Run Specifically by Class Name:
```bash
python -m pytest -k TestShoppingCart -v
```

### From within this Directory:
```bash
python -m pytest test_shopping.py -v
```

### Expected Output:
```text
test_shopping.py::TestShoppingCart::test_new_cart_is_empty PASSED
test_shopping.py::TestShoppingCart::test_new_cart_total_is_zero PASSED
test_shopping.py::TestShoppingCart::test_add_item_increases_count PASSED
test_shopping.py::TestShoppingCart::test_total_sum_prices PASSED
```
