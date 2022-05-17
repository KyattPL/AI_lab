import typing
import Color

class Piece:

    def __init__(self, color: Color, is_king=False) -> None:
        self.color = color
        self.is_king = is_king

    def become_king(self) -> None:
        self.is_king = True