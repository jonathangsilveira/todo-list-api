from src.domain.password.ports.password_hasher import PasswordHasher


class PasswordService:

    """
    Use salt from 10 to 14 length to avoid taking too long to check password.
    Higher numbers are more secure by it costs performance to check hashed passwords.
    """
    def __init__(self, hasher: PasswordHasher, salt_length: int, encoding: str = "utf-8"):
        self._hasher = hasher
        self._salt_length = salt_length
        self._encoding = encoding

    def generate_hash(self, password: str) -> str:
        password_bytes = password.encode(encoding=self._encoding)
        salt = self._hasher.generate_salt(rounds=self._salt_length)
        hashed_password = self._hasher.generate_hash(password_bytes, salt)
        return hashed_password.decode(encoding=self._encoding)

    def is_valid_password(self, password: str, hashed_password: str) -> bool:
        encoded_hashed_password = hashed_password.encode(encoding=self._encoding)
        encoded_password = password.encode(encoding=self._encoding)
        return self._hasher.check_password(encoded_password, encoded_hashed_password)
