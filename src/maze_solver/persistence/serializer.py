"""Provide the functions that handles serialization of maze file.

This module allows the serialization of maze file.

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

The module contains the following functions:
- `dump_squares`: Produces the maze file.
- `serialize`: Produces a tuple consisting of the file header and body.
- `compress`: Compresses two values (square roles and square border
    value) into a single number.
- `load_squares`: Open the file for reading in binary mode to option the file
    header, obtain its file version and obtain iteration of squares.
- `deserialize`: Process the file header and body to create a iteration of
    squares.
- `decompress`: Decompress a single number to two values (square roles and
    square border value).
"""
import array
import pathlib
from typing import Iterator

from maze_solver.models.border import Border
from maze_solver.models.role import Role
from maze_solver.models.square import Square
from maze_solver.persistence.file_format import FileBody, FileHeader

FORMAT_VERSION: int = 1


def dump_squares(
    width: int, height: int, squares: tuple[Square, ...], path: pathlib.Path
) -> None:
    """Produces the maze file.

    Args:
        maze (Maze): Object that represents the maze.
        path (pathlib.Path): Path where to write the maze file.
    """
    header, body = serialize(width, height, squares)
    with path.open(mode="wb") as file:
        header.write(file)
        body.write(file)


def load_squares(path: pathlib.Path) -> Iterator[Square]:
    """Open the file for reading in binary mode to option the file header
    obtain its file version and obtain its body and returns a iteration of
    squares.

    Args:
        path (pathlib.Path): Location of the file to be opened.

    Raises:
        ValueError: Exception created when the version of the file version.

    Returns:
        Maze: Represents the object.
    """
    with path.open("rb") as file:
        header = FileHeader.read(file)
        if header.format_version != FORMAT_VERSION:
            raise ValueError("Unsupported file format version")
        body = FileBody.read(header, file)
        return deserialize(header, body)


def serialize(
    width: int, height: int, squares: tuple[Square, ...]
) -> tuple[FileHeader, FileBody]:
    """Produces a tuple consisting of the file header and body.

    Args:
        maze (Maze): Object that represents the maze.

    Returns:
        tuple[FileHeader, FileBody]: Tuple consisting of the file header and
        the file body.
    """
    header = FileHeader(FORMAT_VERSION, width, height)
    body = FileBody(array.array("B", map(compress, squares)))
    return header, body


def deserialize(header: FileHeader, body: FileBody) -> Iterator[Square]:
    """Process the file header and body to create a iteration of squares.

    Args:
        header (FileHeader): Represents the file header of the maze.
        body (FileBody): Represents the file body of the maze.

    Returns:
        Maze: Represents the maze as an object
    """
    for index, square_value in enumerate(body.square_values):
        row, column = divmod(index, header.width)
        border, role = decompress(square_value)
        yield Square(index, row, column, border, role)


def compress(square: Square) -> int:
    """Compresses two values (square roles and square border value) into a
    single number.

    Args:
        square (Square): Represents the square to be compress.

    Returns:
        int: Integer representing the square roles and border value.
    """
    return (square.role << 4) | square.border.value


def decompress(square_value: int) -> tuple[Border, Role]:
    """Decompress a single number to two values (square roles and square border
    value).

    Args:
        square_value (int): Compress value of the square,

    Returns:
        tuple[Border, Role]: Represents the border and role value of the
            square.
    """
    return Border(square_value & 0xF), Role(square_value >> 4)
