from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.utils import IdrefGetter, create_node, ExternalReferenceHolder
from nafparserpy.layers.elements import Span, ExternalReferences, Sentiment


@dataclass
class Mark(IdrefGetter, ExternalReferenceHolder):
    """Represents a mark"""
    id: str
    span: Span
    """span of covered target ids"""
    sentiment: Union[Sentiment, None] = None
    """optional sentiment"""
    external_references: ExternalReferences = ExternalReferences([])
    """optional externalReferences"""
    type: Union[str, None] = None
    """optional attribute"""
    lemma: Union[str, None] = None
    """optional attribute"""
    pos: Union[str, None] = None
    """optional attribute"""
    morphofeat: Union[str, None] = None
    """optional attribute"""
    case: Union[str, None] = None
    """optional attribute"""
    source: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.external_references.items:
            children.append(self.external_references)
        return create_node('mark',
                           children=children,
                           attributes={'id': self.id},
                           optional_attrs={'type': self.type,
                                           'lemma': self.lemma,
                                           'pos': self.pos,
                                           'morphofeat': self.morphofeat,
                                           'case': self.case,
                                           'source': self.source})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Mark(node.get('id'),
                    Span.object(node.find('span')),
                    Sentiment.object(node.find('sentiment')),
                    ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                    node.get('type'),
                    node.get('lemma'),
                    node.get('pos'),
                    node.get('morphofeat'),
                    node.get('case'),
                    node.get('source'))


@dataclass
class Markables:
    """Markables layer class"""
    items: List[Mark]

    def node(self):
        """Create etree node from object"""
        return create_node('markables', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Mark` objects from etree node"""
        return [Mark.object(n) for n in node]
