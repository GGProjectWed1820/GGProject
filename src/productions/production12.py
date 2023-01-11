from dataclasses import asdict

import networkx as nx

from src.vertex_params import VertexParams, VertexType
from src.productions.production import Production
import collections
from typing import Callable
import itertools

NodeId = int
Node = collections.namedtuple("Node", ["id", "params"])


def mk_vertex(t):
    return asdict(VertexParams(vertex_type=t, position=(0.0, 0.0), level=0))


def are_types_equal(node1, node2) -> bool:
    return VertexParams(**node1).vertex_type == VertexParams(**node2).vertex_type


def graph_id_sequence(graph: nx.Graph) -> Callable[[], NodeId]:
    next_id = max(graph.nodes) + 1

    def internal():
        nonlocal next_id
        rv = next_id
        next_id += 1
        return rv

    return internal


def get_duplicates_with_labels(nodes: list[Node]):
    result = dict()
    for node in nodes:
        key = (node.params.position, node.params.level)
        if key in result:
            result[key].append(node)
        else:
            result[key] = [node]

    for value in result.values():
        if len(value) >= 2:
            yield value


def _merge_two_nodes(graph: nx.Graph, node_1: Node, node_2: Node, new_id: int):
    neighbors = set(graph.neighbors(node_1.id)) | set(graph.neighbors(node_2.id)) - {node_1.id, node_2.id}

    graph.add_nodes_from([(new_id, asdict(node_1.params))])
    graph.add_edges_from([(n, new_id) for n in neighbors])

    graph.remove_node(node_1.id)
    graph.remove_node(node_2.id)

    return graph, new_id


class Production12(Production):
    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        isomorphic_graph = nx.Graph()

        isomorphic_graph.add_nodes_from(
            [
                (1, mk_vertex(VertexType.EXTERIOR)),
                (2, mk_vertex(VertexType.EXTERIOR)),

                (3, mk_vertex(VertexType.INTERIOR_USED)),
                (4, mk_vertex(VertexType.INTERIOR_USED)),

                (5, mk_vertex(VertexType.EXTERIOR)),
                (6, mk_vertex(VertexType.EXTERIOR)),

                (7, mk_vertex(VertexType.INTERIOR)),

                (8, mk_vertex(VertexType.EXTERIOR)),
                (9, mk_vertex(VertexType.EXTERIOR)),

                (10, mk_vertex(VertexType.INTERIOR)),
            ]
        )

        isomorphic_graph.add_edges_from(
            [
                (1, 2),
                (1, 3),
                (2, 3),
                (2, 4),
                (1, 4),

                (3, 7),
                (5, 6),
                (6, 7),
                (7, 5),

                (4, 10),
                (8, 9),
                (9, 10),
                (8, 10),
            ]
        )

        node_diff = len(graph.nodes) - len(isomorphic_graph.nodes)

        if node_diff >= 0:
            all_connected_subgraphs = []

            for SG in (graph.subgraph(selected_nodes) for selected_nodes in
                       itertools.combinations(graph, len(isomorphic_graph))):
                if nx.is_connected(SG):
                    all_connected_subgraphs.append(SG)

            for subgraph in all_connected_subgraphs:
                if nx.is_isomorphic(subgraph, isomorphic_graph, node_match=are_types_equal):
                    nodes: list[Node] = list(
                        map(
                            lambda node: Node(node[0], VertexParams(**node[1])),
                            subgraph.nodes.items(),
                        ),
                    )

                    exterior_nodes: list[Node] = list(
                        filter(lambda x: x[1].vertex_type == VertexType.EXTERIOR, nodes)
                    )
                    for pair in list(get_duplicates_with_labels(exterior_nodes)):
                        if pair[0].params.position != pair[1].params.position:
                            continue
                    if len(list(get_duplicates_with_labels(exterior_nodes))) == 2:
                        return subgraph

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        if cls.find_isomorphic_to_left_side(subgraph) is None:
            raise ValueError("Subgraph is not isomorphic to left side")

        next_id_val_fun = graph_id_sequence(graph)

        new_graph = graph.copy()

        nodes: list[Node] = list(
            map(
                lambda node: Node(node[0], VertexParams(**node[1])),
                subgraph.nodes.items(),
            ),
        )

        exterior_nodes: list[Node] = list(
            filter(lambda x: x[1].vertex_type == VertexType.EXTERIOR, nodes)
        )
        new_ids = []
        for e_pairs in get_duplicates_with_labels(exterior_nodes):
            for e_left, e_right in itertools.combinations(e_pairs, 2):
                new_graph, new_id = _merge_two_nodes(new_graph, e_left, e_right, next_id_val_fun())
                new_ids.append(new_id)

        return new_graph
