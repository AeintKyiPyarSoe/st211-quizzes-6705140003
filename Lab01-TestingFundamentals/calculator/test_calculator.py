from calculator import add, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    
def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3