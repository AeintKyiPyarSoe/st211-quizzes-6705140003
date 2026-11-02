from unittest.mock import Mock

def test_was_called():
    mock = Mock()
    mock.save()
    mock.save.assert_called()
# This test checks if the save() method was called at least once.

def test_was_called_once():
    mock = Mock()
    mock.save()
    mock.save.assert_called_once()
# we want to verify that the save() method was called exactly once. 
# If it was called more than once or not at all, the test will fail.
    
def test_was_called_twice_but_expected_once():
    mock = Mock()
    mock.save()
    mock.save()
    mock.save.assert_called_once()
# This test is designed to fail because the save() method was called twice, but we are asserting that it should have been called only once.

# in real-world scenarios, we often want to verify that certain methods were called with specific arguments.
# for example, if we have a method that sends an email, we might want to check that it was called with the correct recipient and subject line.

def test_called_with_arguments():
    mock = Mock()
    mock.charge(100, currency="USD")
    mock.charge.assert_called_with(100, currency="USD")

def test_call_count():
    mock = Mock()
    mock.log()
    mock.log()
    assert mock.log.call_count == 2