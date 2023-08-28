"""Provide the classes that handles roles for the maze.

This module allows to assign roles to each node of the maze.

Examples:

    >>> from maze_solver.models.role import Role

    >>> Role.ENEMY
    <Role.ENEMY: 1>

    >>> Role.ENEMY.value
    1

    >>> Role.ENEMY + 42
    43

The module contains the following class:
- `Role(IntEnum):`: A class that represents a enum for the roles
"""

from enum import IntEnum, auto


class Role(IntEnum):
    """A class that handles the role of each node or square in the maze.
        It can be an NONE, ENEMY, ENTRANCE, EXIT, EXTERIOR, REWARD, or WALL.
        Extends StrEnum class from enum module.

    Attributes:
        NONE = 0
            Represents no role.
        ENEMY = auto()
            Represents enemy role.
        ENTRANCE = auto()
            Represents entrance role.
        EXIT = auto()
            Represents exit role.
        EXTERIOR = auto()
            Represents exterior role.
        REWARD = auto()
            Represents reward role.
        WALL = auto()
            Represents wall role.

    Returns:
        (Role): It can be an NONE, ENEMY, ENTRANCE, EXIT, EXTERIOR, REWARD, or
            WALL.
    """

    NONE = 0
    ENEMY = auto()
    ENTRANCE = auto()
    EXIT = auto()
    EXTERIOR = auto()
    REWARD = auto()
    WALL = auto()
