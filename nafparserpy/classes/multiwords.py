from dataclasses import dataclass, field
from typing import List

from nafparserpy.classes.terms import Component, ExternalReferences
from nafparserpy.utils import create_node, AttributeGetter


@dataclass
class Mw(AttributeGetter):
    id: str
    type: str
    components: List[Component]
    externalRefs: List[ExternalReferences]
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node('mw', None, self.components + self.externalRefs, self.attrs)

    @staticmethod
    def get_obj(node):
        return Mw(node.get('id'),
                  node.get('type'),
                  [Component.get_obj(n) for n in node.findall('component')],
                  [ExternalReferences.get_obj(n) for n in node.findall('externalReferences')],
                  node.attrib)


@dataclass
class Multiwords:
    items: List[Mw]

    def node(self):
        return create_node('multiwords', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Mw.get_obj(n) for n in node]

