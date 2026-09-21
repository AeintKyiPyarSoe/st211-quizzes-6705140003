import pytest

@pytest.mark.nonexistent_marker
def test_bad_marker():
    assert True