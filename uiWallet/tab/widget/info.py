from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)
from PyQt6.QtGui import QFontMetrics, QFont
from ...model import WalletInfo


class WalletInfoWidget(QWidget):
    def __init__(self, wallet_info: WalletInfo, parent: QObject | None = None) -> None:
        super(WalletInfoWidget, self).__init__(parent)
        self.wallet_info = wallet_info
        self._setup_layout()
        
    def _create_key_label(self, key: str, name: str) -> QLabel:
        label = QLabel(self)
        label.setMaximumWidth(300)
        fm = QFontMetrics(QFont('Arial', 10))
        elided_text = fm.elidedText(
            '%s: %s' % (name, key), Qt.TextElideMode.ElideMiddle, 300
        )
        label.setText(elided_text)
        return label
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(
            self._create_key_label(key=self.wallet_info.publicKey, name='Public key')
        )
        layout.addWidget(
            self._create_key_label(key=self.wallet_info.privateKey, name='Private key')
        )
        