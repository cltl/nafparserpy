from dataclasses import dataclass, field
from typing import List, Union

from nafparserpy.layers.utils import create_node
from nafparserpy.layers.elements import Span


@dataclass
class TLink:
    """Represents a temporal link"""
    id: str
    from_idref: str
    """represents the 'from' NAF attribute"""
    to: str
    fromType: str
    toType: str
    relType: str

    def node(self):
        """Create etree node from object"""
        attrib = {'id': self.id,
                  'from': self.from_idref,
                  'to': self.to,
                  'fromType': self.fromType,
                  'toType': self.toType,
                  'relType': self.relType}
        return create_node('tlink', attributes=attrib)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return TLink(node.get('id'),
                     node.get('from'),
                     node.get('to'),
                     node.get('fromType'),
                     node.get('toType'),
                     node.get('relType'))


@dataclass
class PredicateAnchor:
    spans: List[Span]
    attrs: dict = field(default_factory=dict)
    """optional attributes ('id', 'anchorTime', 'beginPoint', 'endPoint')"""
    id: Union[str, None] = None
    anchorTime: Union[str, None] = None
    beginPoint: Union[str, None] = None
    endPoint: Union[str, None] = None

    def node(self):
        """Create etree node from object"""
        create_node('predicateAnchor', children=self.spans, optional_attrs={
            'id': self.id, 'anchorTime': self.anchorTime, 'beginPoint': self.beginPoint, 'endPoint': self.endPoint
        })

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return PredicateAnchor([Span.object(n) for n in node],
                               node.get('id'),
                               node.get('anchorTime'),
                               node.get('beginPoint'),
                               node.get('endPoint'))


@dataclass
class TemporalRelations:
    """Temporal Relations layer class"""
    tlinks: List[TLink] = field(default_factory=list)
    predicate_anchors: List[PredicateAnchor] = field(default_factory=list)

    def node(self):
        """Create etree node from object"""
        return create_node('temporalRelations', children=self.tlinks + self.predicate_anchors)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return TemporalRelations([TLink.object(n) for n in node.findall('tlink')],
                                 [PredicateAnchor.object(n) for n in node.findall('predicateAnchor')])
