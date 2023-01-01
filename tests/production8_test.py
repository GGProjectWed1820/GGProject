import dataclasses

import pytest
import networkx as nx
from collections import Counter
from src.vertex_params import VertexParams, VertexType
from src.visualization import draw
from tests.fixtures import (
    start_graph,
    graph_before_eighth_production,
    graph_after_eighth_production,
    production8,
)


def _are_graphs_matching(g1: nx.Graph, g2: nx.Graph) -> bool:
    g1_nodes_values = list(map(lambda n: tuple(n.values()), g1.nodes.values()))
    g2_nodes_values = list(map(lambda n: tuple(n.values()), g2.nodes.values()))
    return Counter(g1_nodes_values) == Counter(g2_nodes_values)


def test_applies_to_graph_after_eighth_production(
        graph_before_eighth_production, graph_after_eighth_production, production8
):
    subgraph = production8.find_isomorphic_to_left_side(graph_before_eighth_production)
    graph_after_applying = production8.apply(graph_before_eighth_production, subgraph)

    assert _are_graphs_matching(graph_after_applying, graph_after_eighth_production)


def test_should_not_transform_removed_node(
        graph_before_eighth_production,
        production8
):
    graph_before_eighth_production.remove_node(15)
    subgraph = production8.find_isomorphic_to_left_side(graph_before_eighth_production)
    assert subgraph is None


def test_should_not_transform_removed_edge(
        graph_before_eighth_production,
        production8
):
    graph_before_eighth_production.remove_edge(5, 7)
    subgraph = production8.find_isomorphic_to_left_side(graph_before_eighth_production)
    assert subgraph is None


def test_should_not_transform_wrong_node_type(
        graph_before_eighth_production,
        production8
):
    old_node_1 = VertexParams(**graph_before_eighth_production.nodes[16])

    graph_before_eighth_production.add_nodes_from(
        [(16, dataclasses.asdict(dataclasses.replace(old_node_1, vertex_type=VertexType.INTERIOR)),)])
    subgraph = production8.find_isomorphic_to_left_side(graph_before_eighth_production)
    assert subgraph is None


def test_should_not_transform_wrong_position(
        graph_before_eighth_production,
        production8
):
    old_node_14 = VertexParams(**graph_before_eighth_production.nodes[15])

    graph_before_eighth_production.add_nodes_from(
        [(15, dataclasses.asdict(dataclasses.replace(old_node_14, position=(0.25, 0.69))),)]
    )
    subgraph = production8.find_isomorphic_to_left_side(graph_before_eighth_production)
    assert subgraph is None
