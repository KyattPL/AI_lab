import typing
import Color

class Piece:

    def __init__(self, color: Color) -> None:
        self.color = color
        self.is_king = False

    def become_king(self) -> None:
        self.is_king = True