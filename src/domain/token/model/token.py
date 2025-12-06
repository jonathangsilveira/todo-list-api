import uuid
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(eq=True, frozen=True)
class JwtPayload:
    sub: str
    exp: datetime
    iat: datetime = datetime.now(tz=timezone.utc)
    jti: str = str(uuid.uuid4())