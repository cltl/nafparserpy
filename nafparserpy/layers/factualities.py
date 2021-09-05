from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node
from nafparserpy.layers.elements import Span


@dataclass
class FactVal(AttributeGetter):
    """Represents a factuality value"""
    value: str
    resource: str
    attrs: dict = field(default_factory=dict)
    """optional attributes ('confidence', 'source')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'value': self.value, 'resource': self.resource})

    def node(self):
        """Create etree node from object"""
        return create_node('factVal', None, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return FactVal(node.get('value'), node.get('resource'), node.attrib)


@dataclass
class Factuality(IdrefGetter):
    """Represents a factuality"""
    id: str
    span: Span
    fact_vals: List[FactVal]

    def node(self):
        """Create etree node from object"""
        return create_node('factuality', None, [self.span] + self.fact_vals, {'id': self.id})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Factuality(node.get('id'),
                          Span.object(node.find('span')),
                          [FactVal.object(n) for n in node.findall('factVal')])


@dataclass
class Factualities:
    """Factualities layer class"""
    items: List[Factuality]
    """list of factualities"""

    def node(self):
        """Create etree node from object"""
        return create_node('factualities', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Factuality` objects from etree node"""
        return [Factuality.object(n) for n in node]
