import csv, pytest
from validate import is_valid_login

def load_login_cases():
    cases = [] # define an empty list to hold the test cases
    with open("logins.csv") as f:
        for row in csv.DictReader(f): # read header row as dict keys, each row is a dict with keys as column names and values as cell values
            expected = row["valid"] == "True" # convert string to boolean, "True" becomes True, "False" becomes False
            cases.append((row["username"], row["password"], expected))
    return cases # return a list of tuples, each tuple contains (username, password, expected) for each test case

@pytest.mark.parametrize("username,password,expected", load_login_cases())
def test_is_valid_login(username, password, expected):
    assert is_valid_login(username, password) == expected

'''
Username	Password	Actual result	Expected	Test
admin	    admin123	True	        True	    PASS
user	    pass456	    True	        True	    PASS
hacker	    (empty)	    False	        False	    PASS
(empty)	    nopassword	False	        False	    PASS
'''