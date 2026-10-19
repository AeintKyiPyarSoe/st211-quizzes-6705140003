import json
import pytest

def load_cases():
    with open('test_cases.json') as f:
        data = json.load(f) # read the JSON file and parse it into a Python object
    return [(case['input'], case['expected']) for case in data]

@pytest.mark.parametrize("text,expected", load_cases()) # loader runs once and returns a list of tuples for the test cases
def test_uppercase(text, expected):
    assert text.upper() == expected # only works for strings, so the last test case will fail
