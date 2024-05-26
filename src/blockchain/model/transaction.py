import hashlib
from .utils.hashable import Hashable
from .utils import (
    build_merkel_tree,
    Node
)


class InputPoint(Hashable):
    blockHash: str
    transactionHash: str
    outputIndex: int
    amount: float
    
    def __str__(self) -> str:
        return '%s %s %d %f' % (
            self.blockHash,
            self.transactionHash,
            self.outputIndex,
            self.amount
        )


class OutputPoint(Hashable):
    toAddress: str
    amount: float
    
    def __str__(self) -> str:
        return '%s %f' % (
            self.toAddress,
            self.amount
        )


class Transaction(Hashable):
    timestamp: str
    amount: float
    fromAddress: str
    toAddress: str
    signature: str
    inputs: list[InputPoint] | None = None
    outputs: list[OutputPoint] | None = None
    inputMerkelTree: Node | None = None
    outputMerkelTree: Node | None = None
    
    def __str__(self) -> str:
        return '%s %f %s %s %s' % (
            self.timestamp, self.amount, self.inputs, self.outputs, self.signature
        )
        
    def add_txn_input(self, txn_in: InputPoint) -> None:
        self.inputMerkelTree = None
        self.inputs.append(txn_in)
    
    def add_txn_out(self, txn_out: OutputPoint) -> None:
        self.outputMerkelTree = None
        self.outputs.append(txn_out)
        
    def hash(self) -> str:
        if not self.inputMerkelTree:
            self.inputMerkelTree = build_merkel_tree(
                hashes=[
                    txn_in.hash() for txn_in in self.inputs
                ]
            )
        if not self.outputMerkelTree:
            self.outputMerkelTree = build_merkel_tree(
                hashes=[
                    txn_out.hash() for txn_out in self.outputs
                ]
            )
        return hashlib.sha256(
            (self.inputMerkelTree.hashValue + self.outputMerkelTree.hashValue).encode()
        ).hexdigest()
    
