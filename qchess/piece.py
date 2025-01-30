from abc import ABC, abstractmethod
import random
from board import Vector2, Board
from colorama import Fore, Style

class Piece(ABC):
    def __init__(self, white: bool):
        self.board = None
        self.positions = {}
        self.white = white

    def place(self, start_position: Vector2, board: Board):
        self.board = board
        self.positions = {start_position : 1}

    @abstractmethod
    def get_moves(self, position: Vector2) -> list[list[Vector2]]:
        '''
        Returns a list of possible moves for the piece from the given position.
        For example, rook: [[left, left, left], [up, up, up], [right], [down, down]]
        '''
        pass

    def get_moves_all_states(self) -> dict[Vector2, list[Vector2]]:
        moves = []
        for position in self.positions:
            moves.append({position, self.get_moves(position)})
        return moves

    def move(self, old_position: Vector2, new_positions: list[list[Vector2]]):
        if old_position in self.positions:
            for path in new_positions:
                for position in path:
                    pass

            # Remove the old position
            del self.positions[old_position]
        else:
            raise ValueError("Old position not found in the piece's positions.")
        

    def capture(self):
        if len(self.positions) == 1:
            del self.positions[(self.positions.keys())[0]]
        else:
            raise ValueError("Cannot capture a piece with multiple states.")
        

    def collapse(self, position: Vector2) -> bool:
        '''
        Collapses one of the states.
        Returns True if this state becomes realized, False otherwise.
        '''

        if position in self.positions:
            probability = self.positions[position]

            if random.random() >= probability:
                # Remove this position and update probabilities
                del self.positions[position]
                for pos in self.positions:
                    self.positions[pos] /= 1 - probability
                return False
            else:
                self.positions = {position: 1}
                return True
        else:
            raise ValueError("Position not found in the piece's positions.")
        
    def __repr__(self):
        return f"{Fore.BLUE if self.white else Fore.RED}{self.character()}{Style.RESET_ALL}"

    @abstractmethod
    def character(self) -> str:
        '''
        Returns the character representation of the piece.
        '''
        pass

class Pawn(Piece):
    def get_moves(self, position):
        pass

    def character(self):
        return "P"

class Rook(Piece):
    def get_moves(self, position):
        pass

    def character(self):
        return "R"

class Knight(Piece):
    def get_moves(self, position):
        pass

    def character(self):
        return "N"

class Bishop(Piece):
    def get_moves(self, position):
        pass

    def character(self):
        return "B"

class Queen(Piece):
    def get_moves(self, position):
        pass

    def character(self):
        return "Q"

class King(Piece):
    def get_moves(self, position):
        pass

    def character(self):
        return "K"