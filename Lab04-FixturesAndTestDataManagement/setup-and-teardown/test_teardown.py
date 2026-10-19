import pytest
import os

@pytest.fixture
def temp_file():
    filename = "test_data.txt"
    with open(filename, "w") as f:
        f.write("test content") 
    print("\n[setup] file created")
    
    yield filename # hand the filename to the test
    
    os.remove(filename)
    print("\n[teardown] file removed")
    
def test_file_exists(temp_file):
    assert os.path.exists(temp_file)
    
def test_file_content(temp_file):
    with open(temp_file) as f:
        content = f.read()
        assert content == "test content"
        
        