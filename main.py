import random
from datetime import datetime
from src.model import (
    Transaction,
    Block
)


if __name__ == '__main__':
    min_value: float = 0.0001
    max_value: float = 100.000
    txn_1 = Transaction(
        timestamp=datetime.now().strftime(''),
        amount=random.random() * (max_value - min_value) + min_value,
        fromWallet='vnoqdnvo3214',
        toWallet='jiapvdssjp',
        signature='1'
    )
    txn_2 = Transaction(
        timestamp=datetime.now().strftime(''),
        amount=random.random() * (max_value - min_value) + min_value,
        fromWallet='vnoqdnvo3214',
        toWallet='jiapvdssjp',
        signature='2'
    )
    txn_3 = Transaction(
        timestamp=datetime.now().strftime(''),
        amount=random.random() * (max_value - min_value) + min_value,
        fromWallet='vnoqdnvo3214',
        toWallet='jiapvdssjp',
        signature='3'
    )
    root_block = Block.genesis_block()
    block = Block(
        previousBlockHash=root_block.currentBlockHash,
        transactions=[txn_1, txn_2, txn_3]
    )
    print(
        'Hash of the block: ', block.hash()
    )