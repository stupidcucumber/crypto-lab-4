import pathlib
from fastapi import FastAPI
from src import BlockChainSystem
from src.model import (
    Block,
    Transaction,
    SystemStatus
)


api = FastAPI()
blockchain_system = BlockChainSystem(
    data_directory=pathlib.Path('data')
)
blockchain_system.start()


@api.get('/')
def check_health():
    return {
        'status': 'ok'
    }
    
    
@api.get('/blockchain')
def get_blockchain() -> Block:
    return blockchain_system.root


@api.post('/blockchain/transaction')
def post_transaction(transaction: Transaction) -> Transaction | None:
    result: bool = blockchain_system.add_transaction(
        transaction=transaction
    )
    if result:
        return transaction
    return {
        'status': 'Bad transaction.'
    }


@api.get('/blockchain/mining/block')
def get_block_to_mine() -> Block:
    if blockchain_system.status == SystemStatus.MINING_BLOCK:
        return blockchain_system.current_block
    return {
        'status': 'no blocks to mine at the moment.'
    }
    

@api.post('/blockchain/mining/nonce')
def post_block_nonce() -> None:
    pass