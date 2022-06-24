from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.utils import create_node


@dataclass
class Tunit:
    """Represents a text unit"""
    id: str
    offset: str
    length: str
    type: Union[str, None] = None
    xpath: Union[str, None] = None

    def node(self):
        """Create etree node from object"""
        return create_node('tunit',
                           attributes={'id': self.id, 'offset': self.offset, 'length': self.length},
                           optional_attrs={'type': self.type, 'xpath': self.xpath})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Tunit(node.get('id'), node.get('offset'), node.get('length'), node.get('type'), node.get('xpath'))


@dataclass
class Tunits:
    """Tunits layer class"""
    items: List[Tunit]
    """list of text units"""

    def node(self):
        """Create etree node from object"""
        return create_node('tunits', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Tunit` objects from etree node"""
        return [Tunit.object(n) for n in node]
