from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QTabWidget
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._setup_layout()
        
    def _setup_layout(self) -> None:
        tabbar = QTabWidget(self)
        tabbar.addTab(
            QWidget(),
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
        