from dataclasses import dataclass, field
from typing import List

from nafparserpy.classes.terms import ExternalReferences
from nafparserpy.utils import create_node, AttributeGetter, IdrefGetter
from nafparserpy.classes.span import Span


@dataclass
class Entity(AttributeGetter, IdrefGetter):
    """Entity class

    The implementation differs from the current DTD, and follows
    ELEMENT entity (span,externalReferences*)
    rather than:
    ELEMENT entity (span|externalReferences)+
    """
    id: str
    span: Span      # the current DTD sees span as optional
    external_references: List[ExternalReferences] = field(default_factory=list)
    attrs: dict = field(default_factory=dict)

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('entity', None, [self.span] + self.external_references, attrib)

    @staticmethod
    def get_obj(node):
        return Entity(node.get('id'),
                      Span.get_obj(node.find('span')),
                      [ExternalReferences.get_obj(n) for n in node.findall('externalReferences')],
                      node.attrib)


@dataclass
class Entities:
    items: List[Entity]

    def node(self):
        return create_node('entities', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Entity.get_obj(n) for n in node]
