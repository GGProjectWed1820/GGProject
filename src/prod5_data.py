from src.vertex_params import VertexParams, VertexType
from typing import Any
import dataclasses
import networkx as nx


def get_node(nr: int, vertex_type: VertexType, position: tuple[float, float], level: int) -> tuple[
    int, dict[str, Any]]:
    return (
        nr,
        dataclasses.asdict(
            VertexParams(vertex_type=vertex_type, position=position, level=level)
        ),
    )


def are_graphs_isomorphic(graph1: nx.Graph, graph2: nx.Graph) -> bool:
    return nx.is_isomorphic(
        graph1,
        graph2,
        node_match=are_nodes_equal
    )


def are_nodes_equal(node1, node2) -> bool:
    return VertexParams(**node1) == VertexParams(**node2)


def get_correct_left_side():
    graph = nx.Graph()
    graph.add_nodes_from([
        get_node(0, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1),
        get_node(1, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.5), level=1),
        get_node(2, vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1),
        get_node(3, vertex_type=VertexType.EXTERIOR, position=(0.5, 1.0), level=1),
        get_node(4, vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1),
        get_node(5, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=1),
        get_node(6, vertex_type=VertexType.INTERIOR, position=(1 / 3, 2 / 3), level=1)
    ])

    graph.add_edges_from([
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 0),

        (6, 0),
        (6, 2),
        (6, 4)
    ])

    return graph


def get_expected_right_side():
    graph = nx.Graph()
    graph.add_nodes_from([
        get_node(0, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1),
        get_node(1, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.5), level=1),
        get_node(2, vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1),
        get_node(3, vertex_type=VertexType.EXTERIOR, position=(0.5, 1.0), level=1),
        get_node(4, vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1),
        get_node(5, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=1),

        # _get_node(6, vertex_type=VertexType.INTERIOR, position=(1 / 3, 2 / 3), level=1),
        # _get_node(0, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1),
        # _get_node(1, vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1),
        # _get_node(2, vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1),
        # _get_node(3, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=1),

        # _get_node(6, vertex_type=VertexType.INTERIOR_USED, position=(1 / 3, 2 / 3), level=1),
        # _get_node(7, vertex_type=VertexType.INTERIOR, position=(1 / 6, 0.5), level=2),
        # _get_node(8, vertex_type=VertexType.INTERIOR, position=(0.5, 5/6), level=2),
        # _get_node(9, vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=2),
        # _get_node(10, vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=2),
        # _get_node(11, vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=2),
        # _get_node(12, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2)

        get_node(6, vertex_type=VertexType.INTERIOR_USED, position=(1 / 3, 2 / 3), level=1),
        get_node(7, vertex_type=VertexType.EXTERIOR, position=(0, 0), level=2),
        get_node(8, vertex_type=VertexType.EXTERIOR, position=(0, 0.5), level=2),
        get_node(9, vertex_type=VertexType.EXTERIOR, position=(0, 1), level=2),
        get_node(10, vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2),
        get_node(11, vertex_type=VertexType.EXTERIOR, position=(0.5, 1), level=2),
        get_node(12, vertex_type=VertexType.EXTERIOR, position=(1, 1), level=2),
        get_node(13, vertex_type=VertexType.INTERIOR, position=(1 / 6, 2 / 3), level=2),
        get_node(14, vertex_type=VertexType.INTERIOR, position=(1 / 6, 1 / 3), level=2),
        get_node(15, vertex_type=VertexType.INTERIOR, position=(1 / 3, 5 / 6), level=2),
        get_node(16, vertex_type=VertexType.INTERIOR, position=(2 / 3, 5 / 6), level=2)
    ])

    graph.add_edges_from([
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 0),
        (6, 0),
        (6, 2),
        (6, 4),

        (6, 13),
        (6, 14),
        (6, 15),
        (6, 16),
        (7, 8),
        (7, 10),
        (7, 14),
        (8, 9),
        (8, 13),
        (8, 14),
        (8, 10),
        (9, 10),
        (9, 11),
        (9, 13),
        (9, 15),
        (10, 11),
        (10, 12),
        (10, 13),
        (10, 14),
        (10, 15),
        (10, 16),
        (11, 12),
        (11, 15),
        (11, 16),
        (12, 16)
    ])

    return graph
