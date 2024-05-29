import pathlib, json
from threading import Thread
from collections import deque
from .model import (
    Block,
    Transaction,
    SystemStatus,
    calculate_balance
)


class BlockChainSystem(Thread):
    def __init__(self, data_directory: pathlib.Path | None = None,
                 block_size: int = 2) -> None:
        super(BlockChainSystem, self).__init__()
        self.data_directory = data_directory
        self.block_size = block_size
        self.root = self._initialize_system(data_directory=self.data_directory)
        self.transactions_queue = deque()
        self.current_block: Block | None = None
        self.status: SystemStatus = SystemStatus.WAITING_FOR_BLOCK
        
    def _initialize_system(self, data_directory: pathlib.Path) -> Block:
        data_path = data_directory.joinpath('chain.json')
        
        if data_directory.is_file():
            return RuntimeError('Passed value is pointing not to the directory!', str(data_directory))
        
        if not data_directory.exists():
            data_directory.mkdir()
            result = Block.genesis_block()
            with data_path.open('+w') as data_f:
                json.dump(result, data_f)
            
        with data_path.open('r') as data_f:
            result = json.load(data_f)
        return Block(**result)
    
    def _verify_transaction(self, transaction: Transaction) -> bool:
        if calculate_balance(
            root=self.root,
            address=transaction.fromAddress
        ) >= transaction.amount:
            return True
        return False
    
    def _find_end_of_chain(self) -> Block:
        temp = self.root
        while temp.nextBlock:
            temp = temp.nextBlock
        return temp
    
    def add_transaction(self, transaction: Transaction) -> bool:
        if self._verify_transaction(transaction):
            self.transactions_queue.append(transaction)
                
    def run(self) -> None: 
        while True:
            if self.status == SystemStatus.WAITING_FOR_BLOCK:
                if len(self.transactions_queue) >= self.block_size:
                    self.current_block = Block(
                        previousHash=self._find_end_of_chain().currentBlockHash,
                        transactions=[
                            self.transactions_queue.pop() for _ in range(self.block_size)
                        ]
                    )
                    self.status = SystemStatus.MINING_BLOCK

    