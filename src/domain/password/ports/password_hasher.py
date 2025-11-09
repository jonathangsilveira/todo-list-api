from abc import ABC, abstractmethod


class PasswordHasher(ABC):

    @abstractmethod
    def generate_hash(self, password: bytes, salt: bytes) -> bytes:
        pass

    @abstractmethod
    def generate_salt(self, rounds: int) -> bytes:
        pass

    @abstractmethod
    def check_password(self, password: bytes, hashed_password: bytes) -> bool:
        pass