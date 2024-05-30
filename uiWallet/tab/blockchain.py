from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)
from PyQt6.QtGui import QFontMetrics, QFont
from ..utils import get_blockchain
from svc.blockchain.src.model import Block, Transaction


class BlockWidget(QWidget):
    def __init__(self, block: Block, parent: QObject | None = None) -> None:
        super(BlockWidget, self).__init__(parent)
        self.block = block
        self._setup_layout()
        
    def _create_elided_label(self, text: str, width: int = 300, parent: QObject | None = None) -> QLabel:
        label = QLabel(parent)
        label.setMaximumWidth(width)
        fm = QFontMetrics(QFont('Arial', 10))
        elided_text = fm.elidedText(
            text, Qt.TextElideMode.ElideMiddle, width
        )
        label.setText(elided_text)
        return label
        
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
            self._create_elided_label('From address: %s' % transaction.fromAddress, parent=widget)
        )
        layout.addWidget(
            self._create_elided_label('To address: %s' % transaction.toAddress, parent=widget)
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
            self._create_elided_label(
                text='Previous hash: %s' % self.block.previousHash,
                parent=self
            )
        )
        layout.addWidget(
            self._create_elided_label(
                text='Current hash: %s' % self.block.currentBlockHash,
                parent=self
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