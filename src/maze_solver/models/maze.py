"""Provide the classes that handles the maze.

This module allows to create and manage the maze.

Examples:

    >>> from pathlib import Path
    >>> from maze_solver.models.maze import Maze
    >>> from maze_solver.models.border import Border
    >>> from maze_solver.models.role import Role
    >>> from maze_solver.models.square import Square
    >>> from maze_solver.persistence.serializer import dump

    >>> maze = Maze(
    ...     squares=(
    ...         Square(0, 0, 0, Border.TOP | Border.LEFT),
    ...         Square(1, 0, 1, Border.TOP | Border.RIGHT),
    ...         Square(2, 0, 2, Border.LEFT | Border.RIGHT, Role.EXIT),
    ...         Square(3, 0, 3, Border.TOP | Border.LEFT | Border.RIGHT),
    ...         Square(4, 1, 0, Border.BOTTOM | Border.LEFT | Border.RIGHT),
    ...         Square(5, 1, 1, Border.LEFT | Border.RIGHT),
    ...         Square(6, 1, 2, Border.BOTTOM | Border.LEFT),
    ...         Square(7, 1, 3, Border.RIGHT),
    ...         Square(8, 2, 0, Border.TOP | Border.LEFT, Role.ENTRANCE),
    ...         Square(9, 2, 1, Border.BOTTOM),
    ...         Square(10, 2, 2, Border.TOP | Border.BOTTOM),
    ...         Square(11, 2, 3, Border.BOTTOM | Border.RIGHT),
    ...     )
    ... )

    >>> maze.dump("miniature.maze")
    >>> path = Path("miniature.maze")
    >>> Maze.load(path) == maze
    True

    >>> Maze.load(path) is maze
    False

    >>> maze = Maze.load(path)

    >>> maze.width, maze.height
    (4, 3)

    >>> len(maze.squares)
    12

    >>> maze.entrance
    Square(index=8,
        row=2,
        column=0,
        border=<Border.TOP|LEFT: 5>,
        role=<Role.ENTRANCE: 2>)

    >>> maze.exit
    Square(index=2,
        row=0,
        column=2,
        border=<Border.LEFT|RIGHT: 12>,
        role=<Role.EXIT: 3>)



The module contains the following class:
- `Maze`: A class that handles the maze.

The module contains the following functions:
- `validate_indices`: A function that checks if the index in a square fits.
- `validate_rows_columns`: A function that handles the maze.
- `validate_entrance`: A function that checks if there is one entrance.
- `validate_exit`: A function that checks if there is one entrance.
"""

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterator

from maze_solver.models.role import Role
from maze_solver.models.square import Square
from maze_solver.persistence.serializer import dump_squares, load_squares


@dataclass(frozen=True)
class Maze:
    """A class that handles the maze.

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
        load(cls, path: Path) -> "Maze":
            A class method to load a maze file.
        dump(self, path: Path) -> None:
            A method that writes a file in the path given.

    Returns:
        (Maze): Composed of a tuple of squares.
    """

    squares: tuple[Square, ...]

    def __post_init__(self) -> None:
        validate_indices(self)
        validate_rows_columns(self)

    def __iter__(self) -> Iterator[Square]:
        return iter(self.squares)

    def __getitem__(self, index: int) -> Square:
        return self.squares[index]

    @classmethod
    def load(cls, path: Path) -> "Maze":
        """A class method to load a maze file.

        Args:
            path (Path): Path to file to be loaded

        Returns:
            Maze: Object that represents the object
        """
        return Maze(tuple(load_squares(path)))

    @cached_property
    def width(self):
        """A cached getter method to print the width of the maze.

        Returns:
            void: Prints the width of the maze.
        """
        return max(square.column for square in self) + 1

    @cached_property
    def height(self):
        """A cached getter method to print the height of the maze.

        Returns:
            void: Prints the height of the maze.
        """
        return max(square.row for square in self) + 1

    @cached_property
    def entrance(self) -> Square:
        """A cached getter method to get the square with ENTRANCE role.

        Returns:
            Square: The square with ENTRANCE role.
        """
        return next(sq for sq in self if sq.role is Role.ENTRANCE)

    @cached_property
    def exit(self) -> Square:
        """A cached getter method to get the square with EXIT role.

        Returns:
            Square: The square with EXIT role.
        """
        return next(sq for sq in self if sq.role is Role.EXIT)

    def dump(self, path: Path) -> None:
        """A method that writes a file in the path given.

        Args:
            path (Path): A path where the file will be located.
        """
        dump_squares(self.width, self.height, self.squares, path)


def validate_indices(maze: Maze) -> None:
    """Checks whether the .index property of each square
    fits into a continuous sequence of numbers that enumerates
    all the squares in the maze.

    Args:
        maze (Maze): Represents the maze to be validated.
    """
    assert [square.index for square in maze] == list(
        range(len(maze.squares))
    ), "Wrong square.index"


def validate_rows_columns(maze: Maze) -> None:
    """Iterates over the squares in the maze, ensuring
    that the .row and .column attributes of the corresponding
    square match up with the current row and column of the loops.

    Args:
        maze (Maze): Represents the maze to be validated.
    """
    for y_height in range(maze.height):
        for x_width in range(maze.width):
            square = maze[y_height * maze.width + x_width]
            assert square.row == y_height, "Wrong square.row"
            assert square.column == x_width, "Wrong square.column"


def validate_entrance(maze: Maze) -> None:
    """Iterates over the squares in the maze, ensuring
    that there is only one entrance.

    Args:
        maze (Maze): Represents the maze to be validated.
    """
    assert 1 == sum(
        1 for square in maze if square.role is Role.ENTRANCE
    ), "Must be exactly one entrance"


def validate_exit(maze: Maze) -> None:
    """Iterates over the squares in the maze, ensuring
    that there is only one exit.

    Args:
        maze (Maze): Represents the maze to be validated.
    """
    assert 1 == sum(
        1 for square in maze if square.role is Role.EXIT
    ), "Must be exactly one exit"
