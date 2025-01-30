from abc import ABC, abstractmethod
import random

class Vector2:
    """
    A class to represent a 2D vector.

    Attributes
    ----------
    x : float or int
        The x-coordinate of the vector.
    y : float or int
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

    def __init__(self, x, y):
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

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
    

class Piece(ABC):
    def __init__(self, start_position: Vector2):
        self.positions = {start_position : 1}

    @abstractmethod
    def get_moves(self, position: Vector2) -> list[Vector2]:
        pass

    def get_moves_all_states(self) -> dict[list[Vector2]]:
        moves = []
        for position in self.positions:
            moves.append({position, self.get_moves(position)})
        return moves