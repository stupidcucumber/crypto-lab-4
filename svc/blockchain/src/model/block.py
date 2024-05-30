from __future__ import annotations
import hashlib, time
from .transaction import Transaction
from .utils import (
    build_merkel_tree,
    Node,
    Hashable
)


class Block(Hashable):
    previousHash: str
    currentBlockHash: str | None = None
    transactions: list[Transaction]
    nextBlock: Block | None = None
    merkelTree: Node | None = None
    
    @staticmethod
    def genesis_block() -> Block:
        return Block(
            previousHash=''.join(['0'] * 256),
            transactions=[],
            currentBlockHash=''.join(['0'] * 256)
        )
        
    def add_transaction(self, transaction: Transaction) -> str:
        self.merkelTree = None
        self.transactions.append(transaction)
        
    def merkelTreeHash(self) -> str:
        if not self.merkelTree:
            self.merkelTree = build_merkel_tree(
                hashes=[
                    transaction.hash() for transaction in self.transactions
                ]
            )
        return self.merkelTree.hashValue
    
    def hash_with_nonce(self, nonce: int) -> int:
        previous_hash = self.previousHash
        merkele_tree_hash = self.merkelTreeHash()
        nonce_hash = hashlib.sha256(nonce.to_bytes(256, 'big')).hexdigest()
        current_hash = hashlib.sha256(
            (previous_hash + merkele_tree_hash + nonce_hash).encode()
        ).hexdigest()
        return int(current_hash, base=16)
    
    def hash(self) -> str | None:
        return self.currentBlockHash
