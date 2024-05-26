from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QTabWidget
)
from ..tab import (
    WalletTab
)
from ..model import WalletInfo


class MainWindow(QMainWindow):
    def __init__(self, wallet_info: WalletInfo, width: int = 1400, height: int = 800):
        super(MainWindow, self).__init__()
        self.wallet_info = wallet_info
        self.setGeometry(0, 0, width, height)
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        tabbar = QTabWidget(self)
        tabbar.addTab(
            WalletTab(blockchain_root=None, wallet_info=self.wallet_info, parent=self),
            'Wallet'
        )
        tabbar.addTab(
            QWidget(),
            'Blockchain'    
        ),
        tabbar.addTab(
            QWidget(),
            'Mining'
        )
        self.setCentralWidget(tabbar)
        