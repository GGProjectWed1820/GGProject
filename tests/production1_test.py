from dataclasses import asdict

from src.vertex_params import VertexParams, VertexType

from tests.fixtures import start_graph, start_graph2, incorrect_start_graph, production1


def test_finds_first_element_in_start_graph(start_graph, production1):
    # when
    subgraph = production1.find_isomorphic_to_left_side(start_graph)

    # then
    assert subgraph is not None
    assert len(subgraph.nodes) == 1
    assert VertexParams(**subgraph.nodes[0]).vertex_type == VertexType.START


def test_finds_first_element_in_start_graph2(start_graph2, production1):
    # when
    subgraph = production1.find_isomorphic_to_left_side(start_graph2)

    # then
    assert subgraph is not None
    assert len(subgraph.nodes) == 1
    assert VertexParams(**subgraph.nodes[0]).vertex_type == VertexType.START


def test_right_side_is_correct(start_graph, production1):
    # when
    subgraph = production1.find_isomorphic_to_left_side(start_graph)
    new_graph = production1.apply(start_graph, subgraph)

    # then
    assert new_graph.number_of_nodes() == 7
    nodes = [
        VertexParams(vertex_type=VertexType.START_USED, position=(0.5, 0.5), level=0),

        VertexParams(vertex_type=VertexType.EXTERIOR, position=(0.0, 0.0), level=1),
        VertexParams(vertex_type=VertexType.EXTERIOR, position=(0.0, 1.0), level=1),
        VertexParams(vertex_type=VertexType.EXTERIOR, position=(1.0, 0.0), level=1),
        VertexParams(vertex_type=VertexType.EXTERIOR, position=(1.0, 1.0), level=1),

        VertexParams(vertex_type=VertexType.INTERIOR, position=(0.25, 0.25), level=1),
        VertexParams(vertex_type=VertexType.INTERIOR, position=(0.75, 0.75), level=1),
    ]
    for idx, params in enumerate(nodes):
        assert new_graph.nodes.items().__contains__((idx, asdict(params)))
    print(new_graph.nodes.values())
    assert new_graph.number_of_edges() == 13


def test_does_not_find_anything_in_non_start_graph(start_graph, production1):
    # when
    subgraph = production1.find_isomorphic_to_left_side(start_graph)
    new_graph = production1.apply(start_graph, subgraph)

    new_subgraph = production1.find_isomorphic_to_left_side(new_graph)

    # then
    assert new_subgraph is None


def test_does_not_find_anything_in_non_start_graph2(incorrect_start_graph, production1):
    # when
    subgraph = production1.find_isomorphic_to_left_side(incorrect_start_graph)

    # then
    assert subgraph is None


def test_graph_after_first_production_is_applied(start_graph, production1):
    # given
    subgraph = production1.find_isomorphic_to_left_side(start_graph)

    # when
    new_graph = production1.apply(start_graph, subgraph)

    # then
    assert len(new_graph) == 7
    assert new_graph.nodes[0]["vertex_type"] == VertexType.START_USED
