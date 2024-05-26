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
    Transaction
)


class WalletTab(QWidget):
    def __init__(self, parent: QObject | None = None) -> None:
        super(WalletTab, self).__init__(parent)
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        hbox_l = QHBoxLayout(self)
        hbox_l.addWidget(
            WalletInfoWidget(
                wallet_info=WalletInfo(
                    publicKey='vabn;ovdbno9241512',
                    privateKey='vdsoianvoiasd92314'
                )
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