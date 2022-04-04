from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import create_node


@dataclass
class Dep:
    """Represents a Dependency"""
    from_idref: str
    """id of 'from' node"""
    to: str
    """id of 'to' node"""
    rfunc: str
    """dependency relation"""
    attrs: dict = field(default_factory=dict)
    """optional attributes: 'case'"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'from': self.from_idref, 'to': self.to, 'rfunc': self.rfunc})

    def node(self):
        """Create etree node from object"""
        return create_node('dep', None, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Dep(node.get('from'), node.get('to'), node.get('rfunc'), node.attrib)


@dataclass
class Deps:
    """Deps (dependencies) layer class"""
    items: List[Dep]
    """list of dependencies"""

    def node(self):
        """Create etree node from object"""
        return create_node('deps', None, self.items, {})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return [Dep.object(n) for n in node]

