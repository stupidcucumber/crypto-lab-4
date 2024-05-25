import hashlib
from .utils.hashable import Hashable


class Transaction(Hashable):
    timestamp: str
    amount: float
    toWallet: str
    fromWallet: str
    signature: str
    
    def __str__(self) -> str:
        return '%s %f %s %s %s' % (
            self.timestamp, self.amount, self.toWallet, self.fromWallet, self.signature
        )
    
    def hash(self) -> str:
        str_repr = str(self)
        return hashlib.sha256(str_repr.encode()).hexdigest()