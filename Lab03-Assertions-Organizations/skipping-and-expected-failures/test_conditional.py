import pytest
import os

@pytest.mark.skipif(not os.path.exists("/etc/hosts"), reason="No hosts file")
def test_hosts_file():
    assert os.pa.exists("/etc/hosts")