from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node
from nafparserpy.layers.sublayers import Span, ExternalReferences, Sentiment


@dataclass
class Mark(AttributeGetter, IdrefGetter):
    """Represents a mark"""
    id: str
    span: Span
    """span of covered target ids"""
    sentiment: Sentiment = None
    """optional sentiment"""
    externalReferences: ExternalReferences = ExternalReferences([])
    """optional externalReferences"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'case', 'source')"""

    def node(self):
        children = [self.span]
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.externalReferences.items:
            children.append(self.externalReferences)
        all_attrs = {'id': self.id}
        all_attrs.update(self.attrs)
        return create_node('mark', None, children, all_attrs)

    @staticmethod
    def get_obj(node):
        return Mark(node.get('id'),
                    Span.get_obj(node.find('span')),
                    Sentiment.get_obj(node.find('sentiment')),
                    ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                    node.attrib)


@dataclass
class Markables:
    """Markables layer class"""
    items: List[Mark]

    def node(self):
        return create_node('markables', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """retrieves list of Mark objects"""
        return [Mark.get_obj(n) for n in node]

