# Organized Tests: Test Classes Pattern

**Course:** 192-211 Automated Software Testing  
**Student:** Aeint Kyi Pyar Soe (6705140003)  

---

## Overview

This module illustrates test organization best practices by grouping related test functions inside a Python class (`TestShoppingCart`). Structuring tests with test classes offers several advantages:
- Groups logically related tests together under a shared namespace.
- Keeps test suites modular, organized, and scalable.
- Allows selective execution of entire test classes or specific methods.

---

## Implementation & Test Suite

### 1. `shopping.py` (`ShoppingCart`)
A model representing a shopping cart with the following operations:
- `add(name, price)`: Adds a new item entry `{"name": name, "price": price}` to the cart.
- `total()`: Calculates and returns the sum of all item prices.
- `count()` / `count_items()`: Returns the total count of items in the cart.

### 2. `test_shopping.py` (`TestShoppingCart`)
A test class containing targeted test cases:
- `test_new_cart_is_empty`: Verifies an empty cart initializes with an item count of 0.
- `test_new_cart_total_is_zero`: Verifies an empty cart initializes with a total price of 0.
- `test_add_item_increases_count`: Verifies adding an item increments cart count by 1.
- `test_total_sum_prices`: Verifies multiple added items correctly sum their respective prices.

---

## How to Run

Run the shopping cart test suite:
```bash
python -m pytest test_shopping.py -v
```
