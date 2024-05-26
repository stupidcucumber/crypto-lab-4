from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea
)
from svc.blockchain.src.model import (
    Transaction
)


class TransactionWidget(QWidget):
    def __init__(self, transaction: Transaction, parent: QObject | None = None) -> None:
        super(TransactionWidget, self).__init__(parent)
        self.transaction = transaction
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel('To address: %s' % self.transaction.toAddress)
        )
        layout.addWidget(
            QLabel('Amount: %f' % self.transaction.amount)
        )
        layout.addWidget(
            QLabel('Timestamp: %s' % self.transaction.timestamp)
        )
        
        
class TransactionView(QScrollArea):
    def __init__(self, transactions: list[Transaction], parent: QObject | None = None) -> None:
        super(TransactionView, self).__init__(parent)
        self.transactions = transactions
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        for transaction in self.transactions:
            layout.addWidget(
                TransactionWidget(transaction=transaction, parent=widget)
            )
        self.setWidget(
            widget
        )