class Vector2:
    """
    A class to represent a 2D vector.

    Attributes
    ----------
    x : int
        The x-coordinate of the vector.
    y : int
        The y-coordinate of the vector.

    Methods
    -------
    __init__(x, y)
        Initializes a new instance of the Vector2 class with the given x and y coordinates.
    __add__(other)
        Adds two Vector2 instances and returns a new Vector2 instance.
    __sub__(other)
        Subtracts another Vector2 instance from this instance and returns a new Vector2 instance.
    __eq__(other)
        Checks if another Vector2 instance is equal to this instance.
    __repr__()
        Returns a string representation of the Vector2 instance.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar: int):
        return Vector2(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def as_board_space(self) -> str:
        """
        Returns the board space representation of the vector.
        """
        return f"{chr(self.x + ord('A'))}{self.y + 1}"
    
    @staticmethod
    def from_board_space(space: str) -> 'Vector2':
        """
        Converts a board space string to a Vector2 instance.
        """
        if len(space) != 2:
            raise ValueError("Invalid board space format.")
        x = ord(space[0].upper()) - ord('A')
        y = int(space[1]) - 1
        return Vector2(x, y)
    
    def in_range(self) -> bool:
        """
        Checks if the vector is within the bounds of the chess board.
        """
        return 0 <= self.x < 8 and 0 <= self.y < 8
    
    
Vector2.zero = Vector2(0, 0)
Vector2.up = Vector2(0, 1)
Vector2.down = Vector2(0, -1)
Vector2.left = Vector2(-1, 0)
Vector2.right = Vector2(1, 0)

class Board:
    def __init__(self, board: list[list]):
        self.board = board
        self.board.reverse()
        self.pieces = {}
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                if piece:
                    self.pieces[piece] = Vector2(col, row)
                    piece.place(Vector2(col, row), self)

    def display(self):
        print("  ---------------------------------")
        for i, row in enumerate(self.board[::-1]):
            print(f"{8 - i} | ", end="")
            for piece in row:
                if piece:
                    print(f"{piece} | ", end="")
                else:
                    print(f"  | ", end="")
            print()
            print("  ---------------------------------")
        print("    A   B   C   D   E   F   G   H")
        
    def __getitem__(self, position: Vector2):
        return self.board[position.y][position.x]