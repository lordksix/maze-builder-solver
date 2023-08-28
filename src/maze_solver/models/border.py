"""Provide the classes that handles borders to each node of the maze.

This module allows to assign borders to each node of the maze.

Examples:

    >>> from maze_solver.models.border import Border

    >>> border = Border.TOP | Border.BOTTOM | Border.RIGHT | Border.LEFT

    >>> border
    <Border.TOP|BOTTOM|LEFT|RIGHT: 15>

    >>> border.name
    'TOP|BOTTOM|LEFT|RIGHT'

    >>> border.value
    15
    >>> Border.TOP | Border.BOTTOM
    <Border.TOP|BOTTOM: 3>

    >>> Border.BOTTOM | Border.TOP
    <Border.TOP|BOTTOM: 3>

    >>> border is Border.TOP | Border.BOTTOM | Border.RIGHT | Border.LEFT
    True
    >>> border is Border.TOP
    False

    >>> border == 15
    True
    >>> border == 16
    False

    >>> Border.TOP in border
    True

The module contains the following class:
- `Border(IntFlag):`: A class that represents a enum for the roles
"""

from enum import IntFlag, auto


class Border(IntFlag):
    """A class that handles the border of each node or square in the maze.
        It can be an EMPTY, TOP, BOTTOM, LEFT, or RIGHT.
        Extends IntFlag class from enum module, it can use bitwise operations.

    Attributes:
        EMPTY = 0
            Represents no border.
        TOP = auto()
            Represents top border.
        BOTTOM = auto()
            Represents bottom border.
        LEFT = auto()
            Represents left border.
        RIGHT = auto()
            Represents right border.

    Methods:
        corner(self) -> bool:
            Getter method to verify if it has a corner border.
        dead_end(self) -> bool:
            Getter method to verify if it has a dead end border.
        intersection(self) -> bool:
            Getter method to verify if it is an intersection.
    Returns:
        (Border): It can be an EMPTY, TOP, BOTTOM, LEFT, or RIGHT.
    """

    EMPTY = 0
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()

    @property
    def corner(self) -> bool:
        """Getter method to verify if it has a corner border.

        Returns:
            bool: True if it has a corner border or false if not.
        """
        return self in (
            self.TOP | self.LEFT,
            self.TOP | self.RIGHT,
            self.BOTTOM | self.LEFT,
            self.BOTTOM | self.RIGHT,
        )

    @property
    def dead_end(self) -> bool:
        """Getter method to verify if it has a dead end border.

        Returns:
            bool: True if it has a dead end border or false if not.
        """
        return self.bit_count() == 3

    @property
    def intersection(self) -> bool:
        """Getter method to verify if it is an intersection.

        Returns:
            bool: True if it is an intersection or false if not.
        """
        return self.bit_count() < 2
