from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node
from nafparserpy.layers.elements import Span


@dataclass
class Timex3(AttributeGetter):
    """Represents a time expression

    TODO verify element specification in DTD for spans"""
    id: str
    type: str
    spans: List[Span] = field(default_factory=list)
    """optional list of spans"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('beginPoint', 'endPoint', 'quant', 'freq', 'functionInDocument', 'temporalFunction',
    'value', 'valueFromFunction', 'mod', 'anchorTimeID')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id, 'type': self.type})

    def node(self):
        """Create etree node from object"""
        return create_node('timex3', None, self.spans, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Timex3(node.get('id'),
                      node.get('type'),
                      [Span.object(n) for n in node.findall('span')],
                      node.attrib)


@dataclass
class TimeExpressions:
    """TimeExpressions layer class"""
    items: List[Timex3] = field(default_factory=list)
    """list of time expressions"""

    def node(self):
        """Create etree node from object"""
        return create_node('timeExpressions', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Timex3` objects from etree node"""
        return [Timex3.object(n) for n in node]
