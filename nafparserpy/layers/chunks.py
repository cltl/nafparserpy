from dataclasses import dataclass
from typing import List

from nafparserpy.layers.utils import create_node


@dataclass
class Chunk:
    id: str
    head: str
    phrase: str
    case: str = None

    def node(self):
        attrs = {'id': self.id, 'head': self.head, 'phrase': self.phrase}
        if self.case is not None:
            attrs.update({'case': self.case})
        return create_node('chunk', None, [], attrs)

    @staticmethod
    def get_obj(node):
        return Chunk(node.get('id'), node.get('head'), node.get('phrase'), node.get('case'))


@dataclass
class Chunks:
    items: List[Chunk]

    def node(self):
        return create_node('deps', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Chunk.get_obj(n) for n in node]
