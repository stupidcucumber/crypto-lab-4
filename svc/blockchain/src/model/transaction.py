import hashlib
from .utils.hashable import Hashable
from .utils import (
    build_merkel_tree,
    Node
)

class Transaction(Hashable):
    timestamp: str
    amount: float
    fromAddress: str
    toAddress: str
    signature: str
    merkelTree: Node
    
    def __str__(self) -> str:
        return '%s %f %s %s %s' % (
            self.timestamp, self.amount, self.fromAddress, self.toAddress, self.signature
        )
        
    def hash(self) -> str:
        if not self.merkelTree:
            hashes = [
                hashlib.sha256(self.timestamp.encode()).hexdigest(),
                hashlib.sha256(str(self.amount).encode()).hexdigest(),
                hashlib.sha256(self.fromAddress.encode()).hexdigest(),
                hashlib.sha256(self.toAddress.encode()).hexdigest(),
                hashlib.sha256(self.signature.encode()).hexdigest()
            ]
            self.merkelTree = build_merkel_tree(hashes=hashes).hashValue
        return self.merkelTree.hashValue



        