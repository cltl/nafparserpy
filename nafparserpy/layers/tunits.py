from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node


@dataclass
class Tunit(AttributeGetter):
    id: str
    offset: str
    length: str
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node('tunit', None, [], self.attrs)

    @staticmethod
    def get_obj(node):
        return Tunit(node.get('id'), node.get('offset'), node.get('length'), node.attrib)


@dataclass
class Tunits:
    items: List[Tunit]

    def node(self):
        return create_node('tunits', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """retrieves list of Tunit objects in Tunit layer"""
        return [Tunit.get_obj(n) for n in node]

