from typing import Optional


class DatabaseException(Exception):
    message: Optional[str]

    def __init__(self, message: Optional[str] = None):
        self.message = message or "Database error"
        super().__init__(self.message)

class DatabaseWriteException(DatabaseException):
    pass

class DatabaseReadException(DatabaseException):
    pass
