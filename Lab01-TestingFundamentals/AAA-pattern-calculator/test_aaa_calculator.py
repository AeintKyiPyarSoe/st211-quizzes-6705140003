from calculator import add, divide

def test_add():
    a, b = 2, 3 #Arrange: set up the data for the test
    result = add(a, b) #Act: call the function being tested
    assert result == 5 #Assert: check that the result is as expected
    
def test_divide():
    a, b = 10, 2 
    result = divide(a, b) 
    assert result == 5 