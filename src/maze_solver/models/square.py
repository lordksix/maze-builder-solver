"""Provide the classes that handles the squares square of tha maze.

This module allows to create and handle squares square of tha maze.

The module contains the following class:
- Square:`: A immutable class that represents a square in the maze
"""

from dataclasses import dataclass

from maze_solver.models.border import Border
from maze_solver.models.role import Role


@dataclass(frozen=True)
class Square:
    """An immutable Class that handles the squares of the maze. It requires a
    row and column, which are integers, for positioning. It requires a
    border attribute which represents what kind of borders it has, a role
    attribute which represents the role of the square. By default the role is
    NONE. It also requires a integer index for a one dimensional sequences of
    squares.

    Attributes:
        index: int
            Represents the position of the square in the maze, base on
            one-dimensional sequence of square.
        row: int
            Represents the position of the square in the maze, base on
            Y positioning.
        column: int
            Represents the position of the square in the maze, base on
            X positioning.
        border: Border
            Represents borders of the square.
        role: Role = Role.NONE
            Represents the role of the square. Defaults to NONE.
    """

    index: int
    row: int
    column: int
    border: Border
    role: Role = Role.NONE
