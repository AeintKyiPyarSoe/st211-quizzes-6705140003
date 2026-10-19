import pytest
from bank import BankAccount
@pytest.fixture
def empty_account():
    return BankAccount(0)

@pytest.fixture
def funded_account():
    return BankAccount(1000)

@pytest.fixture
def sample_users():
    return [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"},
        {"id": 3, "name": "Carol", "role": "user"},
    ]