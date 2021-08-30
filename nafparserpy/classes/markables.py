from dataclasses import dataclass, field
from typing import List, Any

from nafparserpy.classes.terms import Sentiment, ExternalReferences
from nafparserpy.utils import AttributeLayer, create_node, AttributeGetter, IdrefGetter
from nafparserpy.classes.span import Span


@dataclass
class Mark(AttributeGetter, IdrefGetter):
    id: str
    span: Span
    sentiment: Sentiment = None
    externalReferences: List[ExternalReferences] = field(default_factory=list)
    attrs: dict = field(default_factory=dict)

    def node(self):
        children = []
        if self.sentiment is not None:
            children.append(self.sentiment)
        children = children + [self.span] + self.externalReferences
        all_attrs = {'id': self.id}
        all_attrs.update(self.attrs)
        return create_node('mark', None, children, all_attrs)

    @staticmethod
    def get_obj(node):
        return Mark(node.get('id'),
                    Span.get_obj(node.find('span')),
                    Sentiment.get_obj(node.find('sentiment')),
                    [ExternalReferences.get_obj(n) for n in node.findall('externalReferences')],
                    node.attrib)


@dataclass
class Markables:
    items: List[Mark]

    def node(self):
        return create_node('markables', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """retrieves list of Mark objects"""
        return [Mark.get_obj(n) for n in node]

