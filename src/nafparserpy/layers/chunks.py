from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.utils import create_node

from nafparserpy.layers.elements import Span


@dataclass
class Chunk:
    """Represents a chunk"""
    id: str
    head: str
    """target id of chunk's head"""
    phrase: str
    """chunk label (NP, PP, etc.)"""
    span: Span
    """chunk span"""
    case: Union[str, None] = None
    """optional attribute: 'case'"""

    def node(self):
        """Create etree node from object"""
        return create_node('chunk',
                           children=[self.span],
                           attributes={'id': self.id, 'head': self.head, 'phrase': self.phrase},
                           optional_attrs={'case': self.case})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Chunk(node.get('id'), node.get('head'), node.get('phrase'), Span.object(node.find('span')), node.get('case'))


@dataclass
class Chunks:
    """Chunks layer class"""
    items: List[Chunk]

    def node(self):
        """Create etree node from object"""
        return create_node('chunks', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Chunk` objects from etree node"""
        return [Chunk.object(n) for n in node]
