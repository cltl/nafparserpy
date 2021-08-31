from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node
from nafparserpy.layers.sublayers import Span, ExternalReferences


@dataclass
class Role(AttributeGetter):
    id: str
    span: Span
    external_references: ExternalReferences = ExternalReferences([])
    attrs: dict = field(default_factory=dict)

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('role', None, [self.span] + [self.external_references], attrib)

    @staticmethod
    def get_obj(node):
        return Role(node.get('id'),
                    Span.get_obj(node.findall('span')),
                    ExternalReferences(ExternalReferences.get_obj(node.findall('externalReferences'))),
                    node.attrib)


@dataclass
class Predicate(AttributeGetter):
    id: str
    span: Span
    external_references: ExternalReferences = ExternalReferences([])
    role: List[Role] = field(default_factory=list)
    attrs: dict = field(default_factory=dict)

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('predicate', None, [self.span] + [self.external_references] + [self.role], attrib)

    @staticmethod
    def get_obj(node):
        return Predicate(node.get('id'),
                         Span.get_obj(node.findall('span')),
                         ExternalReferences(ExternalReferences.get_obj(node.findall('externalReferences'))),
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
