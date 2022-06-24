from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.utils import IdrefGetter, create_node, ExternalReferenceHolder
from nafparserpy.layers.elements import Span, ExternalReferences


@dataclass
class Coref(IdrefGetter, ExternalReferenceHolder):
    """Represents a coreference"""
    id: str
    spans: List[Span]
    """list of coreferent mention spans"""
    external_references: ExternalReferences = ExternalReferences([])
    """optional external references"""
    type: Union[str, None] = None
    """optional type"""
    status: Union[str, None] = None
    """optional status"""

    def target_ids(self):
        """Returns list of target ids covered for each of the layer's spans"""
        return [span.target_ids() for span in self.spans]

    def node(self):
        """Create etree node from object"""
        children = [s for s in self.spans]
        if self.external_references.items:
            children.append(self.external_references)
        return create_node('coref',
                           children=children,
                           attributes={'id': self.id},
                           optional_attrs={'type': self.type, 'status': self.status})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Coref(node.get('id'),
                     [Span.object(n) for n in node.findall('span')],
                     ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                     type=node.get('type'),
                     status=node.get('status'))


@dataclass
class Coreferences:
    """Coreference layer class"""
    items: List[Coref]
    """list of coreferences"""

    def node(self):
        """Create etree node from object"""
        return create_node('coreferences', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Coref` objects from etree node"""
        return [Coref.object(n) for n in node]
