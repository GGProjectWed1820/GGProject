import dataclasses

import networkx as nx
import pytest

from src.productions.production1 import Production1
from src.productions.production2 import Production2
from src.vertex_params import VertexParams, VertexType


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

