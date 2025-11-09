import bcrypt

from src.domain.password.ports.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):

    def generate_hash(self, password: bytes, salt: bytes) -> bytes:
        return bcrypt.hashpw(password, salt)

    def generate_salt(self, rounds: int) -> bytes:
        return bcrypt.gensalt(rounds=rounds)

    def check_password(self, password: bytes, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password, hashed_password)