from access import check_acces

def test_admin_active_granted():
    assert check_acces("admin", True) == "granted"
    
def test_admin_inactive_denied():
    assert check_acces("admin", False) == "denied"

def test_non_admin_active_denied():
    assert check_acces("user", True) == "denied"
    
def test_non_admin_inactive_denied():
    assert check_acces("user", False) == "denied"
    