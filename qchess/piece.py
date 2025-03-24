from abc import ABC, abstractmethod
import random
from board import Vector2, Board
from colorama import Fore, Style

class Piece(ABC):

    def __init__(self, white: bool):
        self.board = None
        self.positions = {}
        self.white = white
        self.selected = False

    def place(self, start_position: Vector2, board: Board):
        self.board = board
        self.positions = {start_position : 1}

    @abstractmethod
    def get_moves(self, position: Vector2) -> list[list[Vector2]]:
        """
        Returns a list of possible move paths for the piece from the given position.
        """
        pass

    def get_moves_all_states(self) -> dict[Vector2, list[Vector2]]:
        moves = []
        for position in self.positions:
            moves.append({position, self.get_moves(position)})
        return moves

    def move(self, old_position: Vector2, new_positions: list[list[Vector2]]):
        if old_position in self.positions:
            # Remove the old position
            self.board[old_position] = None
            probability = self.positions[old_position]
            del self.positions[old_position]

            for path in new_positions:
                final_position = old_position
                for position in path:
                    if self.board[position] is not None:
                        captured = self.board[position].try_capture(position)
                        if captured:
                            final_position = position
                            break
                    else:
                        final_position = position
                    
                self.board[final_position] = self
                if final_position not in self.positions:
                    self.positions[final_position] = probability / len(new_positions)
                else:
                    self.positions[final_position] += probability / len(new_positions)
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
            del self.positions[list(self.positions.keys())[0]]
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
        
    def path_char(self):
        return f"{Fore.YELLOW if self.white else Fore.MAGENTA}{self.character()}{Style.RESET_ALL}"

    def __repr__(self):
        return f"{Fore.BLUE if self.white else Fore.RED}{self.character()}{Style.RESET_ALL}"

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
            
            if not pos.in_range() or (self.board[pos] is not None and len(self.board[pos].positions) == 1):
                break

            moves.append(pos)

            if self.moved:
                break
        
        for sign in range(-1, 2, 2): # For each possible sign (- and +)
            pos = position + (Vector2.up if self.white else Vector2.down) + Vector2.up * sign

        return [moves]
    
    def move(self, old_position, new_positions):
        super().move(old_position, new_positions)
        self.moved = True

    def character(self):
        return "P"

class Rook(Piece):
    def get_moves(self, position):
        moves = []
        #Ben new code

        for direction in Vector2.directions:
            move_set = []
            for i in range(1, 8): # Can only move up to seven squares
                pos = position + direction * i

                if not pos.in_range():
                    break
                elif self.board[pos] is not None and len(self.board[pos].positions) == 1:
                    if self.white != self.board[pos].white:
                        move_set.append(pos)
                    break

                move_set.append(pos)
            if len(move_set) > 0:
                moves.append(move_set)

        return moves

    def character(self):
        return "R"

class Knight(Piece):
    def get_moves(self, position):
        moves = []
        for sign in range(-1, 2, 2): # For each possible sign (- and +)
            for i in range(4):
                # Move 2 in desired direction, 1 in perpendicular direction counterclockwise if positive, clockwise if negative
                pos = position + Vector2.directions[i] * 2 + Vector2.directions[(i + 1) % 4]  * sign 

                if pos.in_range() and (self.board[pos] is None or len(self.board[pos].positions) != 1 
                                       or self.white != self.board[pos].white):
                    moves.append(pos)

        return [moves]

    def character(self):
        return "N"

class Bishop(Piece):
    def get_moves(self, position):
        moves = []

        for j in range(4):
            move_set = []
            for i in range(1, 8): # Can only move up to seven squares
                pos = position + Vector2.directions[j] * i + Vector2.directions[(j + 1) % 4] * i

                if not pos.in_range():
                    break
                elif self.board[pos] is not None and len(self.board[pos].positions) == 1:
                    if self.white != self.board[pos].white:
                        move_set.append(pos)
                    break

                move_set.append(pos)

            if len(move_set) > 0:
                moves.append(move_set)

        return moves

    def character(self):
        return "B"

class Queen(Piece):
    def get_moves(self, position):
        moves = []

        for j in range(4): # First consider diagonals
            move_set = []
            for i in range(1, 8): # Can only move up to seven squares
                pos = position + Vector2.directions[j] * i + Vector2.directions[(j + 1) % 4] * i

                if not pos.in_range():
                    break
                elif self.board[pos] is not None and len(self.board[pos].positions) == 1:
                    if self.white != self.board[pos].white:
                        move_set.append(pos)
                    break

                move_set.append(pos)

            if len(move_set) > 0:
                moves.append(move_set)
        
        for direction in Vector2.directions: # Next, consider the horizontal and vertical directions
            move_set = []
            for i in range(1, 8): # Can only move up to seven squares
                pos = position + direction * i

                if not pos.in_range():
                    break
                elif self.board[pos] is not None and len(self.board[pos].positions) == 1:
                    if self.white != self.board[pos].white:
                        move_set.append(pos)
                    break

                move_set.append(pos)
            
            if len(move_set) > 0:
                moves.append(move_set)

        return moves

    def character(self):
        return "Q"

class King(Piece):
    def get_moves(self, position):
        moves = []

        for j in range(4): # First consider diagonals
            pos = position + Vector2.directions[j] + Vector2.directions[(j + 1) % 4] 

            if pos.in_range() and (self.board[pos] is None or len(self.board[pos].positions) != 1 
                                   or self.white != self.board[pos].white):
                moves.append(pos)
        
        for direction in Vector2.directions: # Next, consider the horizontal and vertical direction
            pos = position + direction

            if pos.in_range() and (self.board[pos] is None or len(self.board[pos].positions) != 1 
                                   or self.white != self.board[pos].white):
                moves.append(pos)

        return [moves]

    def character(self):
        return "K"