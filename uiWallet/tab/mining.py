import threading, enum, typing, itertools
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton
)
from svc.blockchain.src.model import (
    Block
)
from .blockchain import BlockWidget
from ..model import WalletInfo
from ..utils import (
    post_block_nonce,
    get_block_to_mine
)


class MiningState(enum.IntEnum):
    STOP: int = 0
    MINE: int = 1
    CHECK_BLOCK: int = 2
    WAIT_NEW: int = 3


class MinerThread(threading.Thread):
    def __init__(self, wallet_info: WalletInfo, updating_fn: typing.Callable) -> None:
        super(MinerThread, self).__init__()
        self.wallet_info = wallet_info
        self.block: Block = get_block_to_mine()
        self.updating_fn: typing.Callable = updating_fn
        self.counter = itertools.count()
        self.lock: threading.Lock = threading.Lock() 
        self.state: MiningState = MiningState.MINE
    
    def get_state(self) -> MiningState:
        self.lock.acquire()
        state = self.state
        self.lock.release()
        return state
    
    def set_state(self, state: MiningState) -> None:
        self.lock.acquire()
        self.state = state
        self.lock.release()
    
    def stop_mining(self) -> None:
        self.set_state(state=MiningState.STOP)
        
    def _guess_nonce(self) -> None:
        first_zeros_num: int = 3
        nonce = next(self.counter)
        hash_with_nonce = self.block.hash_with_nonce(nonce=nonce)
        result = bin(hash_with_nonce)[3:].zfill(32)
        if result[:first_zeros_num] == '0' * first_zeros_num:
            guessed: int = post_block_nonce(
                my_address=self.wallet_info.publicKey,
                nonce=nonce
            )
            return guessed
        return False
    
    def _check_block(self) -> bool:
        new_block = get_block_to_mine()
        if new_block.previousHash == self.block.previousHash:
            return True
        return False
        
    def run(self) -> None:
        check_every: int = 200
        step_counter: int = itertools.count()
        while True:
            step = next(step_counter)
            if self.get_state() == MiningState.MINE:
                guessed = self._guess_nonce()
                if guessed:
                    self.counter = itertools.count()
                    self.block = get_block_to_mine()
                    self.set_state(MiningState.WAIT_NEW)
                if step % check_every == 0:
                    self.set_state(MiningState.CHECK_BLOCK)
            elif self.get_state() == MiningState.CHECK_BLOCK:
                is_same: bool = self._check_block()
                if not is_same:
                    self.block = get_block_to_mine()
                    self.counter = itertools.count()
                self.set_state(MiningState.MINE)
            elif self.get_state() == MiningState.STOP:
                break
            elif self.get_state() == MiningState.WAIT_NEW:
                if not self._check_block():
                    self.block = get_block_to_mine()
                    self.set_state(MiningState.MINE)
        self.updating_fn()
            

class MinerTab(QWidget):
    def __init__(self, wallet_info: WalletInfo, parent: QObject | None = None) -> None:
        super(MinerTab, self).__init__(parent)
        self.wallet_info = wallet_info
        self.miner_thread: MinerThread | None = None
        self._setup_layout()
        
    def _start_mining(self) -> None:
        self.miner_thread = MinerThread(wallet_info=self.wallet_info, updating_fn=self._setup_layout)
        self.miner_thread.start()
        self._setup_layout()
        
    def _stop_mining(self) -> None:
        self.miner_thread.stop_mining()
        self.miner_thread = None
        self._setup_layout()
        
    def _instantiate_start_mining_button(self) -> QPushButton:
        button = QPushButton('Start Mining', self)
        button.pressed.connect(
            self._start_mining
        )
        return button
        
    def _instantiate_stop_mining_button(self) -> QPushButton:
        button = QPushButton('Stop Mining', self)
        button.pressed.connect(
            self._stop_mining
        )
        return button
        
    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        if self.miner_thread:
            layout.addWidget(
                BlockWidget(block=self.miner_thread.block, parent=self)
            )
        layout.addWidget(self._instantiate_start_mining_button())
        layout.addWidget(self._instantiate_stop_mining_button())