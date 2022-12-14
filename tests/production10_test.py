import dataclasses

import networkx as nx
import pytest

from tests.fixtures import production10
from tests.fixtures import correct_graph_after_p10
from tests.fixtures import exact_correct_graph_after_p10
from tests.fixtures import graph_for_p10
from tests.fixtures import exact_graph_for_p10
from tests.fixtures import _are_graphs_isomorphic
from tests.fixtures import _are_nodes_equal
from src.vertex_params import VertexParams,VertexType

def test_should_correctly_transform(
        exact_graph_for_p10,
        exact_correct_graph_after_p10,
        production10
):
    subgraph = production10.find_isomorphic_to_left_side(exact_graph_for_p10)
    graph_after_p10 = production10.apply(exact_graph_for_p10, subgraph)

    assert _are_graphs_isomorphic(graph_after_p10, exact_correct_graph_after_p10)


def test_should_correctly_transform_bigger_graph(
        graph_for_p10,
        correct_graph_after_p10,
        production10
):
    subgraph = production10.find_isomorphic_to_left_side(graph_for_p10)
    graph_after_p10 = production10.apply(graph_for_p10, subgraph)

    assert _are_graphs_isomorphic(graph_after_p10, correct_graph_after_p10)


def test_should_not_transform_missing_edge(
        graph_for_p10,
        correct_graph_after_p10,
        production10
):
    graph_for_p10.remove_edge(14,13)
    subgraph = production10.find_isomorphic_to_left_side(graph_for_p10)
  

    assert subgraph is None


def test_should_not_transform_wrong_node_type(
        graph_for_p10,
        correct_graph_after_p10,
        production10
):
    old = VertexParams(**graph_for_p10.nodes[16])

    graph_for_p10.add_nodes_from([
        (
            16,
            dataclasses.asdict(
                dataclasses.replace(
                    old, vertex_type=VertexType.INTERIOR_USED
                )
            ),
        )
    ])
    subgraph = production10.find_isomorphic_to_left_side(graph_for_p10)
  

    assert subgraph is None

def test_should_not_transform_missing_node(
        graph_for_p10,
        correct_graph_after_p10,
        production10
):
    graph_for_p10.remove_node(16)
    subgraph = production10.find_isomorphic_to_left_side(graph_for_p10)
  

    assert subgraph is None


def test_should_not_transform_wrong_position(
        graph_for_p10,
        correct_graph_after_p10,
        production10
):
    old = VertexParams(**graph_for_p10.nodes[13])

    graph_for_p10.add_nodes_from([
        (
            13,
            dataclasses.asdict(
                dataclasses.replace(
                    old, position=(2, 2)
                )
            ),
        )
    ])
    subgraph = production10.find_isomorphic_to_left_side(graph_for_p10)
  

    assert subgraph is None