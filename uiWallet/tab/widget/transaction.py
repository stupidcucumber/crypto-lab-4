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
    def __init__(self, transaction: Transaction, incoming: bool, parent: QObject | None = None) -> None:
        super(TransactionWidget, self).__init__(parent)
        self.transaction = transaction
        self.incoming: bool = incoming
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel('To address: %s' % self.transaction.toAddress)
        )
        amount_label = QLabel('Amount: %f' % self.transaction.amount)
        amount_label.setStyleSheet('color: %s;' % ('green' if self.incoming else 'red'))
        layout.addWidget(
            amount_label
        )
        layout.addWidget(
            QLabel('Timestamp: %s' % self.transaction.timestamp)
        )
        
        
class TransactionView(QScrollArea):
    def __init__(self, incoming_transactions: list[Transaction], outcoming_transactions: list[Transaction], parent: QObject | None = None) -> None:
        super(TransactionView, self).__init__(parent)
        self.incoming_transactions = incoming_transactions
        self.outcoming_transactions = outcoming_transactions
        self._setup_layout()
    
    def _setup_layout(self) -> None:
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        transaction_widgets: list[TransactionWidget] = []
        for transaction in self.incoming_transactions:
            transaction_widgets.append(
                TransactionWidget(
                    transaction=transaction,
                    incoming=True,
                    parent=widget
                )
            )
        for transaction in self.outcoming_transactions:
            transaction_widgets.append(
                TransactionWidget(
                    transaction=transaction,
                    incoming=False,
                    parent=widget
                )
            )
        transaction_widgets = sorted(
            transaction_widgets,
            key=lambda widget: int(widget.transaction.timestamp)
        )
        for transaction_widget in transaction_widgets:
            layout.addWidget(transaction_widget)
        self.setWidget(
            widget
        )