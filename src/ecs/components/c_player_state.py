from enum import Enum


class CPlayerState:
    def __init__(self) -> None:
        self.state = PlayerState.IDLE
    
class PlayerState:
    IDLE = 0
    MOVE = 1