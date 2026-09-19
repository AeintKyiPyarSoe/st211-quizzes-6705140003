import pytest
from calculator import divide

def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(10, 0)
        
def test_divide_by_zero_raises_with_message():
    with pytest.raises(ValueError, match = "Cannot be divided by zero"):
        divide(5, 0)