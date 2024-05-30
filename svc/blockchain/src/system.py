import pathlib, json, time
from threading import Thread, Lock
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
        self.data_path = None
        self.block_size = block_size
        self.root = self._initialize_system(data_directory=self.data_directory)
        self.current_block_lock: Lock = Lock()
        self.queue_lock: Lock = Lock()
        self.transactions_queue = deque()
        self.current_block: Block | None = None
        self.status: SystemStatus = SystemStatus.WAITING_FOR_BLOCK
        
    def get_current_block(self) -> Block:
        self.current_block_lock.acquire()
        block = self.current_block
        self.current_block_lock.release()
        return block
    
    def set_current_block(self, block: Block) -> None:
        self.current_block_lock.acquire()
        self.current_block = block
        self.current_block_lock.release()
        
    def _save_blockchain(self) -> None:
        with self.data_path.open('+w') as data_f:
            json.dump(self.root.model_dump(), data_f)
            
    def _append_new_block_to_end(self, block: Block) -> None:
        temp = self.root
        while temp.nextBlock:
            temp = temp.nextBlock
        temp.nextBlock = block
        
    def _initialize_system(self, data_directory: pathlib.Path) -> Block:
        self.data_path = data_directory.joinpath('chain.json')
        
        if data_directory.is_file():
            return RuntimeError('Passed value is pointing not to the directory!', str(data_directory))
        
        if not data_directory.exists():
            data_directory.mkdir()
            
        if not self.data_path.exists():
            result = Block.genesis_block()
            with self.data_path.open('+w') as data_f:
                json.dump(result.model_dump(), data_f)
            
        with self.data_path.open('r') as data_f:
            result = json.load(data_f)
        return Block(**result)
    
    def _verify_transaction(self, transaction: Transaction) -> bool:
        if calculate_balance(
            root=self.root,
            address=transaction.fromAddress
        ) >= transaction.amount:
            return True
        return False
    
    def _verify_block_validation(self, nonce: int) -> bool:
        first_zeros_num: int = 10
        block_hash_with_nonce = self.current_block.hash_with_nonce(nonce=nonce)
        result = bin(block_hash_with_nonce)[3:].zfill(32)
        if result[:first_zeros_num] == '0' * first_zeros_num:
            return True
        return False
    
    def _find_end_of_chain(self) -> Block:
        temp = self.root
        while temp.nextBlock:
            temp = temp.nextBlock
        return temp
    
    def add_transaction(self, transaction: Transaction) -> bool:
        if self._verify_transaction(transaction):
            self.queue_lock.acquire()
            self.transactions_queue.append(transaction)
            self.queue_lock.release()
            return True
        return False
    
    def extract_available_transactions(self) -> list[Transaction]:
        self.queue_lock.acquire()
        result = [
            self.transactions_queue.pop() for _ in range(len(self.transactions_queue))
        ]
        self.queue_lock.release()
        return result
    
    def add_block(self, miner_address: str, nonce: int) -> bool:
        self.current_block_lock.acquire()
        if self._verify_block_validation(nonce=nonce):
            self.current_block.currentBlockHash = hex(self.current_block.hash_with_nonce(nonce=nonce))[3:]
            self.current_block.transactions.append(
                Transaction(
                    timestamp=str(int(time.time())),
                    amount=25.0,
                    fromAddress='coinbase',
                    toAddress=miner_address,
                    signature=''
                )
            )
            self.status = SystemStatus.WAITING_FOR_BLOCK
            self._append_new_block_to_end(block=self.current_block)
            self._save_blockchain()
            self.current_block_lock.release()
            return True
        self.current_block_lock.release()
        return False
                
    def run(self) -> None: 
        while True:
            if self.status == SystemStatus.WAITING_FOR_BLOCK:
                self.set_current_block(
                    block=Block(
                        previousHash=self._find_end_of_chain().currentBlockHash,
                        transactions=self.extract_available_transactions()
                    )
                )
                self.status = SystemStatus.MINING_BLOCK
            time.sleep(1)

    