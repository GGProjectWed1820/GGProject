from src.vertex_params import VertexParams, VertexType

from tests.fixtures import start_graph, production1


def test_finds_first_element_in_start_graph(start_graph, production1):
    # when
    subgraph = production1.find_isomorphic_to_left_side(start_graph)

    # then
    assert subgraph is not None
    assert len(subgraph.nodes) == 1
    assert VertexParams(**subgraph.nodes[0]).vertex_type == VertexType.START


def test_does_not_find_anything_in_non_start_graph(start_graph, production1):
    # when
    subgraph = production1.find_isomorphic_to_left_side(start_graph)
    new_graph = production1.apply(start_graph, subgraph)

    new_subgraph = production1.find_isomorphic_to_left_side(new_graph)

    # then
    assert new_subgraph is None


def test_graph_after_first_production_is_applied(start_graph, production1):
    # given
    subgraph = production1.find_isomorphic_to_left_side(start_graph)

    # when
    new_graph = production1.apply(start_graph, subgraph)

    # then
    assert len(new_graph) == 7
    assert new_graph.nodes[0]["vertex_type"] == VertexType.START_USED
