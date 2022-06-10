from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import IdrefGetter, create_node, AttributeGetter, ExternalReferenceHolder
from nafparserpy.layers.elements import Span, ExternalReferences


@dataclass
class Coref(IdrefGetter, AttributeGetter, ExternalReferenceHolder):
    """Represents a coreference"""
    id: str
    spans: List[Span]
    """list of coreferent mention spans"""
    external_references: ExternalReferences = ExternalReferences([])
    """optional external references"""
    attrs: dict = field(default_factory=dict)
    """optional attributes: 'type', 'status'"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id})

    def target_ids(self):
        """Returns list of target ids covered for each of the layer's spans"""
        return [span.target_ids() for span in self.spans]

    def node(self):
        """Create etree node from object"""
        children = [s for s in self.spans]
        if self.external_references.items:
            children.append(self.external_references)
        return create_node('coref', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Coref(node.get('id'),
                     [Span.object(n) for n in node.findall('span')],
                     ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                     node.attrib)


@dataclass
class Coreferences:
    """Coreference layer class"""
    items: List[Coref]
    """list of coreferences"""

    def node(self):
        """Create etree node from object"""
        return create_node('coreferences', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Coref` objects from etree node"""
        return [Coref.object(n) for n in node]
