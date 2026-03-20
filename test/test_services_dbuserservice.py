import sys, os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.dbclient import DBClient
from services.dbuserservice import DBUserService


def test_dbuserservices():
    dbfilename = f"test_services_{os.getpid()}.db"
    db = DBClient(dbfilename)
    service = DBUserService(db=db)

    service.create_user(
        first_name="Test",
        last_name="User",
        email="test@user.com",
        password="secret_password",
        birthdate="2000-01-01",
        height_cm=180,
    )

    user_exists = service.user_exists(email="test@user.com")
    assert user_exists is True

    user = service.get_user(email="test@user.com")
    assert user is not None

    user_auth = service.authenticate_user(
        email="test@user.com", password="secret_password"
    )
    assert user_auth is True

    assert user["first_name"] == "Test"
