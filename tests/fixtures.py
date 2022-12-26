import dataclasses

import networkx as nx
import pytest

from src.productions.production1 import Production1
from src.productions.production10 import Production10
from src.productions.production2 import Production2
from src.productions.production5 import Production5
from src.productions.production6 import Production6
from src.productions.production7 import Production7
from src.vertex_params import VertexParams, VertexType


def mk_vertex(t, pos, level):
    return dataclasses.asdict(VertexParams(vertex_type=t, position=pos, level=level))


def _are_nodes_equal(node1, node2) -> bool:
    return VertexParams(**node1).vertex_type == VertexParams(**node2).vertex_type


def _are_graphs_isomorphic(graph1: nx.Graph, graph2: nx.Graph) -> bool:
    return nx.is_isomorphic(
        graph1,
        graph2,
        node_match=_are_nodes_equal
    )


@pytest.fixture
def start_graph():
    graph = nx.Graph()
    graph.add_nodes_from(
        [(
            0,
            dataclasses.asdict(
                VertexParams(vertex_type=VertexType.START, position=(0.5, 0.5), level=0)
            ),
        )]
    )
    return graph


@pytest.fixture
def start_graph2():
    graph = nx.Graph()
    graph.add_nodes_from(
        [(
            0,
            dataclasses.asdict(
                VertexParams(vertex_type=VertexType.START, position=(0.5, 0.5), level=0)
            ),
        ),
        (
            1,
            dataclasses.asdict(
                VertexParams(vertex_type=VertexType.START, position=(1, 1), level=0)
            ),
        )]
    )
    graph.add_edges_from([(0, 1)])
    return graph


@pytest.fixture
def incorrect_start_graph():
    graph = nx.Graph()
    graph.add_nodes_from(
        [(
            0,
            dataclasses.asdict(
                VertexParams(vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=0)
            ),
        )]
    )
    return graph


@pytest.fixture
def production1():
    return Production1()


@pytest.fixture
def production2():
    return Production2()


@pytest.fixture
def production6():
    return Production6()

@pytest.fixture
def production5():
    return Production5()


@pytest.fixture
def production7():
    return Production7()


@pytest.fixture
def production10():
    return Production10()


@pytest.fixture
def graph_before_seventh_production(start_graph, production1):
    G = nx.Graph()
    G.add_nodes_from(
        [
            (
                0,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.START_USED, position=(0.5, 0.5), level=0
                    )
                ),
            ),
            (
                1,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1
                    )
                ),
            ),
            (
                2,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1
                    )
                ),
            ),
            (
                3,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1
                    )
                ),
            ),
            (
                4,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1
                    )
                ),
            ),
            (
                5,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                6,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                7,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=2
                    )
                ),
            ),
            (
                8,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=2
                    )
                ),
            ),
            (
                9,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=2
                    )
                ),
            ),
            (
                10,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2
                    )
                ),
            ),
            (
                11,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                12,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),

            (
                14,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=2
                    )
                ),
            ),
            (
                15,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=2
                    )
                ),
            ),
            (
                16,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2
                    )
                ),
            ),
            (
                17,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                18,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
        ]
    )

    G.add_edges_from(
        [
            (0, 5),
            (0, 6),
            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 4),
            (1, 5),
            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),
            (4, 6),
            (7, 8),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 10),
            (5, 11),
            (5, 12),
            (7, 11),
            (7, 12),
            (8, 11),
            (9, 12),
            (10, 11),
            (10, 12),
            (6, 17),
            (8, 15),
            (14, 15),
            (16, 17),
            (14, 17),
            (15, 17),
            (16, 14),
            (16, 8),
            (16, 18),
            (8, 18),
            (15, 18),
            (6, 18),
            (16, 15)
        ]
    )

    return G


@pytest.fixture
def graph_after_seventh_production(start_graph, production1):
    G = nx.Graph()
    G.add_nodes_from(
        [
            (
                0,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.START_USED, position=(0.5, 0.5), level=0
                    )
                ),
            ),
            (
                1,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1
                    )
                ),
            ),
            (
                2,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1
                    )
                ),
            ),
            (
                3,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1
                    )
                ),
            ),
            (
                4,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1
                    )
                ),
            ),
            (
                5,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                6,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR_USED, position=None, level=1
                    )
                ),
            ),
            (
                7,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=2
                    )
                ),
            ),
            (
                8,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=2
                    )
                ),
            ),
            (
                11,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                12,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                15,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=2
                    )
                ),
            ),

            (
                17,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                18,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.INTERIOR, position=None, level=2
                    )
                ),
            ),
            (
                19,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=2
                    )
                ),
            ),
            (
                20,
                dataclasses.asdict(
                    VertexParams(
                        vertex_type=VertexType.EXTERIOR, position=(0.5, 0.5), level=2
                    )
                ),
            ),
        ]
    )

    G.add_edges_from(
        [
            (0, 5),
            (0, 6),
            (1, 2),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (3, 4),
            (3, 5),
            (3, 6),
            (4, 6),
            (5, 11),
            (5, 12),
            (6, 17),
            (7, 8),
            (7, 11),
            (7, 12),
            (7, 19),
            (7, 20),
            (8, 11),
            (8, 15),
            (8, 18),
            (8, 19),
            (11, 19),
            (12, 19),
            (12, 20),
            (15, 17),
            (15, 18),
            (15, 20),
            (17, 19),
            (17, 20),
            (18, 19),
            (19, 20),
        ]
    )

    return G


@pytest.fixture
def graph_for_p10():
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, mk_vertex(VertexType.START_USED, (0.5, 0.5), 0)),

            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 1)),
            (2, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (3, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),
            (4, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 1)),

            (5, mk_vertex(VertexType.INTERIOR_USED, None, 1)),
            (6, mk_vertex(VertexType.INTERIOR_USED, None, 1)),

            (7, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 2)),
            (8, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (9, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (10, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (11, mk_vertex(VertexType.INTERIOR, None, 2)),
            (12, mk_vertex(VertexType.INTERIOR, None, 2)),

            (13, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (14, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (15, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 2)),
            

            (16, mk_vertex(VertexType.INTERIOR, None, 2)),
        ]
    )

    graph.add_edges_from(
        [
            (0, 5),
            (0, 6),

            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 4),

            (1, 5),
            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),
            (4, 6),

            (7, 8),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 10),

            (5, 11),
            (5, 12),

            (7, 11),
            (7, 12),
            (8, 11),
            (9, 12),
            (10, 11),
            (10, 12),

            (6, 16),

            (13, 14),
            (13, 15),
            (14, 15),

            (13, 16),
            (14, 16),
            (15, 16),
        ]
    )
    return graph


@pytest.fixture
def graph_for_p10_bigger():
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, mk_vertex(VertexType.START_USED, (0.5, 0.5), 0)),

            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 1)),
            (2, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (3, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),
            (4, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 1)),

            (5, mk_vertex(VertexType.INTERIOR_USED, None, 1)),
            (6, mk_vertex(VertexType.INTERIOR_USED, None, 1)),

            (7, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 2)),
            (8, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (9, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (10, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (11, mk_vertex(VertexType.INTERIOR, None, 2)),
            (12, mk_vertex(VertexType.INTERIOR, None, 2)),

            (13, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (14, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (15, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 2)),
            (17, mk_vertex(VertexType.EXTERIOR, (1.5, 1.5), 2)),
            

            (16, mk_vertex(VertexType.INTERIOR, None, 2)),
        ]
    )

    graph.add_edges_from(
        [
            (0, 5),
            (0, 6),

            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 4),

            (1, 5),
            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),
            (4, 6),

            (7, 8),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 10),

            (5, 11),
            (5, 12),

            (7, 11),
            (7, 12),
            (8, 11),
            (9, 12),
            (10, 11),
            (10, 12),

            (6, 16),

            (13, 14),
            (13, 15),
            (14, 15),

            (13, 16),
            (14, 16),
            (15, 16),
            (15, 17)
        ]
    )
    return graph


@pytest.fixture
def exact_graph_for_p10():
    graph = nx.Graph()

    graph.add_nodes_from(
        [

            (2, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (3, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),

            (5, mk_vertex(VertexType.INTERIOR_USED, None, 1)),
            (6, mk_vertex(VertexType.INTERIOR_USED, None, 1)),

            (7, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 2)),
            (8, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (9, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (10, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (11, mk_vertex(VertexType.INTERIOR, None, 2)),
            (12, mk_vertex(VertexType.INTERIOR, None, 2)),

            (13, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (14, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (15, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 2)),

            (16, mk_vertex(VertexType.INTERIOR, None, 2)),
        ]
    )

    graph.add_edges_from(
        [

            (2, 3),

            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),

            (7, 8),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 10),

            (5, 11),
            (5, 12),

            (7, 11),
            (7, 12),
            (8, 11),
            (9, 12),
            (10, 11),
            (10, 12),

            (6, 16),

            (13, 14),
            (13, 15),
            (14, 15),

            (13, 16),
            (14, 16),
            (15, 16),
        ]
    )
    return graph


@pytest.fixture
def exact_correct_graph_after_p10():
    graph = nx.Graph()
    graph.add_nodes_from(
        [

            (2, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (3, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),

            (5, mk_vertex(VertexType.INTERIOR_USED, None, 1)),
            (6, mk_vertex(VertexType.INTERIOR_USED, None, 1)),

            (7, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 2)),
            (8, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (9, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (10, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (11, mk_vertex(VertexType.INTERIOR, None, 2)),
            (12, mk_vertex(VertexType.INTERIOR, None, 2)),

            (15, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 2)),

            (16, mk_vertex(VertexType.INTERIOR, None, 2)),
        ]
    )

    graph.add_edges_from(
        [

            (2, 3),

            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),

            (7, 8),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 10),

            (5, 11),
            (5, 12),

            (7, 11),
            (7, 12),
            (8, 11),
            (9, 12),
            (10, 11),
            (10, 12),

            (6, 16),

            (8, 15),
            (9, 15),

            (8, 16),
            (9, 16),
            (15, 16),
        ]
    )
    return graph


@pytest.fixture
def correct_graph_after_p10():
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, mk_vertex(VertexType.START_USED, (0.5, 0.5), 0)),

            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 1)),
            (2, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (3, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),
            (4, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 1)),

            (5, mk_vertex(VertexType.INTERIOR_USED, None, 1)),
            (6, mk_vertex(VertexType.INTERIOR_USED, None, 1)),

            (7, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 2)),
            (8, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (9, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (10, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (11, mk_vertex(VertexType.INTERIOR, None, 2)),
            (12, mk_vertex(VertexType.INTERIOR, None, 2)),

            (15, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 2)),

            (16, mk_vertex(VertexType.INTERIOR, None, 2)),
        ]
    )

    graph.add_edges_from(
        [
            (0, 5),
            (0, 6),

            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 4),

            (1, 5),
            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),
            (4, 6),

            (7, 8),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 10),

            (5, 11),
            (5, 12),

            (7, 11),
            (7, 12),
            (8, 11),
            (9, 12),
            (10, 11),
            (10, 12),

            (6, 16),

            (8, 15),
            (9, 15),

            (8, 16),
            (9, 16),
            (15, 16),
        ]
    )
    return graph

@pytest.fixture
def correct_graph_after_p10_bigger():
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            (0, mk_vertex(VertexType.START_USED, (0.5, 0.5), 0)),

            (1, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 1)),
            (2, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 1)),
            (3, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 1)),
            (4, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 1)),

            (5, mk_vertex(VertexType.INTERIOR_USED, None, 1)),
            (6, mk_vertex(VertexType.INTERIOR_USED, None, 1)),

            (7, mk_vertex(VertexType.EXTERIOR, (0.0, 0.0), 2)),
            (8, mk_vertex(VertexType.EXTERIOR, (0.0, 1.0), 2)),
            (9, mk_vertex(VertexType.EXTERIOR, (1.0, 0.0), 2)),
            (10, mk_vertex(VertexType.EXTERIOR, (0.5, 0.5), 2)),

            (11, mk_vertex(VertexType.INTERIOR, None, 2)),
            (12, mk_vertex(VertexType.INTERIOR, None, 2)),

            (15, mk_vertex(VertexType.EXTERIOR, (1.0, 1.0), 2)),
            (17, mk_vertex(VertexType.EXTERIOR, (1.5, 1.5), 2)),

            (16, mk_vertex(VertexType.INTERIOR, None, 2)),
        ]
    )

    graph.add_edges_from(
        [
            (0, 5),
            (0, 6),

            (1, 2),
            (1, 3),
            (2, 3),
            (2, 4),
            (3, 4),

            (1, 5),
            (2, 5),
            (3, 5),
            (2, 6),
            (3, 6),
            (4, 6),

            (7, 8),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 10),

            (5, 11),
            (5, 12),

            (7, 11),
            (7, 12),
            (8, 11),
            (9, 12),
            (10, 11),
            (10, 12),

            (6, 16),

            (8, 15),
            (9, 15),

            (8, 16),
            (9, 16),
            (15, 16),
            (15,17)
        ]
    )
    return graph