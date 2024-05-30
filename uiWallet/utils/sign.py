from svc.blockchain.src.model import Transaction
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


def sign_transaction(private_key_str: str, transaction: Transaction) -> None:
    number = int(private_key_str, 16)
    private_key = load_pem_private_key(
        data=number.to_bytes((number.bit_length() + 7) // 8, 'big'),
        password=None,
        backend=default_backend()
    )
    signature = private_key.sign(
        transaction.hash().encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    transaction.signature = signature.hex()