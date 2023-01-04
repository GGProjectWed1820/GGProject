# pylint: disable = invalid-name, too-many-locals, fixme

import collections
import dataclasses
import itertools
from itertools import combinations

import networkx as nx

from src.productions.production import Production
from src.vertex_params import VertexParams, VertexType

Node = collections.namedtuple("Node", ["id", "params"])


class Production8(Production):
    @classmethod
    def find_isomorphic_to_left_side(cls, graph: nx.Graph) -> nx.Graph | None:
        isomorphic_graph = nx.Graph()
        isomorphic_graph.add_nodes_from(
            [
                (1, mk_vertex(VertexType.EXTERIOR)),
                (2, mk_vertex(VertexType.EXTERIOR)),

                (3, mk_vertex(VertexType.INTERIOR_USED)),
                (4, mk_vertex(VertexType.INTERIOR_USED)),

                (5, mk_vertex(VertexType.INTERIOR)),
                (6, mk_vertex(VertexType.INTERIOR)),
                (7, mk_vertex(VertexType.INTERIOR)),
                (8, mk_vertex(VertexType.INTERIOR)),

                (9, mk_vertex(VertexType.EXTERIOR)),

                (10, mk_vertex(VertexType.EXTERIOR)),
                (11, mk_vertex(VertexType.EXTERIOR)),

                (12, mk_vertex(VertexType.EXTERIOR))
            ]
        )

        isomorphic_graph.add_edges_from(
            [
                (1, 2),
                (1, 3),
                (1, 4),
                (2, 3),
                (2, 4),
                (3, 5),
                (3, 6),
                (4, 7),
                (4, 8),
                (5, 9),
                (5, 10),
                (6, 10),
                (6, 12),
                (7, 9),
                (7, 11),
                (8, 11),
                (8, 12),
                (9, 10),
                (9, 11),
                (10, 12),
                (11, 12)
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

                    if len(list(get_duplicates_with_label(exterior_nodes))) == 1:
                        return subgraph

        return None

    @classmethod
    def apply(cls, graph: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        if subgraph is None:
            raise ValueError("Subgraph is not isomorphic to left side")

        new_graph = graph.copy()

        nodes: list[Node] = list(
            map(
                lambda node: Node(node[0], VertexParams(**node[1])),
                new_graph.nodes.items(),
            ),
        )

        max_node_id = max(node.id for node in nodes)

        exterior_nodes: list[Node] = list(
            filter(lambda x: x[1].vertex_type == VertexType.EXTERIOR, nodes)
        )

        for e_pairs in get_duplicates_with_label(exterior_nodes):
            for e_left, e_right in combinations(e_pairs, 2):
                common_neighbors = []
                for e_left_n in get_neighbors_of_type(new_graph, nodes, e_left, VertexType.EXTERIOR):
                    if e_left_n in get_neighbors_of_type(new_graph, nodes, e_right, VertexType.EXTERIOR):
                        common_neighbors.append(e_left_n)
                for e1, e2 in combinations(common_neighbors, 2):
                    if is_node_between(e1, e_left, e2) and is_node_between(e1, e_right, e2):
                        new_graph = merge_two_nodes(new_graph, e_left, e_right, max_node_id + 1)
                        return new_graph


def get_duplicates_with_label(nodes: list[Node]):
    result = dict()
    for node in nodes:
        key = (node.params.position, node.params.level)
        if key in result:
            result[key].append(node)
        else:
            result[key] = [node]

    for value in result.values():
        if value.__len__() >= 2:
            yield value


def find_node(node_id: int, nodes: list[Node]) -> Node:
    for node in nodes:
        if node.id == node_id:
            return node


def get_common_neighbors_of_type(graph: nx.Graph, nodes: list[Node], node1: Node, node2: Node, vertex_type: VertexType):
    for node in get_neighbors_of_type(graph, nodes, node1, vertex_type):
        if node in get_neighbors_of_type(graph, nodes, node2, vertex_type):
            yield node


def get_neighbors_of_type(graph: nx.Graph, nodes: list[Node], node: Node, vertex_type: VertexType) -> list[Node]:
    abc = [
        neighbor
        for neighbor in graph.neighbors(node.id)
        if graph.nodes[neighbor]["vertex_type"] == vertex_type
    ]

    return list(map(lambda neighbor: find_node(neighbor, nodes), abc))


def is_node_between(e1: Node, e2: Node, e3: Node) -> bool:
    return e2.params.position[0] == (e1.params.position[0] + e3.params.position[0]) / 2 \
           and e2.params.position[1] == (e1.params.position[1] + e3.params.position[1]) / 2


def merge_two_nodes(graph: nx.Graph, node_1: Node, node_2: Node, new_id: int):
    neighbors = set(graph.neighbors(node_1.id)) | set(graph.neighbors(node_2.id)) - {node_1.id, node_2.id}

    graph.add_nodes_from([(new_id, dataclasses.asdict(node_1.params))])

    graph.remove_node(node_1.id)
    graph.remove_node(node_2.id)

    graph.add_edges_from([(n, new_id) for n in neighbors])
    return graph


def mk_vertex(t):
    return dataclasses.asdict(VertexParams(vertex_type=t, position=(0.0, 0.0), level=0))


def are_types_equal(node1, node2) -> bool:
    return VertexParams(**node1).vertex_type == VertexParams(**node2).vertex_type
