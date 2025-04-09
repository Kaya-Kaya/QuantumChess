from board import *
from piece import Piece
from colorama import Fore, Style
import itertools

class Game:
    def __init__(self, board: Board, player_white: bool = True):
        self.player_white = player_white
        self.board = board

    def parse_input(self, input_str: str) -> Vector2:
        """
        Converts a board piece from string to a vector.
        """
        if ((len(input_str) != 2) or not (input_str[0] >= 'A' and input_str[0] <= 'H') 
                                  or not (input_str[1] >= '1' and input_str[1] <= '8')):
            raise ValueError("Invalid input. Should be [A-H][1-8].\n")
            
        return Vector2(ord(input_str[0]) - ord('A'), ord(input_str[1]) - ord('1'))

    def select_piece(self, is_white: bool) -> tuple[Piece, Vector2]:
        """
        Takes in user input specifying which piece they would like to move.
        """
        print(f"It's {Fore.BLUE if is_white else Fore.RED}{"white" if is_white else "black"}{Style.RESET_ALL}'s turn!")
        
        valid_input = False

        while not valid_input:
            piece_pos = input("Enter position of piece: ")
            try:
                pos_vec = self.parse_input(piece_pos)
                piece = self.board[pos_vec]
                if (piece is None):
                    print("There's no piece there.\n")
                elif ((is_white and not piece.white) or (not is_white and piece.white)):
                    print("That's the opponent's piece.\n")
                elif len(piece.get_moves(pos_vec)) == 0:
                    print("That piece can't be moved.\n")
                else:
                    valid_input = True
            except ValueError as e:
                print(e)
        
        return (piece, pos_vec)
    
    def move_piece(self, piece: Piece, pos: Vector2, is_white: bool):
        moves = piece.get_moves(pos)
        move_positions = list(itertools.chain.from_iterable(moves))
        self.board.display(move_positions, is_white)
        moves_to_make = []
        done = False

        for i in range(len(move_positions)):
            valid_input = False
            while not valid_input:
                piece_pos = input("Enter move position: ")
                try:
                    pos_vec = self.parse_input(piece_pos)
                    if pos_vec not in move_positions:
                        print("You can't move that piece there.\n")
                    else:
                        for move_list in moves:
                            if pos_vec in move_list:
                                moves_to_make.append(move_list[:move_list.index(pos_vec) + 1])
                                break
                        valid_input = True
                except ValueError as e:
                    print(e)

            
            if i != len(move_positions) - 1:
                while True:
                    more = input("Would you like to split into more moves (y/n)? ")
                    if more == 'y':
                        break
                    elif more == 'n':
                        done = True
                        break

                if done:
                    break

        piece.move(pos, moves_to_make)

    def turn(self, is_white: bool):
        self.board.display()

        piece, pos = self.select_piece(is_white)
        piece.selected = True

        self.move_piece(piece, pos, is_white)
        piece.selected = False

    def start(self):
        try:
            while True:
                # White's turn
                self.turn(True)

                # Black's turn
                self.turn(False)
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            