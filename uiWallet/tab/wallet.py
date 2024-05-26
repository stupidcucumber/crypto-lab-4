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
from svc.blockchain.src.model import (
    Transaction,
    Block
)


class WalletTab(QWidget):
    def __init__(self, blockchain_root: Block, wallet_info: WalletInfo, 
                 parent: QObject | None = None) -> None:
        super(WalletTab, self).__init__(parent)
        self.blockchain_root = blockchain_root
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
                transactions=[
                    Transaction(
                        timestamp='10-10-10',
                        amount=321.0,
                        fromAddress='fijpaf',
                        toAddress='nvioenavoid',
                        signature='fnoavifdn'
                    )
                ],
                parent=self
            )
        )