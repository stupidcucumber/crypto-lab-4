import time
from typing import Callable
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMainWindow,
    QLineEdit
)
from PyQt6.QtGui import QFontMetrics, QFont
from ...model import WalletInfo
from ...utils import (
    get_balance,
    post_transacton,
    sign_transaction
)
from svc.blockchain.src.model import Transaction


class TransactionWindow(QMainWindow):
    def __init__(self, wallet_info: WalletInfo, parent: QObject | None = None) -> None:
        super(TransactionWindow, self).__init__(parent)
        self.setGeometry(400, 400, 600, 400)
        self.wallet_info = wallet_info
        self.current_recipient: str = ''
        self.current_amount: float = 0.000
        self.line_edit_address = self._setup_inputs(slot=lambda e: self._set_recipient(e))
        self.line_edit_amount = self._setup_inputs(slot=lambda e: self._set_amount(e))
        self.setWindowTitle('Transaction')
        self._setup_layout()
        
    def close_window(self) -> None:
        self.current_recipient = ''
        self.line_edit_address.setText('')
        self.line_edit_amount.setText('0') 
        self.close()
        
    def _set_recipient(self, address: str) -> None:
        self.current_recipient = address
        
    def _set_amount(self, amount: str) -> None:
        self.current_amount = float(amount)
        
    def _send_transaction(self) -> None:
        transaction = Transaction(
            timestamp=str(int(time.time())),
            amount=self.current_amount,
            fromAddress=self.wallet_info.publicKey,
            toAddress=self.current_recipient,
            signature=''
        )
        sign_transaction(private_key_str=self.wallet_info.privateKey, transaction=transaction)
        result = post_transacton(
            transaction=transaction
        )
        if result:
            self.close_window()
        else:
            print('Quite sad :(')
        
    def _setup_inputs(self, slot: Callable) -> QLineEdit:
        line_edit = QLineEdit(self)
        line_edit.textChanged.connect(slot)
        return line_edit
        
    def _instantiate_cancel_button(self) -> QPushButton:
        button = QPushButton('Cancel', self)
        button.pressed.connect(
            lambda: self.close_window()
        )
        return button
    
    def _instantiate_send_button(self) -> QPushButton:
        button = QPushButton('Send', self)
        button.pressed.connect(
            lambda: self._send_transaction()
        )
        return button
    
    def _instantiate_controls(self) -> QWidget:
        widget = QWidget(self)
        layout = QHBoxLayout(widget)
        layout.addWidget(
            self._instantiate_send_button()
        )
        layout.addWidget(
            self._instantiate_cancel_button()
        )
        return widget
    
    def _setup_layout(self) -> None:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(
            QLabel('Public address of the recipient:', widget)
        )
        layout.addWidget(self.line_edit_address)
        layout.addWidget(
            QLabel('Amount to send: ', widget)
        )
        layout.addWidget(self.line_edit_amount)
        layout.addWidget(
            self._instantiate_controls()
        )
        self.setCentralWidget(widget)


class WalletInfoWidget(QWidget):
    def __init__(self, wallet_info: WalletInfo, parent: QObject | None = None) -> None:
        super(WalletInfoWidget, self).__init__(parent)
        self.wallet_info = wallet_info
        self.balance = get_balance(
            my_address=self.wallet_info.publicKey
        )
        self.transaction_window = TransactionWindow(wallet_info=wallet_info, parent=self)
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
    
    def _instantiate_create_transaction_button(self) -> QPushButton:
        button = QPushButton('Create transaction', self)
        button.pressed.connect(
            lambda: self.transaction_window.show()
        )
        return button
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel('Your current balance is: %.4f' % self.balance)
        )
        layout.addWidget(
            self._create_key_label(key=self.wallet_info.publicKey, name='Public key')
        )
        layout.addWidget(
            self._create_key_label(key=self.wallet_info.privateKey, name='Private key')
        )
        layout.addWidget(
            self._instantiate_create_transaction_button()
        )
        