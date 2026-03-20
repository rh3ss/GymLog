import sys, os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.hash import hash_password, compare_passwords


def test_hash_and_compare():
    password = "supersecret123"
    hashed = hash_password(password)

    assert isinstance(hashed, str)

    assert len(hashed) > 0

    assert compare_passwords(password, hashed) is True

    assert compare_passwords("wrongpassword", hashed) is False
