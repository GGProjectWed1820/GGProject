import dataclasses
from dataclasses import asdict

import networkx as nx
import pytest

from src.productions.production4 import Production4
from src.vertex_params import VertexParams, VertexType
from tests.fixtures import start_graph, production4


def mk_vertex(t, pos, level):
    return asdict(VertexParams(vertex_type=t, position=pos, level=level))


def _assert_graphs_equal(graph1: nx.Graph, graph2: nx.Graph):
    assert nx.is_isomorphic(
        graph1,
        graph2,
        node_match=lambda node1, node2: VertexParams(**node1) == VertexParams(**node2)
    )


@pytest.fixture
def p4_left_side():
    graph = nx.Graph()

    graph.add_nodes_from(
        [
            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 0)),
            (2, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 0)),
            (3, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 0)),

            (4, mk_vertex(VertexType.INTERIOR, (1 / 3, 2 / 3), 0)),

            (5, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 0)),
            (6, mk_vertex(VertexType.EXTERIOR, (0.5, 1), 0)),
        ]
    )

    graph.add_edges_from(
        [
            (1, 4),
            (2, 4),
            (3, 4),

            (1, 5),
            (2, 5),
            (2, 3),
            (1, 6),
            (3, 6),
        ]
    )
    return graph


@pytest.fixture
def p4_after_production():
    graph = nx.Graph()

    graph.add_nodes_from(
        [
            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 0)),
            (2, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 0)),
            (3, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 0)),

            (4, mk_vertex(VertexType.INTERIOR_USED, (1 / 3, 2 / 3), 0)),

            (5, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 0)),
            (6, mk_vertex(VertexType.EXTERIOR, (0.5, 1), 0)),

            (7, mk_vertex(VertexType.INTERIOR, (1 / 3, 2.5 / 3), 1)),
            (8, mk_vertex(VertexType.INTERIOR, (2 / 3, 2.5 / 3), 1)),
            (9, mk_vertex(VertexType.INTERIOR, (2.5 / 3, 2 / 3), 1)),

            (10, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (11, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),
            (12, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 1)),

            (13, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 1)),
            (14, mk_vertex(VertexType.EXTERIOR, (0.5, 1), 1)),
        ]
    )
    graph.add_edges_from(
        [
            (1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 3), (3, 4), (3, 6), (4, 7), (4, 8), (4, 9), (7, 10), (7, 13),
            (7, 14), (8, 12), (8, 14), (8, 13), (9, 12), (9, 11), (9, 13), (10, 14), (10, 13), (11, 13), (11, 12),
            (12, 14), (12, 13), (13, 14)
        ]
    )
    return graph


def test_should_transform_correct_graph(p4_left_side, p4_after_production):
    subgraph = Production4.find_isomorphic_to_left_side(p4_left_side)
    new_graph = Production4.apply(p4_left_side, subgraph)

    _assert_graphs_equal(new_graph, p4_after_production)


def test_should_not_find_isomorphic_when_node_removed(p4_left_side):
    p4_left_side.remove_node(5)
    subgraph = Production4.find_isomorphic_to_left_side(p4_left_side)
    assert subgraph is None


def test_should_not_find_isomorphic_when_third_breaking_node_added(p4_left_side):
    p4_left_side.add_nodes_from([(7, mk_vertex(VertexType.EXTERIOR, (1, 0.5), 0))])
    p4_left_side.remove_edges_from([(2, 3)])
    p4_left_side.add_edges_from([(2, 7), (3, 7)])
    subgraph = Production4.find_isomorphic_to_left_side(p4_left_side)
    assert subgraph is None


def test_should_not_find_isomorphic_when_edge_removed(p4_left_side):
    p4_left_side.remove_edge(2, 3)
    subgraph = Production4.find_isomorphic_to_left_side(p4_left_side)
    assert subgraph is None


def test_should_not_find_isomorphic_when_node_type_changed(p4_left_side):
    node_1 = VertexParams(**p4_left_side.nodes[1])
    p4_left_side.add_nodes_from([(1, dataclasses.asdict(dataclasses.replace(node_1, vertex_type=VertexType.INTERIOR)))])
    subgraph = Production4.find_isomorphic_to_left_side(p4_left_side)
    assert subgraph is None


def test_should_not_find_isomorphic_when_node_position_changed(p4_left_side):
    node_5 = VertexParams(**p4_left_side.nodes[5])
    p4_left_side.add_nodes_from([(1, dataclasses.asdict(dataclasses.replace(node_5, position=(0.3, 0.5))))])
    subgraph = Production4.find_isomorphic_to_left_side(p4_left_side)
    assert subgraph is None
