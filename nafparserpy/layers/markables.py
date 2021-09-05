from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node
from nafparserpy.layers.elements import Span, ExternalReferences, Sentiment


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

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id})

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.externalReferences.items:
            children.append(self.externalReferences)
        return create_node('mark', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Mark(node.get('id'),
                    Span.object(node.find('span')),
                    Sentiment.object(node.find('sentiment')),
                    ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                    node.attrib)


@dataclass
class Markables:
    """Markables layer class"""
    items: List[Mark]

    def node(self):
        """Create etree node from object"""
        return create_node('markables', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Mark` objects from etree node"""
        return [Mark.object(n) for n in node]

