from unittest.mock import Mock

def test_multiple_return_values():
    mock = Mock()
    mock.next_id.side_effect = [1, 2, 3]
    assert mock.next_id() == 1
    assert mock.next_id() == 2
    assert mock.next_id() == 3
    
#side effect allows us to specify a sequence of return values for a mock method, enabling us to simulate different scenarios in our tests.
#in this case, the next_id method of the mock object will return 1 on the first call, 2 on the second call, and 3 on the third call.
#it can be useful when testing code that relies on a sequence of values or when we want to simulate different behaviors for the same method in different test cases.