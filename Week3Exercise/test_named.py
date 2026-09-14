import pytest
from bank import BankAccount

def test_deposit_positive_amount_increases_balance():   
    account = BankAccount(100)
    account.deposit(50)
    assert account.balance == 150

def test_deposit_negative_amount_raises_value_error():   
    account = BankAccount(100)
    with pytest.raises(ValueError): 
        account.deposit(-10)

def test_withdraw_more_than_balance_raises_value_error():   
    account = BankAccount(100)
    with pytest.raises(ValueError): 
        account.withdraw(200)

def test_withdraw_exact_balance_leaves_zero():  
    account = BankAccount(100)
    account.withdraw(100)
    assert account.balance == 0
