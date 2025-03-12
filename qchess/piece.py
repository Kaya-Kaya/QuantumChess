from abc import ABC, abstractmethod
import random
from board import Vector2, Board
from colorama import Fore, Style

moveList = [Vector2.up, Vector2.right, Vector2.down, Vector2.down]

class Piece(ABC):

    def __init__(self, white: bool):
        self.board = None
        self.positions = {}
        self.white = white
        self.selected = False
        self.path = False

    def place(self, start_position: Vector2, board: Board):
        self.board = board
        self.positions = {start_position : 1}

    @abstractmethod
    def get_moves(self, position: Vector2) -> list[list[Vector2]]:
        """
        Returns a list of possible moves for the piece from the given position.
        For example, rook: [[left, left, left], [up, up, up], [right], [down, down]]
        """
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
                    if self.board[position] is not None:
                        captured = self.board[position].try_capture(position)
                        if captured:
                            self.board[position] = self
                            break

            # Remove the old position
            del self.positions[old_position]
        else:
            raise ValueError("Old position not found in the piece's positions.")
        
    def try_capture(self, position: Vector2) -> bool:
        if position in self.positions:
            exists = self.board[position].collapse(position)
            if exists:
                self.capture()
                return True
            else:
                return False
        else:
            raise ValueError("Position not found in the piece's positions.")

    def capture(self) -> None:
        if len(self.positions) == 1:
            del self.positions[(self.positions.keys())[0]]
        else:
            raise ValueError("Cannot capture a piece with multiple states.") # Why can't you capture a piece with multiple states? 
        

    def collapse(self, position: Vector2) -> bool:
        """
        Collapses one of the states.
        Returns True if this state becomes realized, False otherwise.
        """

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
        char = chr(ord(self.character()) + ((ord('Ⓐ') - ord('A')) if self.path else 0))

        if not self.selected:
            return f"{Fore.BLUE if self.white else Fore.RED}{char}{Style.RESET_ALL}"
        else:
            return f"{Fore.YELLOW if self.white else Fore.MAGENTA}{char}{Style.RESET_ALL}"

    @abstractmethod
    def character(self) -> str:
        """
        Returns the character representation of the piece.
        """
        pass


class Pawn(Piece):
    def __init__(self, white):
        super().__init__(white)
        self.moved = False

    def get_moves(self, position):
        moves = []

        for i in range(1, 3):
            pos = position + (Vector2.up if self.white else Vector2.down) * i
            
            if not pos.in_range() or (self.board[pos] is not None and (self.board[pos].white == self.white or self.board[pos].positions == 1)):
                break

            moves.append(pos)

            if self.moved:
                break
        
        for sign in range(-1, 2, 2): # For each possible sign (- and +)
            pos = position + (Vector2.up if self.white else Vector2.down) + Vector2.up * sign

        return [moves]

    def character(self):
        return "P"

class Rook(Piece):
    def __init__(self, white): # Is this needed for non-pawn pieces?
        super().__init__(white)
        self.moved = False

    def get_moves(self, position):
        moves = []
        #Ben new code

        for direction in moveList:
            for i in range(1, 8): # Can only move up to seven squares
                pos = position + direction * i

                if not pos.in_range() or (self.board[pos] is not None and (self.board[pos].white == self.white or self.board[pos].positions == 1)):
                    break

                moves.append(pos)

        return [moves]

    def character(self):
        return "R"

class Knight(Piece):
    def __init__(self, white):
        super().__init__(white)
        self.moved = False

    def get_moves(self, position):
        moves = []
        for sign in range(-1, 2, 2): # For each possible sign (- and +)
            for i in range(4):
                # Move 3 in desired direction, 1 in perpendicular direction counterclockwise if positive, clockwise if negative
                pos = position + moveList[i] * 3 + moveList[(i + 1) % 4]  * sign 

                if not pos.in_range() or (self.board[pos] is not None and (self.board[pos].white == self.white or self.board[pos].positions == 1)):
                    break

                moves.append(pos)

        return [moves]

    def character(self):
        return "N"

class Bishop(Piece):
    def __init__(self, white):
        super().__init__(white)
        self.moved = False

    def get_moves(self, position):
        moves = []

        for j in range(4):
            for i in range(1, 8): # Can only move up to seven squares
                pos = position + moveList[j] * i + moveList[(j + 1) % 4] * i

                if not pos.in_range() or (self.board[pos] is not None and (self.board[pos].white == self.white or self.board[pos].positions == 1)):
                    break

                moves.append(pos)

        return [moves]

    def character(self):
        return "B"

class Queen(Piece):
    def __init__(self, white):
        super().__init__(white)
        self.moved = False

    def get_moves(self, position):
        moves = []

        for j in range(4): # First consider diagonals
            for i in range(1, 8): # Can only move up to seven squares
                pos = position + moveList[j] * i + moveList[(j + 1) % 4] * i

                if not pos.in_range() or (self.board[pos] is not None and (self.board[pos].white == self.white or self.board[pos].positions == 1)):
                    break

                moves.append(pos)
        
        for direction in moveList: # Next, consider the horizontal and vertical directiosn
            for i in range(1, 8): # Can only move up to seven squares
                pos = position + direction * i

                if not pos.in_range() or (self.board[pos] is not None and (self.board[pos].white == self.white or self.board[pos].positions == 1)):
                    break

                moves.append(pos)

        return [moves]

    def character(self):
        return "Q"

class King(Piece):
    def __init__(self, white):
        super().__init__(white)
        self.moved = False

    def get_moves(self, position):
        moves = []

        for j in range(4): # First consider diagonals
            pos = position + moveList[j] + moveList[(j + 1) % 4] 

            if not pos.in_range() or (self.board[pos] is not None and (self.board[pos].white == self.white or self.board[pos].positions == 1)):
                break

            moves.append(pos)
        
        for direction in moveList: # Next, consider the horizontal and vertical direction
            pos = position + direction

            if not pos.in_range() or (self.board[pos] is not None and (self.board[pos].white == self.white or self.board[pos].positions == 1)):
                break

            moves.append(pos)

        return [moves]

    def character(self):
        return "K"