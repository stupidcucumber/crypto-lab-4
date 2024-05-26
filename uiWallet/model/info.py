from pydantic import BaseModel


class WalletInfo(BaseModel):
    publicKey: str
    privateKey: str