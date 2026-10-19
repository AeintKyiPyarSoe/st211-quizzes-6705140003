import pytest

@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request): # request is a built-in pytest fixture that provides information about the requesting test function
    return request.param # request.param holds the current parameter value for the fixture, which will be one of the values in the params list

def test_database_connection(database_type):
    print(f"\n Testing with {database_type}")
    assert database_type in ["sqlite", "postgresql", "mysql"]