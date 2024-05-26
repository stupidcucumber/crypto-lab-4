import sys, json, pathlib
from uiWallet.model import WalletInfo
from PyQt6.QtWidgets import QApplication
from uiWallet.window import MainWindow

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def generate_rsa_key_pair() -> WalletInfo:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return WalletInfo(
        privateKey=private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).hex(),
        publicKey=public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()
    )


def load_wallet_info(path: pathlib.Path) -> WalletInfo:
    if not path.exists():
        wallet_info = generate_rsa_key_pair()
        with path.open('+w') as wallet_f:
            json.dump(wallet_info.model_dump(), wallet_f, indent=4)
        return wallet_info
    with path.open('r') as wallet_f:
        data = json.load(wallet_f)
    return WalletInfo(**data) 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow(
        wallet_info=load_wallet_info(
            path=pathlib.Path('data', 'wallet_info.json')
        )
    )
    mainWindow.show()
    sys.exit(app.exec())