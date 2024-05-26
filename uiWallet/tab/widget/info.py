from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)
from ...model import WalletInfo


class WalletInfoWidget(QWidget):
    def __init__(self, wallet_info: WalletInfo, parent: QObject | None = None) -> None:
        super(WalletInfoWidget, self).__init__(parent)
        self.wallen_info = wallet_info
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel('Public Key: %s' % self.wallen_info.publicKey, self)
        )
        layout.addWidget(
            QLabel('Private Key: %s' % self.wallen_info.privateKey, self)
        )
        