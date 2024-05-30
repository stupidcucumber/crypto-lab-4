import pathlib, pydantic
from fastapi import FastAPI, Request
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
def post_transaction(transaction: Transaction) -> dict[str, bool]:
    result: bool = blockchain_system.add_transaction(
        transaction=transaction
    )
    return {
        'status': result
    }


@api.get('/blockchain/mining/block')
def get_block_to_mine() -> Block | None:
    return blockchain_system.get_current_block()
    

class BlockNonceRequest(pydantic.BaseModel):
    nonce: int
    address: str
    
@api.post('/blockchain/mining/nonce')
def post_block_nonce(request: BlockNonceRequest) -> dict[str, bool]:
    print('Request: ', request)
    result = blockchain_system.add_block(
        miner_address=request.address,
        nonce=request.nonce
    )
    print('Result: ', result)
    return {
        'status': result
    }
    