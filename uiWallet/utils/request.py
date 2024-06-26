import requests, typing
from svc.blockchain.src.model import Transaction, Block


def send_request(endpoint: str, method: typing.Callable, **kwargs) -> requests.Response:
    url: str = 'http://127.0.0.1:8080' + endpoint
    response: requests.Response = method(
        url=url,
        **kwargs
    )
    response.raise_for_status()
    return response


def get_blockchain() -> Block:
    response = send_request(
        endpoint='/blockchain',
        method=requests.get
    )
    return Block(**response.json())


def get_balance(my_address: str) -> float | None:
    response = send_request(
        endpoint='/blockchain/balance',
        method=requests.get,
        params={
            'address': my_address
        }
    )
    return response.json()['balance']


def get_incoming_transactions(my_address: str) -> list[Transaction]:
    response = send_request(
        endpoint='/blockchain/toTransaction',
        method=requests.get,
        params={
            'address': my_address
        }
    )
    return [Transaction(**transaction_data) for transaction_data in response.json()]


def get_outcoming_transactions(my_address: str) -> list[Transaction]:
    response = send_request(
        endpoint='/blockchain/fromTransaction',
        method=requests.get,
        params={
            'address': my_address
        }
    )
    return [Transaction(**transaction_data) for transaction_data in response.json()]


def get_block_to_mine() -> Block:
    response = send_request(
        endpoint='/blockchain/mining/block',
        method=requests.get
    )
    return Block(**response.json())


def post_transacton(transaction: Transaction) -> bool:
    response = send_request(
        endpoint='/blockchain/transaction',
        method=requests.post,
        json=transaction.model_dump()
    )
    return response.json()['status']
    
    
def post_block_nonce(my_address: str, nonce: int) -> bool:
    response = send_request(
        endpoint='/blockchain/mining/nonce',
        method=requests.post,
        json={
            'address': my_address,
            'nonce': nonce
        }
    )
    return response.json()['status']