import pytest
from mathutils import is_even

@pytest.mark.parametrize("number", [2,4,6,8,100])
def test_even_numbers(number):
    assert is_even(number) == True # every value in the list must be even, so is_even should return True
    
@pytest.mark.parametrize("number", [1,3,5,7,99])
def test_odd_numbers(number):
    assert is_even(number) == False # odd number in is_even should return False