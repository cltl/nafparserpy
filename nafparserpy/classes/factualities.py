from dataclasses import dataclass, field
from typing import List

from nafparserpy.utils import create_node, AttributeGetter, IdrefGetter
from nafparserpy.classes.span import Span


@dataclass
class FactVal(AttributeGetter):
    value: str
    resource: str
    attrs: dict = field(default_factory=dict)

    def node(self):
        attrib = {'value': self.value, 'resource': self.resource}
        attrib.update(self.attrs)
        return create_node('factVal', None, [], attrib)

    @staticmethod
    def get_obj(node):
        return FactVal(node.get('value'), node.get('resource'), node.attrib)


@dataclass
class Factuality(IdrefGetter):
    id: str
    span: Span
    fact_vals: List[FactVal]

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('factuality', None, [self.span] + self.fact_vals)

    @staticmethod
    def get_obj(node):
        return Factuality(node.get('id'),
                          Span.get_obj(node.find('span')),
                          [FactVal.get_obj(n) for n in node.findall('factVal')])


@dataclass
class Factualities:
    items: List[Factuality]

    def node(self):
        return create_node('factualities', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Factuality.get_obj(n) for n in node]
