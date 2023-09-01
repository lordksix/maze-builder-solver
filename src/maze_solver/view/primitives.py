"""Provide the classes and functions that handles the creation of xml tags for
rendering.

This module allows the creation of xml tags for rendering.

Examples:

    >>> from maze_solver.view.primitives import tag

    >>> # Element name
    >>> tag("svg")
    '<svg />'

    >>> # Element name and value
    >>> tag("svg", "Your web browser doesn't support SVG")
    "<svg>Your web browser doesn't support SVG</svg>"

    >>> # Element name and attributes (including one with a hyphen)
    >>> tag("svg", xmlns="http://www.w3.org/2000/svg", stroke_linejoin="round")
    '<svg xmlns="http://www.w3.org/2000/svg" stroke-linejoin="round" />'

    >>> # Element name, value, and attributes
    >>> tag("svg", "SVG not supported", width="100%", height="100%")
    '<svg width="100%" height="100%">SVG not supported</svg>'

    >>> # Nested elements
    >>> tag("svg", tag("rect", fill="blue"), width="100%")
    '<svg width="100%"><rect fill="blue" /></svg>'

The module contains the following classes:
- `Primitive`:A class that represents a geometric primitive and extends the
    protocol class.
- `Point`: A class that represents a point primitive in a 2D plane.
- `Line`: A class that represents a line primitive in a 2D plane.
- `Polyline`: A class that represents a polyline primitive in a 2D plane.
- `Polygon`: A class that represents a polygon primitive in a 2D plane.
- `DisjointLines`: A class that represents a logical collection of lines
    with no SVG equivalent.
- `Rect`: A immutable class that represents a rectangle.
- `Text`: A immutable class that represents a text.
- `NullPrimitive`: A immutable class that represents a Null geometric
    primitive.

The module contains the following functions:
- `tag`: A function that checks  that its first square is
    the maze entrance, the last square is the exit, and every two consecutive
    squares belong to the same row or column.
"""
from dataclasses import dataclass
from typing import NamedTuple, Protocol


class Primitive(Protocol):
    """A class that represents a interface for all geometric primitives and
    extends the protocol class. Used to type checker.

    Methods:
        draw(self, **attributes) -> str:
            A method to draw the geometric primitive as svg.
    """

    def draw(self, **attributes) -> str:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """
        return ""

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


class Point(NamedTuple):
    """A class that represents a point primitive in a XY Euclidean plane.
    Extends NamedTuple.

    Args:
        x: int
            Represents the position of the point on the X-axis
        y: int
            Represents the position of the point on the Y-axis

    Methods:
        draw(self, **attributes) -> str:
            A method to create a SVG Point.
        translate(self, x=0, y=0) -> "Point":
            A method to create a point the translated position.
    """

    x: int
    y: int

    def draw(self) -> str:
        """A method to represent a SVG point.

        Returns:
            str: A SVG point.
        """
        return f"{self.x},{self.y}"

    def translate(self, x_pos=0, y_pos=0) -> "Point":
        """A method to create a point the translated position.

        Args:
            x (int, optional): Units to translate X. Defaults to 0.
            y (int, optional): Units to translate Y. Defaults to 0.

        Returns:
            Point: A point on the new X, Y position
        """
        return Point(self.x + x_pos, self.y + y_pos)

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


class Line(NamedTuple):
    """A class that represents a line primitive in a XY Euclidean Line.
    Extends NamedTuple.

    Args:
        start: Point
            Represents the start point of the line
        end: Point
            Represents the end point of the line

    Methods:
        draw(self, **attributes) -> str:
            A method to create a SVG Line.
    """

    start: Point
    end: Point

    def draw(self, **attributes) -> str:
        """A method to represent a SVG Line.

        Returns:
            str: A SVG line.
        """
        return tag(
            "line",
            x1=self.start.x,
            y1=self.start.y,
            x2=self.end.x,
            y2=self.end.y,
            **attributes,
        )

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


class Polyline(tuple[Point, ...]):
    """A class that represents a polyline primitive in a XY Euclidean Line.
    It a group of point primitives that together forms continuous lines, that
    doesn't close.

    Args:
        tuple (Point, ...): A tuple of points

    Methods:
        draw(self, **attributes) -> str:
            A method to represent a SVG polyline.
    """

    def draw(self, **attributes) -> str:
        """A method to represent a SVG polyline.

        Returns:
            str: A SVG line.
        """
        points = " ".join(point.draw() for point in self)
        return tag("polyline", points=points, **attributes)

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


class Polygon(tuple[Point, ...]):
    """A class that represents a polygon primitive in a XY Euclidean Line.
    It a group of point primitives that together forms continuous lines, that
    closes.

    Args:
        tuple (Point, ...): A tuple of points

    Methods:
        draw(self, **attributes) -> str:
            A method to represent a SVG polygon.
    """

    def draw(self, **attributes) -> str:
        """A method to represent a SVG polygon.

        Returns:
            str: A SVG line.
        """
        points = " ".join(point.draw() for point in self)
        return tag("polygon", points=points, **attributes)

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


class DisjointLines(tuple[Line, ...]):
    """A class that represents a DisjointLines primitive in a XY Line.
    It a logical collection of lines.

    Args:
        tuple (Point, ...): A tuple of points

    Methods:
        draw(self, **attributes) -> str:
            A method to represent a SVG DisjointLines.
    """

    def draw(self, **attributes) -> str:
        """A method to represent a SVG DisjointLines.

        Returns:
            str: A string of all lines together
        """
        return "".join(line.draw(**attributes) for line in self)

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


@dataclass(frozen=True)
class Rect:
    """A immutable class that represents a rectangle. Extends dataclass.

    Attributes:
        top_left: Point | None = None
            Represents the first point, top left, of the rectangle.
    """

    top_left: Point | None = None

    def draw(self, **attributes) -> str:
        """A method to represent a SVG representation of a rectangle.

        Returns:
            str: A SVG rectangle.
        """
        if self.top_left:
            attrs = attributes | {"x": self.top_left.x, "y": self.top_left.y}
        else:
            attrs = attributes
        return tag("rect", **attrs)

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


@dataclass(frozen=True)
class Text:
    """A immutable class that represents a text. Extends dataclass.

    Attributes:
        content: str
            Represents the text to be printed.
        point: Point
            Represents the position where to start.

    """

    content: str
    point: Point

    def draw(self, **attributes) -> str:
        """A method to represent a SVG representation of a text.

        Returns:
            str: A SVG text.
        """
        return tag("text", self.content, x=self.point.x, y=self.point.y, **attributes)

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


class NullPrimitive:
    """A class that represents a null geometric primitive.

    Methods:
        draw(self, **attributes) -> str:
            A method to represent the null primitive.
    """

    def draw(self, **attributes) -> str:
        """A method to represent the null primitive.

        Returns:
            str: A SVG text.
        """
        return ""

    def placeholder(self, **attributes) -> None:
        """A method to represent the geometric primitive.

        Returns:
            str: _description_
        """


def tag(name: str, value: str | None = None, **attributes) -> str:
    """Creates XML tag elements from a name, an optional value, and key-value
    attributes.

    Args:
        name (str): Represents the name of the XML tag.
        value (str | None, optional): Represents the value of the tag.
            Defaults to None.

    Returns:
        str: A complete XML tag as a string
    """
    attrs = (
        ""
        if not attributes
        else " "
        + " ".join(
            f'{key.replace("_", "-")}=' + f'"{value}"'
            for key, value in attributes.items()
        )
    )
    if value is None:
        return f"<{name}{attrs} />"
    return f"<{name}{attrs}>{value}</{name}>"
