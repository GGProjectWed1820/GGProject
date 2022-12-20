import collections
import contextlib
import copy
import dataclasses
import itertools
import math
from typing import Sequence, Callable, Tuple, List
import networkx as nx
from src.vertex_params import VertexParams, VertexType
from src.productions.production import Production

NodeId = int
Node = collections.namedtuple("Node", ["id", "params"])


def _get_neighbors_of_type(
        graph: nx.Graph, node_id: NodeId, vertex_type: VertexType) -> List[NodeId]:
    return [
        neighbor
        for neighbor in graph.neighbors(node_id)
        if graph.nodes[neighbor]["vertex_type"] == vertex_type
    ]


def _graph_id_sequence(graph: nx.Graph) -> Callable[[], NodeId]:
    next_id = max(graph.nodes) + 1

    def internal():
        nonlocal next_id
        rv = next_id
        next_id += 1
        return rv

    return internal


def _node_distance(params1: VertexParams, params2: VertexParams) -> float:
    x1, y1 = params1.position
    x2, y2 = params2.position
    x = x1 - x2
    y = y1 - y2
    return math.sqrt(x * x + y * y)


def _find_hypotenuse_nodes(triangle_graph_nodes: Sequence[Node]) -> Tuple[Node, ...]:
    assert len(triangle_graph_nodes) == 3

    return max(
        itertools.combinations(triangle_graph_nodes, 2),
        key=lambda node_pair: _node_distance(node_pair[0].params, node_pair[1].params),
    )


def _node_line_middle(
        params1: VertexParams, params2: VertexParams) -> Tuple[float, float]:
    x1, y1 = params1.position
    x2, y2 = params2.position
    return (x1 + x2) / 2, (y1 + y2) / 2


def _move_down_node(params: VertexParams) -> VertexParams:
    return dataclasses.replace(params, level=params.level + 1)


def _hypotenuse_middle_node_params(node1: Node, node2: Node) -> VertexParams:
    mid_x, mid_y = _node_line_middle(node1.params, node2.params)
    return dataclasses.replace(
        node1.params, position=(mid_x, mid_y), level=node1.params.level + 1
    )


def _get_params_with_lower_level(nodes: Sequence[Node]) -> Sequence[VertexParams]:
    return list(map(lambda node: _move_down_node(node.params), nodes))


def _create_edges(
        used_internal_node: Node,
        new_internal_node: Node,
        new_nodes: Sequence[Node]) -> Sequence[Tuple[NodeId, NodeId]]:
    print(f'NODE OF 0 {new_nodes[0]}')
    return [
        (used_internal_node.id, new_internal_node.id),
        (new_internal_node.id, new_nodes[0].id),
        (new_internal_node.id, new_nodes[1].id),
        (new_internal_node.id, new_nodes[2].id),
        (new_nodes[0].id, new_nodes[1].id),
        (new_nodes[1].id, new_nodes[2].id),
        (new_nodes[2].id, new_nodes[0].id)
    ]


class Production9(Production):
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph:
        for node_id, params in graph.nodes.items():
            if (VertexParams(**params)).vertex_type != VertexType.INTERIOR:
                continue

            exterior_neighbors = _get_neighbors_of_type(
                graph, node_id, VertexType.EXTERIOR
            )
            if len(exterior_neighbors) != 3:
                continue

            with contextlib.suppress(nx.NetworkXNoCycle):
                nx.find_cycle(graph.subgraph(exterior_neighbors))
                return graph.subgraph([node_id, *exterior_neighbors])

        return None

    def apply(self, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        assert len(subgraph.nodes) == 4

        new_graph = copy.deepcopy(graph)
        next_id_val_fun = _graph_id_sequence(graph)
        subgraph_nodes: List[Node] = list(
            map(
                lambda node: Node(node[0], VertexParams(**node[1])),
                subgraph.nodes.items(),
            )
        )
        internal_node = next(
            filter(
                lambda node: node.params.vertex_type == VertexType.INTERIOR,
                subgraph_nodes,
            )
        )

        used_internal_node = Node(
            internal_node.id,
            dataclasses.replace(
                internal_node.params, vertex_type=VertexType.INTERIOR_USED
            ),
        )
        new_internal_node = Node(
            next_id_val_fun(),
            _get_params_with_lower_level([internal_node])[0]
        )

        external_nodes = list(
            filter(lambda node: node != internal_node, subgraph_nodes)
        )

        new_nodes = list(
            map(
                lambda params: Node(next_id_val_fun(), params),
                _get_params_with_lower_level(external_nodes),
            )
        )
        new_level_nodes = new_nodes + [new_internal_node]
        new_level_raw_nodes = map(
            lambda node: (node.id, dataclasses.asdict(node.params)), new_level_nodes
        )

        new_level_edges = _create_edges(
            used_internal_node,
            new_internal_node,
            new_level_nodes
        )

        new_graph.add_nodes_from(new_level_raw_nodes)
        new_graph.add_edges_from(new_level_edges)

        return new_graph
