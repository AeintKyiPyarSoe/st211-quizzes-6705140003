import pytest
import sys

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    assert False # would fail if run, but is skipped
    
@pytest.mark.skipif(sys.version_info < (3,8), reason="Require Python 3.8+")
def test_needs_modern_python():
    assert True