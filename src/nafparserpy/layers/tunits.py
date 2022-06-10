from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node


@dataclass
class Tunit(AttributeGetter):
    """Represents a text unit"""
    id: str
    offset: str
    length: str
    attrs: dict = field(default_factory=dict)
    """optional attributes ('type', 'xpath')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id, 'offset': self.offset, 'length': self.length})

    def node(self):
        """Create etree node from object"""
        return create_node('tunit', None, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Tunit(node.get('id'), node.get('offset'), node.get('length'), node.attrib)


@dataclass
class Tunits:
    """Tunits layer class"""
    items: List[Tunit]
    """list of text units"""

    def node(self):
        """Create etree node from object"""
        return create_node('tunits', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Tunit` objects from etree node"""
        return [Tunit.object(n) for n in node]
