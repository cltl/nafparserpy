from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node
from nafparserpy.layers.sublayers import Span, ExternalReferences


@dataclass
class Role(AttributeGetter):
    id: str
    spans: List[Span]  # FIXME we follow the DTD here
    external_references: List[ExternalReferences]
    attrs: dict = field(default_factory=dict)

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('role', None, self.spans + self.external_references, attrib)

    @staticmethod
    def get_obj(node):
        return Role(node.get('id'),
                    [Span.get_obj(n) for n in node.findall('span')],
                    [ExternalReferences.get_obj(n) for n in node.findall('externalReferences')],
                    node.attrib)


@dataclass
class Predicate(AttributeGetter):
    id: str
    span: List[Span]  # FIXME we follow the DTD here
    external_references: List[ExternalReferences]
    role: List[Role]
    attrs: dict = field(default_factory=dict)

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('predicate', None, self.span + self.external_references + self.role, attrib)

    @staticmethod
    def get_obj(node):
        return Predicate(node.get('id'),
                         [Span.get_obj(n) for n in node.findall('span')],
                         [ExternalReferences.get_obj(n) for n in node.findall('externalReferences')],
                         [Role.get_obj(n) for n in node.findall('role')],
                         node.attrib)


@dataclass
class Srl:
    items: List[Predicate]

    def node(self):
        return create_node('srl', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Predicate.get_obj(n) for n in node]
