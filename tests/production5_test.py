import pytest

from tests.fixtures import production5, _are_graphs_isomorphic
from src.prod5_data import get_expected_right_side, get_correct_left_side


def test_should_correctly_transform(
        correct_graph_for_left_side_p5,
        correct_graph_for_p5_right_side,
        production5
):
    subgraph = production5.find_isomorphic_to_left_side(correct_graph_for_left_side_p5)
    production_right_side = production5.apply(correct_graph_for_left_side_p5, subgraph)

    assert subgraph is not None
    assert production_right_side is not None
    assert _are_graphs_isomorphic(production_right_side, correct_graph_for_p5_right_side)


def test_should_not_transform_removed_edge(
        correct_graph_for_left_side_p5,
        correct_graph_for_p5_right_side,
        production5
):
    correct_graph_for_left_side_p5.remove_edge(0, 1)
    subgraph = production5.find_isomorphic_to_left_side(correct_graph_for_left_side_p5)
    assert subgraph is None


def test_should_not_transform_wrong_position(
        correct_graph_for_left_side_p5,
        correct_graph_for_p5_right_side,
        production5
):
    correct_graph_for_left_side_p5.nodes[3]['position'] = (0.5, 1.5)
    subgraph = production5.find_isomorphic_to_left_side(correct_graph_for_left_side_p5)
    assert subgraph is None


@pytest.fixture
def correct_graph_for_left_side_p5():
    return get_correct_left_side()


@pytest.fixture
def correct_graph_for_p5_right_side():
    return get_expected_right_side()





