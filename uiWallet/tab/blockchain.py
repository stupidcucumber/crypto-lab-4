from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)
from ..utils import get_blockchain
from svc.blockchain.src.model import Block, Transaction


class BlockWidget(QWidget):
    def __init__(self, block: Block, parent: QObject | None = None) -> None:
        super(BlockWidget, self).__init__(parent)
        self.block = block
        self._setup_layout()
        
    def _create_transaction_widget(self, transaction: Transaction) -> QWidget:
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        layout.addWidget(
            QLabel('Timestamp: %s' % transaction.timestamp, widget)
        )
        layout.addWidget(
            QLabel('Amount: %f' % transaction.amount, widget)
        )
        layout.addWidget(
            QLabel('From address: %s' % transaction.fromAddress, widget)
        )
        layout.addWidget(
            QLabel('To Address: %s' % transaction.toAddress, widget)
        )
        layout.addWidget(
            QLabel('Signature: %s' % transaction.signature, widget)
        )
        return widget
        
    def _create_scrollable_transaction_area(self, transactions: list[Transaction]) -> QScrollArea:
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        for transaction in transactions:
            layout.addWidget(
                self._create_transaction_widget(transaction=transaction)
            )
        
        scrollArea = QScrollArea(self)
        scrollArea.setWidget(widget)
        return scrollArea
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel('Block', self)
        )
        layout.addWidget(
            QLabel(
                'Previous hash: %s' % self.block.previousHash, 
                self
            )
        )
        layout.addWidget(
            QLabel(
                'Current hash: %s' % self.block.currentBlockHash,
                self
            )
        )
        layout.addWidget(
            self._create_scrollable_transaction_area(
                transactions=self.block.transactions
            )
        )


class BlockchainTab(QScrollArea):
    def __init__(self, parent: QObject | None = None) -> None:
        super(BlockchainTab, self).__init__(parent)
        self.blockchain_root = get_blockchain()
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        temp = self.blockchain_root
        widget = QWidget()
        layout = QHBoxLayout(widget)
        while temp:
            layout.addWidget(
                BlockWidget(block=temp, parent=widget)
            )
            temp = temp.nextBlock
        self.setWidget(widget)