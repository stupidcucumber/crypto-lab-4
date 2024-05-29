import pathlib
from fastapi import FastAPI
from src import BlockChainSystem
from src.model import (
    Block,
    Transaction,
    SystemStatus,
    find_transactions_to_address,
    find_transactions_from_address,
    calculate_balance
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


@api.get('/blockchain/balance')
def get_balance(address: str) -> dict[str, float]:
    balance: float = calculate_balance(
        root=blockchain_system.root,
        address=address
    )
    return {
        'balance': balance
    }


@api.get('/blockchain/toTransaction')
def get_transactons_to_address(address: str) -> list[Transaction]:
    return find_transactions_to_address(
        root=blockchain_system.root,
        to_address=address
    )


@api.get('/blockchain/fromTransaction')
def get_transactions_from_address(address: str) -> list[Transaction]:
    return find_transactions_from_address(
        root=blockchain_system.root,
        from_address=address
    )


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
def post_block_nonce(minerAddress: str, nonce: int) -> dict[str, bool]:
    result = blockchain_system.add_block(
        miner_address=minerAddress,
        nonce=nonce
    )
    return {
        'status': result 
    }
