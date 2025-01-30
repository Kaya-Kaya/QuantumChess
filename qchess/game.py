from board import Board

class Game:
    def __init__(self, board: Board, player_white: bool = True):
        self.player_white = player_white
        self.board = board

    def start(self):
        while True:
            self.board.display()
            raise NotImplementedError