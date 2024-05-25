from pydantic import BaseModel


class Hashable(BaseModel):
    def hash(self) -> str:
        raise NotImplementedError()