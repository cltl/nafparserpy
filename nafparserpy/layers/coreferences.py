from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import IdrefGetter, create_node, AttributeGetter
from nafparserpy.layers.elements import Span, ExternalReferences


@dataclass
class Coref(IdrefGetter, AttributeGetter):
    """Represents a coreference"""
    id: str
    status: str
    spans: List[Span]
    """list of coreferent mention spans"""
    externalReferences: ExternalReferences = field(default_factory=ExternalReferences([]))
    """optional external references"""
    attrs: dict = field(default_factory=dict)
    """optional attributes: 'type', 'status'"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id, 'status': self.status})

    def target_ids(self):
        """Returns list of target ids covered for each of the layer's spans"""
        return [span.target_ids() for span in self.spans]

    def node(self):
        """Create etree node from object"""
        children = self.spans
        if self.externalReferences.items:
            children.append(self.externalReferences)
        return create_node('coref', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Coref(node.get('id'),
                     node.get('status'),
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
