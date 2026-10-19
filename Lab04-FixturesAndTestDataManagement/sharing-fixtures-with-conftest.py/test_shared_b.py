def test_user_count(sample_users):
    assert len(sample_users) == 3

def test_first_user_is_admin(sample_users):
    assert sample_users[0]["role"] == "admin"
    
def test_funded_can_withdraw(funded_account):
    funded_account.withdraw(500)
    assert funded_account.balance == 500