from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node
from nafparserpy.layers.sublayers import Span


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

    def node(self):
        attrib = {'id': self.id, 'type': self.type}
        attrib.update(self.attrs)
        return create_node('timex3', None, self.spans, attrib)

    @staticmethod
    def get_obj(node):
        return Timex3(node.get('id'),
                      node.get('type'),
                      [Span.get_obj(n) for n in node.findall('span')],
                      node.attrib)


@dataclass
class TimeExpressions:
    """TimeExpressions layer class"""
    items: List[Timex3] = field(default_factory=list)
    """list of time expressions"""

    def node(self):
        return create_node('timeExpressions', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Timex3.get_obj(n) for n in node]
