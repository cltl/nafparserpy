from dataclasses import dataclass
from typing import List

from nafparserpy.layers.utils import create_node, AttributeGetter


@dataclass
class Chunk(AttributeGetter):
    """Represents a chunk"""
    id: str
    head: str
    phrase: str
    attrs: dict
    """optional attributes: 'case'"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id, 'head': self.head, 'phrase': self.phrase})

    def node(self):
        """Create etree node from object"""
        return create_node('chunk', None, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Chunk(node.get('id'), node.get('head'), node.get('phrase'), node.attrib)


@dataclass
class Chunks:
    """Chunks layer class"""
    items: List[Chunk]

    def node(self):
        """Create etree node from object"""
        return create_node('chunks', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Chunk` objects from etree node"""
        return [Chunk.object(n) for n in node]
