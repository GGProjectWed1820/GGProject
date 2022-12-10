from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class VertexType(str, Enum):

    START = "EL"
    START_USED = "el"
    EXTERIOR = "E"
    INTERIOR = "I"
    INTERIOR_USED = "i"


@dataclass()
class VertexParams:

    vertex_type: VertexType
    position: tuple[float, float]
    level: int

    def __eq__(self, o: object) -> bool:
        return (
                isinstance(o, VertexParams)
                and self.vertex_type == o.vertex_type
                and self.level == o.level
                and positions_equal(self.position, o.position)
        )


EPSILON = 1e-5


def positions_equal(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> bool:
    x_diff = abs(pos1[0] - pos2[0])
    y_diff = abs(pos1[1] - pos2[1])

    return x_diff < EPSILON and y_diff < EPSILON
