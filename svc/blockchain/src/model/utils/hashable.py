import hashlib
from pydantic import BaseModel


class Hashable(BaseModel):
    def __str__(self) -> str:
        raise NotImplementedError()
    
    def hash(self) -> str | None:
        raise hashlib.sha256(str(self).encode()).hexdigest()