from __future__ import annotations
import hashlib
from .transaction import Transaction
from .utils import (
    build_merkel_tree,
    Node,
    Hashable
)


class Block(Hashable):
    previousBlockHash: str
    transactions: list[Transaction]
    currentBlockHash: str | None = None
    merkelTree: Node | None = None
    
    @staticmethod
    def genesis_block() -> Block:
        return Block(
            previousBlockHash=''.join(['0'] * 256),
            transactions=[],
            currentBlockHash=''.join(['0'] * 256)
        )
        
    def add_transaction(self, transaction: Transaction) -> str:
        self.merkelTree = None
        self.transactions.append(transaction)
    
    def hash(self) -> str:
        if not self.merkelTree:
            self.merkelTree = build_merkel_tree(
                hashes=[
                    transaction.hash() for transaction in self.transactions
                ]
            )
            self.currentBlockHash = hashlib.sha256(
                (self.merkelTree.hashValue + self.previousBlockHash).encode()
            ).hexdigest()
        return self.currentBlockHash