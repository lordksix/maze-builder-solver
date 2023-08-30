"""Provide the classes that handles the maze.

This module allows to create and manage the maze.

The module contains the following class:
- `Solution`: A class that handles the maze.

The module contains the following functions:
- `validate_corridor`: A function that checks  that its first square is
    the maze entrance, the last square is the exit, and every two consecutive
    squares belong to the same row or column.
"""

from dataclasses import dataclass
from functools import reduce
from typing import Iterator

from maze_solver.models.role import Role
from maze_solver.models.square import Square


@dataclass(frozen=True)
class Solution:
    """A class that handles the solution of the maze.

    Attributes:
        squares: tuple[Square, ...]
            Represents all squares of the Maze

    Methods:
        width(self):
            A cached getter method to print the width of the maze.
        height(self):
            A cached getter method to print the height of the maze.
        entrance(self) -> Square:
            A cached getter method to get the square with ENTRANCE role.
        exit(self) -> Square:
            A cached getter method to get the square with EXIT role.

    Returns:
        (Maze): Composed of a tuple of squares.
    """

    squares: tuple[Square, ...]

    def __post_init__(self) -> None:
        assert self.squares[0].role is Role.ENTRANCE
        assert self.squares[-1].role is Role.EXIT
        reduce(validate_corridor, self.squares)

    def __iter__(self) -> Iterator[Square]:
        return iter(self.squares)

    def __getitem__(self, index: int) -> Square:
        return self.squares[index]

    def __len__(self) -> int:
        return len(self.squares)


def validate_corridor(current: Square, following: Square) -> Square:
    """A function that checks  that its first square is the maze entrance,
    the last square is the exit, and every two consecutive squares belong
    to the same row or column.

    Args:
        current (Square): Current square to be evaluated
        following (Square): Following square to be evaluated.

    Returns:
        Square: Following square to be evaluated.
    """
    assert any(
        [current.row == following.row, current.column == following.column]
    ), "Squares must lie in the same row or column"
    return following
