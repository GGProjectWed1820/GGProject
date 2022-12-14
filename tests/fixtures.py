import dataclasses

import networkx as nx
import pytest

from src.productions.production1 import Production1
from src.productions.production2 import Production2
from src.productions.production10 import Production10
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
def production1():
    return Production1()


@pytest.fixture
def production2():
    return Production2()

@pytest.fixture
def production10():
    return Production10()

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

