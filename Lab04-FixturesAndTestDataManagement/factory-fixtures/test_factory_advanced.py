import pytest

@pytest.fixture
def make_user():
    created = []  # track what we make for cleanup

    def _make(name, role="user"):
        user = {"name": name, "role": role, "active": True}
        created.append(user)
        return user

    yield _make

    print(f"\n[cleanup] created {len(created)} users during test")


def test_default_role(make_user):
    user = make_user("Alice")
    assert user["role"] == "user"


def test_custom_role(make_user):
    user = make_user("Bob", role="admin")
    assert user["role"] == "admin"