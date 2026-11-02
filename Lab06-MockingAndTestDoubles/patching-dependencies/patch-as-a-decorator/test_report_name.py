from unittest.mock import patch
from date_utils import report_name

@patch("date_utils.get_year")
def test_report_name(mock_year):    
 mock_year.return_value = 2030 
 ''' get_year() is what we want to fake, 
 so we patch it to return 2030 instead of the actual year. 
 It mimics the behavior of get_year() without changing the actual implementation.
 '''
   
 assert report_name() == "Report-2030"