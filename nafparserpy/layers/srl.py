from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node
from nafparserpy.layers.sublayers import Span, ExternalReferences


@dataclass
class Role(AttributeGetter):
    id: str
    span: Span
<<<<<<< HEAD
    external_references: ExternalReferences = ExternalReferences([])
=======
    external_references: ExternalReferences = field(default_factory=ExternalReferences([]))
>>>>>>> wip
    attrs: dict = field(default_factory=dict)
    # optional attributes ('confidence' and 'status')

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('role', None, [self.span] + [self.external_references], attrib)

    @staticmethod
    def get_obj(node):
        return Role(node.get('id'),
<<<<<<< HEAD
                    Span.get_obj(node.findall('span')),
                    ExternalReferences(ExternalReferences.get_obj(node.findall('externalReferences'))),
=======
                    Span.get_obj(node.find('span')),
                    ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
>>>>>>> wip
                    node.attrib)


@dataclass
class Predicate(AttributeGetter):
    """Represents a predicate"""
    id: str
    span: Span
<<<<<<< HEAD
    external_references: ExternalReferences = ExternalReferences([])
    role: List[Role] = field(default_factory=list)
=======
    role: Role
    external_references: ExternalReferences = field(default_factory=ExternalReferences([]))
>>>>>>> wip
    attrs: dict = field(default_factory=dict)
    # optional attributes ('confidence', 'status')

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('predicate', None, [self.span] + [self.external_references] + [self.role], attrib)

    @staticmethod
    def get_obj(node):
        return Predicate(node.get('id'),
<<<<<<< HEAD
                         Span.get_obj(node.findall('span')),
                         ExternalReferences(ExternalReferences.get_obj(node.findall('externalReferences'))),
                         [Role.get_obj(n) for n in node.findall('role')],
=======
                         Span.get_obj(node.find('span')),
                         Role.get_obj(node.find('role')),
                         ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
>>>>>>> wip
                         node.attrib)


@dataclass
class Srl:
    """SRL layer class"""
    items: List[Predicate]
    # list of predicates

    def node(self):
        return create_node('srl', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Predicate.get_obj(n) for n in node]
