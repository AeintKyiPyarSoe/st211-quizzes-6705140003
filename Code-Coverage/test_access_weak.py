from access import check_acces

def test_admin_active():
    assert check_acces("admin", True) == "granted"
    
def test_user_inactive():
    assert check_acces("user", False) == "denied"
    
