import pytest
from mathutils import factorial

@pytest.mark.parametrize("n,expected", [
    (0,1), # 0! = 1
    (1,1), # 1! = 1
    (2,2), # 2! = 2
    (3,6), # 3! = 6
    (4,24), # 4! = 24
    (5,120), # 5! = 120
])
def test_factorial(n, expected):
    assert factorial(n) == expected