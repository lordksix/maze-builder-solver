"""Provide the functions that handles the conversion of the mazes to graphs.

This module allows the creation of graphs from mazes.

The module contains the following classes:
- `Edge`: A class that represents the edge between graph nodes. A node is
    equivalent to a Square.
- `FileBody`: A class that represents the body of the maze file.

The module contains the following functions:
- `get_nodes`: A function to get a set of nodes from a Maze object.
- `get_edges`: A function to get a set of edges from a Maze object and its
    set of nodes.
- `make_graph`: A function to create a NetworkX graph of the maze.
"""
import math
from typing import NamedTuple, TypeAlias

import networkx as nx

from maze_solver.models.border import Border
from maze_solver.models.maze import Maze
from maze_solver.models.role import Role
from maze_solver.models.square import Square

Node: TypeAlias = Square


class Edge(NamedTuple):
    """A class that represents the edge between graph nodes. A node is
    equivalent to a Square,

    Args:
        NamedTuple (Node): Couple of Nodes(node1, node2).

    Methods:
        - distance(self) -> float:
            A function to calculate the distance between nodes.
        - weight(self, bonus=1, penalty=2) -> float:
            A function to calculate the the weighted distance of the edge base
            on role.
        - flip(self) -> "Edge":
            A function which creates a new Edge from the flipped nodes of the
            original edge.
    """

    node1: Node
    node2: Node

    @property
    def distance(self) -> float:
        """Calculates the distance between the nodes of the Edge.

        Returns:
            float: Distance between nodes of the Edge.
        """
        return math.dist(
            (self.node1.row, self.node1.column),
            (self.node2.row, self.node2.column),  # line
        )

    @property
    def flip(self) -> "Edge":
        """Creates a new Edge instance by flipping the nodes.

        Returns:
            Edge: Edge instance with the nodes flipped.
        """
        return Edge(self.node2, self.node1)

    def weight(self, bonus=1, penalty=2) -> float:
        """Calculate the weighted distance of the edge base on role.

        Args:
            bonus (int, optional): Weight to be deducted from the distance.
                Defaults to 1.
            penalty (int, optional): Weight to be added from the distance.
                Defaults to 2.

        Returns:
            float: Total weighted distance.
        """
        match self.node2.role:
            case Role.REWARD:
                return self.distance - bonus
            case Role.ENEMY:
                return self.distance + penalty
            case _:
                return self.distance


def get_nodes(maze: Maze) -> set[Node]:
    """A function to process a Maze object to get a set of unique nodes.

    Args:
        maze (Maze): Represents the Maze object to be processed.

    Returns:
        set[Node]: Set of unique nodes.
    """
    nodes: set[Node] = set()
    for square in maze:
        if square.role in (Role.EXTERIOR, Role.WALL):
            continue
        if square.role is not Role.NONE:
            nodes.add(square)
        if (
            square.border.intersection
            or square.border.dead_end
            or square.border.corner  #
        ):  #
            nodes.add(square)
    return nodes


def get_edges(maze: Maze, nodes: set[Node]) -> set[Edge]:
    """A function to process a Maze object to get a set of unique edges from
    its set of nodes.

    Args:
        maze (Maze): Maze object being process.
        nodes (set[Node]): Set of unique nodes from the maze being process.

    Returns:
        set[Edge]: Set of unique edges
    """
    edges: set[Edge] = set()
    for source_node in nodes:
        # Follow right:
        node = source_node
        for x_pos in range(node.column + 1, maze.width):
            if node.border & Border.RIGHT:
                break
            node = maze.squares[node.row * maze.width + x_pos]
            if node in nodes:
                edges.add(Edge(source_node, node))
                break
        # Follow down:
        node = source_node
        for y_pos in range(node.row + 1, maze.height):
            if node.border & Border.BOTTOM:
                break
            node = maze.squares[y_pos * maze.width + node.column]
            if node in nodes:
                edges.add(Edge(source_node, node))
                break
    return edges


def make_graph(maze: Maze) -> nx.DiGraph:
    """Creates a NetworkX graph of the maze.

    Args:
        maze (Maze): Represents the maze object.

    Returns:
        nx.Graph: Graph of the maze
    """
    return nx.DiGraph(
        (edge.node1, edge.node2, {"weight": edge.weight()})
        for edge in get_directed_edges(maze, get_nodes(maze))
    )


def get_directed_edges(maze: Maze, nodes: set[Node]) -> set[Edge]:
    """Return a set of edges in both directions based on the undirected edges.
        Depending on the direction, the same edge may have different weights

    Args:
        maze (Maze): Maze to be processed
        nodes (set[Node]): set of nodes of the maze

    Returns:
        set[Edge]: Return a set of edges in both directions based on the
            undirected edges.
    """
    return (edges := get_edges(maze, nodes)) | {edge.flip for edge in edges}
