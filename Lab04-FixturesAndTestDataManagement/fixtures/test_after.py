import pytest
from bank import BankAccount

@pytest.fixture
# fixture is not a test
def account():
    return BankAccount(100)

def test_deposit(account):
    account.deposit(50)
    assert account.balance == 150
    
def test_withdraw(account):
    account.withdraw(30)
    assert account.balance == 70