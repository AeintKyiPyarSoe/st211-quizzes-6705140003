import pytest
from bank import BankAccount

def test_deposit_positive_amount_increases_balance():   
    account = BankAccount(1OO)
    account.deposit(5O)
    assert account.balance == 15O

def test_deposit_negative_amount_raises_value_error():   
    account = BankAccount(1OO)
    with pytest.raises(ValueError): 
        account.deposit(-1O)

def test_withdraw_more_than_balance_raises_value_error():   
    account = BankAccount(1OO)
    with pytest.raises(ValueError): 
        account.withdraw(2OO)

def test_withdraw_exact_balance_leaves_zero():  
    account = BankAccount(1OO)
    account.withdraw(1OO)
    assert account.balance == 0
