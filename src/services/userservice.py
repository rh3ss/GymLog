from datetime import date
from utils.dbclient import DBClient
from utils.hash import hash_password, compare_passwords

class UserService:
    def __init__(self, db: DBClient) -> None:
        self.db = db

    def user_exists(self, email: str) -> bool:
        exists = self.db._execute(
            "SELECT user_id FROM user WHERE email = ?", (email,), fetch=True
        )
        return bool(exists)

    def get_user_name(self, email: str) -> str:
        first_name = self.db._execute(
            "SELECT first_name FROM user WHERE email = ?", (email,), fetch=True
        )
        return str(first_name[0][0])

    def create_user(self, first_name: str, last_name: str, email: str, password: str, birthdate: date, height_cm: int) -> None:
        password_hash = hash_password(password)
        self.db._execute(
            "INSERT INTO user (first_name, last_name, email, password_hash, date_of_birth, height_cm) VALUES (?, ?, ?, ?, ?, ?)",
            (first_name, last_name, email, password_hash, birthdate, height_cm), commit=True
        )

    def authenticate_user(self, email: str, password: str) -> bool:
        password_hash = self.db._execute(
            "SELECT password_hash FROM user WHERE email = ?", (email,), fetch=True
        )
        if compare_passwords(password=password, hashed_password=password_hash[0][0]):
            return True
        return False
