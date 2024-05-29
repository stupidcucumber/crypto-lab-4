from .transaction import Transaction
from .block import Block


def find_transactions_to_address(root: Block, to_address: str) -> list[Transaction]:
    result = []
    temp = root
    while temp:
        for transaction in temp.transactions:
            if transaction.toAddress == to_address:
                result.append(transaction)
        temp = temp.nextBlock
    return result


def find_transactions_from_address(root: Block, from_address: str) -> list[Transaction]:
    result = []
    temp = root
    while temp:
        for transaction in temp.transactions:
            if transaction.fromAddress == from_address:
                result.append(transaction)
        temp = temp.nextBlock
    return result


def calculate_balance(root: Block, address: str) -> float:
    to_address_transactions = find_transactions_to_address(root=root, to_address=address)
    from_address_transactions = find_transactions_from_address(root=root, from_address=address)
    total_income = sum([transaction.amount for transaction in to_address_transactions])
    total_outcome = sum([transaction.amount for transaction in from_address_transactions])
    return total_income - total_outcome