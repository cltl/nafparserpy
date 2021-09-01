from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.sublayers import ExternalReferences, Component
from nafparserpy.layers.utils import AttributeGetter, create_node


@dataclass
class Mw(AttributeGetter):
    """Represents a multiword"""
    id: str
    type: str
    components: List[Component]
    externalRefs: ExternalReferences = ExternalReferences([])
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node('mw', None, self.components + [self.externalRefs], self.attrs)

    @staticmethod
    def get_obj(node):
        return Mw(node.get('id'),
                  node.get('type'),
                  [Component.get_obj(n) for n in node.findall('component')],
                  ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                  node.attrib)


@dataclass
class Multiwords:
    """Multiwords layer class"""
    items: List[Mw]

    def node(self):
        return create_node('multiwords', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Mw.get_obj(n) for n in node]

