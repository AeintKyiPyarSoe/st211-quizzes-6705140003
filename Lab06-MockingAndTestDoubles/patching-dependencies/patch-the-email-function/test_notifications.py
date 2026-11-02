from unittest.mock import patch
from notifications import notify_user

def test_notify_user_without_sending_email():
    with patch("notifications.send_email") as mock_send: 
        '''notify_user() will call send_email(), 
        but we don't want to actually send an email during testing, 
        so we patch send_email() to replace it with a mock object. 
        notifications.send_email is the path to the function we want to patch. 
        The mock object is assigned to mock_send, which we can use to control the behavior of the patched function.
        ''' 
        mock_send.return_value
        
        result = notify_user("student@siam.ac.th")
        
    assert result == "Notified student@siam.ac.th"