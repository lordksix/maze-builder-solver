"""Provide the functions that handles maze file format.

This module allows the creation of maze file header.

The module contains the following classes:
- `FileHeader`: A class that represents the header of the maze file.
    the border of the square in SVG.
- `FileBody`: A class that represents the body of the maze file.
"""
import array
import struct
from dataclasses import dataclass
from typing import BinaryIO

MAGIC_NUMBER: bytes = b"MAZE"


@dataclass(frozen=True)
class FileHeader:
    """A class that represents the header of the maze file.

    Methods:
        - read(cls, file: BinaryIO) -> "FileHeader":
            A class method that read a binary file to get the maze
            file header.
        - write(self, file: BinaryIO) -> None:
            Writes its own content into a supplied binary file.
    """

    format_version: int
    width: int
    height: int

    @classmethod
    def read(cls, file: BinaryIO) -> "FileHeader":
        """A class method that read a binary file to get the maze
        file header.

        Args:
            file (BinaryIO): Binary file that is read to get the
                FileHeader object.

        Returns:
            FileHeader: Instance of the FileHeader class with the
                information from the file.
        """
        assert (
            file.read(len(MAGIC_NUMBER)) == MAGIC_NUMBER
        ), "Unknown file type"  # one line
        (format_version,) = struct.unpack("B", file.read(1))
        width, height = struct.unpack("<2I", file.read(2 * 4))
        return cls(format_version, width, height)

    def write(self, file: BinaryIO) -> None:
        """Writes its own content into a supplied binary file.

        Args:
            file (BinaryIO): Binary file where FileHeader object writes
                its content.
        """
        file.write(MAGIC_NUMBER)
        file.write(struct.pack("B", self.format_version))
        file.write(struct.pack("<2I", self.width, self.height))


@dataclass(frozen=True)
class FileBody:
    """A class that represents the body of the file.

    Methods:
        - read(cls, header: FileHeader, file: BinaryIO) -> "FileBody":
            A class method that read a binary file to get the maze
            file body.
        - write(self, file: BinaryIO) -> None:
            Writes its own content into a supplied binary file.
    """

    square_values: array.array

    @classmethod
    def read(cls, header: FileHeader, file: BinaryIO) -> "FileBody":
        """A class method that read a binary file to get the maze
            file body.

        Args:
            header (FileHeader): Represents the header of the maze file.
            file (BinaryIO): Binary file that is read to get the
                FileBody object.

        Returns:
            FileBody: Representation of the FileBody
        """
        return cls(array.array("B", file.read(header.width * header.height)))

    def write(self, file: BinaryIO) -> None:
        """Writes its own content into a supplied binary file.

        Args:
            file (BinaryIO): Binary file where FileObject object writes
                its content.
        """
        file.write(self.square_values.tobytes())
