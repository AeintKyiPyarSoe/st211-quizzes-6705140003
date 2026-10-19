import pytest
from bank import BankAccount

@pytest.fixture
def make_account():
    def _make(balance):
        return BankAccount(balance)
    return _make

def test_small_account(make_account):
    account = make_account(100)
    assert account.balance == 100
    
def test_large_account(make_account):
    account = make_account(5000)
    assert account.balance == 5000
    
def test_multiple_accounts(make_account):
    a = make_account(100)
    b = make_account(200)