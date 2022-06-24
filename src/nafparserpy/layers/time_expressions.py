from dataclasses import dataclass, field
from typing import List, Union

from nafparserpy.layers.utils import create_node, IdrefGetter
from nafparserpy.layers.elements import Span


@dataclass
class Timex3(IdrefGetter):
    """Represents a temporal expression """
    id: str
    type: str
    span: Span
    """optional list of spans"""
    beginPoint: Union[str, None] = None
    endPoint: Union[str, None] = None
    quant: Union[str, None] = None
    freq: Union[str, None] = None
    functionInDocument: Union[str, None] = None
    temporalFunction: Union[str, None] = None
    value: Union[str, None] = None
    valueFromFunction: Union[str, None] = None
    mod: Union[str, None] = None
    anchorTimeID: Union[str, None] = None

    def node(self):
        """Create etree node from object"""
        return create_node('timex3',
                           children=[self.span],
                           attributes={'id': self.id, 'type': self.type},
                           optional_attrs={'beginPoint': self.beginPoint, 'endPoint': self.endPoint,
                                           'quant': self.quant, 'freq': self.freq,
                                           'functionInDocument': self.functionInDocument,
                                           'temporalFunction': self.temporalFunction,
                                           'value': self.value, 'valueFromFunction': self.valueFromFunction,
                                           'mod': self.mod, 'anchorTimeID': self.anchorTimeID})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Timex3(node.get('id'),
                      node.get('type'),
                      Span.object(node.find('span')),
                      node.get('beginPoint'), node.get('endPoint'), node.get('quant'), node.get('freq'),
                      node.get('functionInDocument'), node.get('temporalFunction'),
                      node.get('value'), node.get('valueFromFunction'), node.get('mod'), node.get('anchorTimeID'))


@dataclass
class TimeExpressions:
    """TimeExpressions layer class"""
    items: List[Timex3] = field(default_factory=list)
    """list of time expressions"""

    def node(self):
        """Create etree node from object"""
        return create_node('timeExpressions', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Timex3` objects from etree node"""
        return [Timex3.object(n) for n in node]
