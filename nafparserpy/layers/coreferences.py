from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import IdrefGetter, create_node
from nafparserpy.layers.elements import Span, ExternalReferences


@dataclass
class Coref(IdrefGetter):
    """Represents a coreference"""
    id: str
    status: str
    spans: List[Span]
    """list of coreferent mention spans"""
    externalReferences: ExternalReferences = field(default_factory=ExternalReferences([]))
    """optional external references"""
    attrs: dict = field(default_factory=dict)
    """optional attributes: 'type', 'status'"""

    def target_ids(self):
        """Returns list of target ids covered for each of the layer's spans"""
        return [span.target_ids() for span in self.spans]

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        children = self.spans
        if self.externalReferences.items:
            children.append(self.externalReferences)
        return create_node('coref', None, children, attrib)

    @staticmethod
    def get_obj(node):
        return Coref(node.get('id'),
                     node.get('status'),
                     [Span.get_obj(n) for n in node.findall('span')],
                     ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                     node.get('type'))


@dataclass
class Coreferences:
    """Coreference layer class"""
    items: List[Coref]
    """list of coreferences"""

    def node(self):
        return create_node('coreferences', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Coref.get_obj(n) for n in node]
