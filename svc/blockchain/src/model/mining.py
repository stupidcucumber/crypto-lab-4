import enum


class SystemStatus(enum.IntEnum):
    WAITING_FOR_BLOCK: int = 0
    MINING_BLOCK: int = 0
    