"""Provide the functions that handles the solution of the maze using graphs
through NetworkX library.

Example:
    >>> from pathlib import Path
    >>> from maze_solver.graphs.solver import solve
    >>> from maze_solver.models.maze import Maze
    >>> from maze_solver.view.renderer import SVGRenderer

    >>> maze = Maze.load(Path("mazes") / "miniature.maze")
    >>> solution = solve(maze)

    >>> len(solution)
    6

    >>> [square.index for square in solution]
    [8, 9, 11, 7, 6, 2]

    >>> SVGRenderer().render(maze, solution).preview()

This module allows the solution of the maze using graphs through NetworkX
library.

The module contains the following functions:
- `solve`: A functions that finds the shortest path to solve the maze.
- `solve_all`: A functions that finds the all shortest path to solve the maze.
"""
import networkx as nx

from maze_solver.graphs.converter import make_graph
from maze_solver.models.maze import Maze
from maze_solver.models.solution import Solution


def solve(maze: Maze) -> Solution | None:
    """Finds the shortest path as a solution of the maze.

    Args:
        maze (Maze): Represents the maze object to be solved.

    Returns:
        Solution | None: Object that represents the solution.
    """
    try:
        return Solution(
            squares=tuple(
                nx.shortest_path(
                    make_graph(maze),
                    source=maze.entrance,
                    target=maze.exit,
                    weight="weight",
                )
            )
        )
    except nx.NetworkXException:
        return None


def solve_all(maze: Maze) -> list[Solution]:
    """Finds all the shortest path as a solution of the maze.

    Args:
        maze (Maze): Represents the maze object to be solved.

    Returns:
        list[Solution]: List of all shortest paths.
    """
    try:
        return [
            Solution(squares=tuple(path))
            for path in nx.all_shortest_paths(
                make_graph(maze),
                source=maze.entrance,
                target=maze.exit,
                weight="weight",
            )
        ]
    except nx.NetworkXException:
        return []
