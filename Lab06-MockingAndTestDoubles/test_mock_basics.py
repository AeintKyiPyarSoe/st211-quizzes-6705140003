from unittest.mock import Mock

def test_mock_returs_configured_value():
    mock = Mock() # create a mock object using Mock()
    mock.get_data.return_value = "fake data" # what should be defined when get_data() (attribute of mock) is called
    assert mock.get_data() == "fake data" # verify that the configured value is returned
    # A mock can imitate the behavior of a real method without implementing
    
def test_mock_accepts_any_call():
    mock = Mock()
    mock.anything() # mock automatically create methods when they are accessed
    mock.whatever(1,2,3)
    
def test_mock_attributes():
    mock = Mock()
    mock.name = "TestUser" # an attribute is assigned to the mock, the attribute can be read back like a normal object
    assert mock.name == "TestUser"
