from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout
)
from .widget import (
    TransactionView,
    WalletInfoWidget
)
from ..model import WalletInfo
from ..utils import (
    get_incoming_transactions,
    get_outcoming_transactions
)


class WalletTab(QWidget):
    def __init__(self, wallet_info: WalletInfo, 
                 parent: QObject | None = None) -> None:
        super(WalletTab, self).__init__(parent)
        self.wallet_info = wallet_info
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        hbox_l = QHBoxLayout(self)
        hbox_l.addWidget(
            WalletInfoWidget(
                wallet_info=self.wallet_info
            )
        )
        hbox_l.addWidget(
            TransactionView(
                incoming_transactions=get_incoming_transactions(my_address=self.wallet_info.publicKey),
                outcoming_transactions=get_outcoming_transactions(my_address=self.wallet_info.publicKey),
                parent=self
            )
        )