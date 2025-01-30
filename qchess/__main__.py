from piece import *
from board import *

if __name__ == "__main__":
    start_board = [[Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False), Rook(False)],
                   [Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False), Pawn(False)],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [None, None, None, None, None, None, None, None],
                   [Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True), Pawn(True)],
                   [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)]]
    
    board = Board(start_board)
    board.display()