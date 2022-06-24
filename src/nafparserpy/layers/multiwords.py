from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.elements import ExternalReferences, Component
from nafparserpy.layers.utils import create_node, ExternalReferenceHolder


@dataclass
class Mw(ExternalReferenceHolder):
    """Represents a multiword expression"""
    id: str
    type: str
    components: List[Component]
    external_references: ExternalReferences = ExternalReferences([])
    lemma: Union[str, None] = None
    """optional attribute"""
    pos: Union[str, None] = None
    """optional attribute"""
    morphofeat: Union[str, None] = None
    """optional attribute"""
    case: Union[str, None] = None
    """optional attribute"""
    status: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        return create_node('mw',
                           children=self.components + [self.external_references],
                           attributes={'id': self.id, 'type': self.type},
                           optional_attrs={'lemma': self.lemma,
                                           'pos': self.pos,
                                           'morphofeat': self.morphofeat,
                                           'case': self.case,
                                           'status': self.status})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Mw(node.get('id'),
                  node.get('type'),
                  [Component.object(n) for n in node.findall('component')],
                  ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                  node.get('lemma'),
                  node.get('pos'),
                  node.get('morphofeat'),
                  node.get('case'),
                  node.get('status'))


@dataclass
class Multiwords:
    """Multiwords layer class"""
    items: List[Mw]
    """list of multiwords"""

    def node(self):
        """Create etree node from object"""
        return create_node('multiwords', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Mw` objects from etree node"""
        return [Mw.object(n) for n in node]
