import pytest

@pytest.fixture(scope="function")
def function_fixture():
    print("\n [function fixture] running")
    return "function"

@pytest.fixture(scope="module")
def module_fixture():
    print("\n [module fixture] running")
    return "module"

def test_one(function_fixture, module_fixture):
    assert function_fixture == "function"
    
def test_two(function_fixture, module_fixture):
    assert module_fixture == "module"
    
def test_three(function_fixture, module_fixture):
    assert True