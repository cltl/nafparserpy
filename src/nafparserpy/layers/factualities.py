from dataclasses import dataclass, field
from typing import List, Union

from nafparserpy.layers.utils import IdrefGetter, create_node
from nafparserpy.layers.elements import Span


@dataclass
class FactVal:
    """Represents a factuality value"""
    value: str
    resource: str
    attrs: dict = field(default_factory=dict)
    confidence: Union[str, None] = None
    """optional attribute"""
    source: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        return create_node('factVal',
                           attributes={'value': self.value, 'resource': self.resource},
                           optional_attrs={'confidence': self.confidence, 'source': self.source})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return FactVal(node.get('value'), node.get('resource'), node.get('confidence'), node.get('source'))


@dataclass
class Factuality(IdrefGetter):
    """Represents a factuality"""
    id: str
    span: Span
    fact_vals: List[FactVal]

    def node(self):
        """Create etree node from object"""
        return create_node('factuality', children=[self.span] + self.fact_vals, attributes={'id': self.id})

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
        return create_node('factualities', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Factuality` objects from etree node"""
        return [Factuality.object(n) for n in node]
