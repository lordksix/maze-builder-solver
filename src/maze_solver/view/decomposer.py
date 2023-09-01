"""Provide the functions that handles border representation in SVG.

This module allows the creation of xml tags for rendering.

The module contains the following functions:
- `decompose`: A function that returns a geometric primitive that represents
    the border of the square in SVG.
"""
from maze_solver.models.border import Border
from maze_solver.view.primitives import (
    DisjointLines,
    Line,
    NullPrimitive,
    Point,
    Polygon,
    Polyline,
    Primitive,
)


def decompose(border: Border, top_left: Point, sq_size: int) -> Primitive:
    """A function that returns a geometric primitive that represents
    the border of the square in SVG.
    Args:
        border (Border): Represents the border pattern of the square.
        top_left (Point): Represents the top left point, starting point.
            of the square
        sq_size (int): Represents the size of the side of the square.

    Returns:
        Primitive: geometric primitive that represents the border of the
            square in SVG.
    """
    top_right: Point = top_left.translate(x_pos=sq_size)
    bottom_right: Point = top_left.translate(x_pos=sq_size, y_pos=sq_size)
    bottom_left: Point = top_left.translate(y_pos=sq_size)

    top = Line(top_left, top_right)
    bottom = Line(bottom_left, bottom_right)
    left = Line(top_left, bottom_left)
    right = Line(top_right, bottom_right)

    if border is Border.LEFT | Border.TOP | Border.RIGHT | Border.BOTTOM:
        return Polygon(
            [
                top_left,
                top_right,
                bottom_right,
                bottom_left,
            ]
        )

    if border is Border.BOTTOM | Border.LEFT | Border.TOP:
        return Polyline(
            [
                bottom_right,
                bottom_left,
                top_left,
                top_right,
            ]
        )

    if border is Border.LEFT | Border.TOP | Border.RIGHT:
        return Polyline(
            [
                bottom_left,
                top_left,
                top_right,
                bottom_right,
            ]
        )

    if border is Border.TOP | Border.RIGHT | Border.BOTTOM:
        return Polyline(
            [
                top_left,
                top_right,
                bottom_right,
                bottom_left,
            ]
        )

    if border is Border.RIGHT | Border.BOTTOM | Border.LEFT:
        return Polyline(
            [
                top_right,
                bottom_right,
                bottom_left,
                top_left,
            ]
        )

    if border is Border.LEFT | Border.TOP:
        return Polyline(
            [
                bottom_left,
                top_left,
                top_right,
            ]
        )

    if border is Border.TOP | Border.RIGHT:
        return Polyline(
            [
                top_left,
                top_right,
                bottom_right,
            ]
        )

    if border is Border.BOTTOM | Border.LEFT:
        return Polyline(
            [
                bottom_right,
                bottom_left,
                top_left,
            ]
        )

    if border is Border.RIGHT | Border.BOTTOM:
        return Polyline(
            [
                top_right,
                bottom_right,
                bottom_left,
            ]
        )

    if border is Border.LEFT | Border.RIGHT:
        return DisjointLines([left, right])

    if border is Border.TOP | Border.BOTTOM:
        return DisjointLines([top, bottom])

    if border is Border.TOP:
        return top

    if border is Border.RIGHT:
        return right

    if border is Border.BOTTOM:
        return bottom

    if border is Border.LEFT:
        return left

    return NullPrimitive()
