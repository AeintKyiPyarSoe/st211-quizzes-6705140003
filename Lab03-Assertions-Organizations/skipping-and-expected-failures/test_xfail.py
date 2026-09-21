import pytest

@pytest.mark.xfail(reason="Known bug #123, fix pending")
def test_known_broken_feature():
    assert 1 == 2 # currently broken
    
@pytest.mark.xfail(reason="Might pass sometimes")
def test_actually_works_now():
    assert 1 == 1 #this will XPASS