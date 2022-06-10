from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.elements import ExternalReferences, Component
from nafparserpy.layers.utils import AttributeGetter, create_node, ExternalReferenceHolder


@dataclass
class Mw(AttributeGetter, ExternalReferenceHolder):
    """Represents a multiword expression"""
    id: str
    type: str
    components: List[Component]
    external_references: ExternalReferences = ExternalReferences([])
    attrs: dict = field(default_factory=dict)

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id, 'type': self.type})

    def node(self):
        """Create etree node from object"""
        return create_node('mw', None, self.components + [self.external_references], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Mw(node.get('id'),
                  node.get('type'),
                  [Component.object(n) for n in node.findall('component')],
                  ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                  node.attrib)


@dataclass
class Multiwords:
    """Multiwords layer class"""
    items: List[Mw]
    """list of multiwords"""

    def node(self):
        """Create etree node from object"""
        return create_node('multiwords', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Mw` objects from etree node"""
        return [Mw.object(n) for n in node]
