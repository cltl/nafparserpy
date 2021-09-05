from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node
from nafparserpy.layers.elements import Span


@dataclass
class TLink:
    """Represents a temporal link"""
    id: str
    from_idref: str
    """represents the 'from' NAF attribute"""
    fromType: str
    to: str
    toType: str
    reTlype: str

    def node(self):
        """Create etree node from object"""
        attrib = {'id': self.id,
                  'from': self.from_idref,
                  'fromType': self.fromType,
                  'to': self.to,
                  'toType': self.toType,
                  'relType': self.relType}
        return create_node('tlink', None, [], attrib)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return TLink(node.get('id'),
                     node.get('from'),
                     node.get('fromType'),
                     node.get('to'),
                     node.get('toType'),
                     node.get('relType'))


@dataclass
class PredicateAnchor(AttributeGetter):
    spans: List[Span]
    attrs: dict = field(default_factory=dict)
    """optional attributes ('id', 'anchorTime', 'beginPoint', 'endPoint')"""

    def node(self):
        """Create etree node from object"""
        create_node('predicateAnchor', None, self.spans, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return PredicateAnchor([Span.object(n) for n in node], node.attrib)


@dataclass
class TemporalRelations:
    """Temporal Relations layer class

    TODO check the specification (is the DTD too liberal?)"""
    tlinks: List[TLink] = field(default_factory=list)
    predicate_anchors: List[PredicateAnchor] = field(default_factory=list)

    def node(self):
        """Create etree node from object"""
        return create_node('temporalRelations', None, self.tlinks + self.predicate_anchors, {})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return TemporalRelations([TLink.object(n) for n in node.findall('tlink')],
                                 [PredicateAnchor.object(n) for n in node.findall('predicateAnchor')])
