from dataclasses import dataclass, field
from typing import List

from nafparserpy.utils import create_node, AttributeGetter
from nafparserpy.classes.span import Span


@dataclass
class TLink:
    id: str
    from_idref: str
    from_type: str
    to_idref: str
    to_type: str
    rel_type: str

    def node(self):
        attrib = {'id': self.id,
                  'from': self.from_idref,
                  'fromType': self.from_type,
                  'to': self.to_idref,
                  'toType': self.to_type,
                  'relType': self.rel_type}
        return create_node('tlink', None, [], attrib)

    @staticmethod
    def get_obj(node):
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

    def node(self):
        create_node('predicateAnchor', None, self.spans, self.attrs)

    @staticmethod
    def get_obj(node):
        return PredicateAnchor([Span.get_obj(n) for n in node], node.attrib)


@dataclass
class TemporalRelations:
    tlinks: List[TLink] = field(default_factory=list)
    predicate_anchors: List[PredicateAnchor] = field(default_factory=list)

    def node(self):
        return create_node('temporalRelations', None, self.tlinks + self.predicate_anchors, {})

    @staticmethod
    def get_obj(node):
        return TemporalRelations([TLink.get_obj(n) for n in node.findall('tlink')],
                                 [PredicateAnchor.get_obj(n) for n in node.findall('predicateAnchor')])
