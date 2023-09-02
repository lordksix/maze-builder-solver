"""Provide the classes and functions that handles the creation of xml tags for
rendering.

This module allows the creation of xml tags for rendering.

Examples:

    >>> from pathlib import Path

    >>> from maze_solver.models.border import Border
    >>> from maze_solver.models.maze import Maze
    >>> from maze_solver.models.role import Role
    >>> from maze_solver.models.solution import Solution
    >>> from maze_solver.models.square import Square
    >>> from maze_solver.view.renderer import SVGRenderer, SVG

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

    >>> solution = Solution(squares=[maze[i] for i in (8, 11, 7, 6, 2)])

    >>> renderer = SVGRenderer()
    >>> renderer.render(maze).preview()
    >>> renderer.render(maze, solution).preview()

    >>> from maze_solver.view.renderer import SVG
    >>> svg = SVG('<svg><rect width="30" height="20" fill="red" /></svg>')
    >>> print(svg.html_content)

The module contains the following classes:
- `SVG`: A class that represents the xml content in string.
- `SVGRenderer`: A class that handles the svg rendering of maze and its
    solution.

The module contains the following functions:
- `tag`: A function that checks  that its first square is
    the maze entrance, the last square is the exit, and every two consecutive
    squares belong to the same row or column.
- `arrow_marker`: The <defs> and <marker> elements define an arrow shape that
    you'll reference later in the SVG document.
"""
import tempfile
import textwrap
import webbrowser
from dataclasses import dataclass

from maze_solver.models.maze import Maze
from maze_solver.models.role import Role
from maze_solver.models.solution import Solution
from maze_solver.models.square import Square
from maze_solver.view.decomposer import decompose
from maze_solver.view.primitives import Point, Polyline, Rect, Text, tag

ROLE_EMOJI = {
    Role.ENTRANCE: "\N{pedestrian}",
    Role.EXIT: "\N{chequered flag}",
    Role.ENEMY: "\N{ghost}",
    Role.REWARD: "\N{white medium star}",
}


@dataclass(frozen=True)
class SVG:
    """A class that represents the xml content in string.

    Methods:
        - html_content(self) -> str:
            Presents XML content in a minimal HTML website.
        - preview(self) -> None:
            Opens the HTML content in a temporary file.
    """

    xml_content: str

    @property
    def html_content(self) -> str:
        """s XML content in a minimal HTML website.

        Returns:
            str: Return HTML text of the maze
        """
        return textwrap.dedent(
            """\
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>SVG Preview</title>
        </head>
        <body>
        {0}
        </body>
        </html>"""
        ).format(self.xml_content)

    def preview(self) -> None:
        """Opens the HTML content in a temporary file."""
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", suffix=".html", delete=False
        ) as file:
            file.write(self.html_content)
        webbrowser.open(f"file://{file.name}")


@dataclass(frozen=True)
class SVGRenderer:
    """A class that handles the svg rendering of maze and its solution.

    Attributes:
        square_size: int
            Represents the size of the side of the square. Defaults to 100
        line_width: int
            Represents the width of the line of each border. Defaults to 6
    Methods:
        offset(self):
            Getter of the width of the line drawn.
        render(self, maze: Maze, solution: Solution | None = None) -> SVG:
            Creates a string that represents the maze and its solution in SVG
            tags for XML.
        exit(self) -> Square:
            A cached getter method to get the square with EXIT role.
    """

    square_size: int = 100
    line_width: int = 6

    @property
    def offset(self):
        """Getter of the width of the line drawn.

        Returns:
            int: Return the with of the line
        """
        return self.line_width // 2

    def render(self, maze: Maze, solution: Solution | None = None) -> SVG:
        """Creates a string that represents the maze and its solution in SVG
        tags for XML. Used to see the maze on a web browser.

        Args:
            maze (Maze): A class that handles and represent the maze
            solution (Solution | None, optional): Solution to the maze.
                Defaults to None.

        Returns:
            SVG: Represents the xml content in string.
        """
        margins = 2 * (self.offset + self.line_width)
        width = margins + maze.width * self.square_size
        height = margins + maze.height * self.square_size
        return SVG(
            tag(
                "svg",
                self._get_body(maze, solution),
                xmlns="http://www.w3.org/2000/svg",
                stroke_linejoin="round",
                width=width,
                height=height,
                viewBox=f"0 0 {width} {height}",
            )
        )

    def _get_body(self, maze: Maze, solution: Solution | None) -> str:
        """Private method to get the body of the svg tag. It consist of the
        markers,  which is used to end the line representing the solution
        with an arrow pointing towards the exit, a rectangle follow by the
        entire view to provide a white background. Next, it is rendered the
        individual squares and overlay them with the solution if supplied.

        Args:
            maze (Maze): A class that handles and represent the maze
            solution (Solution | None): Solution to the maze.

        Returns:
            str: Body of the svg tag.
        """
        return "".join(
            [
                arrow_marker(),
                background(),
                *map(self._draw_square, maze),
                self._draw_solution(solution) if solution else "",
            ]
        )

    def _transform(self, square: Square, extra_offset: int = 0) -> Point:
        """Establishes where a square should go by transforming its row and
        column into pixel coordinates.

        Args:
            square (Square): Square to be drawn.
            extra_offset (int, optional): Position translation of the square.
                Defaults to 0.

        Returns:
            Point: Final position of the top left corder of the square to be
                drawn.
        """
        return Point(
            x=square.column * self.square_size,
            y=square.row * self.square_size,
        ).translate(
            x_pos=self.offset + extra_offset, y_pos=self.offset + extra_offset
        )  # for next line

    def _draw_square(self, square: Square) -> str:
        """Draws the square by drawing its border, filling with colour
            depending on its role, adding the corresponding label inside.
            Each of these elements will become a separate SVG tag that you'll
            append to a Python list before joining together.

        Args:
            square (Square): Represents the square to be drawn.

        Returns:
            str: SVG tag in string the represents the square drawn.
        """
        top_left: Point = self._transform(square)
        tags = []
        if square.role is Role.EXTERIOR:
            tags.append(exterior(top_left, self.square_size, self.line_width))
        elif square.role is Role.WALL:
            tags.append(wall(top_left, self.square_size, self.line_width))
        elif emoji := ROLE_EMOJI.get(square.role):  # type: ignore
            tags.append(label(emoji, top_left, self.square_size // 2))
        tags.append(self._draw_border(square, top_left))
        return "".join(tags)

    def _draw_border(self, square: Square, top_left: Point) -> str:
        """Draws tje border of a given square from the starting point.

        Args:
            square (Square): Square to be drawn
            top_left (Point): Starting point

        Returns:
            str: String representation of the SVG tag.
        """
        return decompose(square.border, top_left, self.square_size).draw(
            stroke_width=self.line_width, stroke="black", fill="none"
        )

    def _draw_solution(self, solution: Solution) -> str:
        """Draws the solution as a line, which ends with an arrow marker.

        Args:
            solution (Solution): Solution to the maze.

        Returns:
            str: SOlution to the maze
        """
        return Polyline(
            [
                self._transform(point, self.square_size // 2)
                for point in solution  # for next line
            ]  # for next line
        ).draw(
            stroke_width=self.line_width * 2,
            stroke_opacity="50%",
            stroke="red",
            fill="none",
            marker_end="url(#arrow)",
        )


def arrow_marker() -> str:
    """The <defs> and <marker> elements define an arrow shape that you'll
    reference later in the SVG document

    Returns:
        str: SVG string representation of th arrow marker
    """
    return tag(
        "defs",
        tag(
            "marker",
            tag(
                "path",
                d="M 0,0 L 10,5 L 0,10 2,5 z",
                fill="red",
                fill_opacity="50%",  # noqa: E501
            ),
            id="arrow",
            viewBox="0 0 20 20",
            refX="2",
            refY="5",
            markerUnits="strokeWidth",
            markerWidth="10",
            markerHeight="10",
            orient="auto",
        ),
    )


def background() -> str:
    """Creates  Rect primitive to draw a white rectangle stretched across the
    entire image.

    Returns:
        str: SVF string representation of the a white rectangle.
    """
    return Rect().draw(width="100%", height="100%", fill="white")


def exterior(top_left: Point, size: int, line_width: int) -> str:
    """Draws a white rectangle.

    Args:
        top_left (Point): Starting point.
        size (int): Length of the rectangle.
        line_width (int): Width of the rectangle.

    Returns:
        str: String SVG representation of the drawn rectangle.
    """
    return Rect(top_left).draw(
        width=size,
        height=size,
        stroke_width=line_width,
        stroke="none",
        fill="white",  # line
    )


def wall(top_left: Point, size: int, line_width: int) -> str:
    """Draws a lightgray rectangle.

    Args:
        top_left (Point): Starting point.
        size (int): Length of the rectangle.
        line_width (int): Width of the rectangle.

    Returns:
        str: String SVG representation of the drawn rectangle.
    """
    return Rect(top_left).draw(
        width=size,
        height=size,
        stroke_width=line_width,
        stroke="none",
        fill="lightgray",
    )


def label(emoji: str, top_left: Point, offset: int) -> str:
    """Draws tje specific emoji icon int he middle of the square.

    Args:
        emoji (str): Emoji to be drawn.
        top_left (Point): Starting point.
        offset (int): Offset from the starting point.

    Returns:
        str: _description_
    """
    return Text(emoji, top_left.translate(x_pos=offset, y_pos=offset)).draw(
        font_size=f"{offset}px",
        text_anchor="middle",
        dominant_baseline="middle",  # line
    )
