from typing import Optional


class DatabaseException(Exception):
    details: Optional[str]

    def __init__(self, details: Optional[str] = None):
        self.details = details or "Database error"
        super().__init__(self.details)

class DatabaseWriteException(DatabaseException):
    pass

class DatabaseReadException(DatabaseException):
    pass
