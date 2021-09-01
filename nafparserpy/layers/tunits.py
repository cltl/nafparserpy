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

    def node(self):
        attrib = {'id': self.id, 'offset': self.offset, 'length': self.length}
        attrib.update(self.attrs)
        return create_node('tunit', None, [], attrib)

    @staticmethod
    def get_obj(node):
        return Tunit(node.get('id'), node.get('offset'), node.get('length'), node.attrib)


@dataclass
class Tunits:
    """Tunits layer class"""
    items: List[Tunit]
    """list of text units"""

    def node(self):
        return create_node('tunits', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """returns list of text units in layer"""
        return [Tunit.get_obj(n) for n in node]

