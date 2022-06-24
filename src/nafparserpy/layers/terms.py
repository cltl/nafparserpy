from dataclasses import dataclass, field
from typing import List, Union

from nafparserpy.layers.utils import IdrefGetter, create_node, ExternalReferenceHolder
from nafparserpy.layers.elements import Component, Span, ExternalReferences, Sentiment


@dataclass
class Term(IdrefGetter, ExternalReferenceHolder):
    """Represents a term """
    id: str
    span: Span
    """span of covered idrefs"""
    components: List[Component] = field(default_factory=list)
    """optional list of morphemes in term"""
    external_references: ExternalReferences = ExternalReferences([])
    """optional ExternalReferences"""
    sentiment: Union[Sentiment, None] = None
    """optional sentiment"""
    type: Union[str, None] = None
    """optional attribute"""
    lemma: Union[str, None] = None
    """optional attribute"""
    pos: Union[str, None] = None
    """optional attribute"""
    morphofeat: Union[str, None] = None
    """optional attribute"""
    netype: Union[str, None] = None
    """optional attribute"""
    case: Union[str, None] = None
    """optional attribute"""
    head: Union[str, None] = None
    """optional attribute"""
    component_of: Union[str, None] = None
    """optional attribute"""
    compound_type: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.external_references.items:
            children.append(self.external_references)
        if self.components:
            children.extend(self.components)
        return create_node('term',
                           children=children,
                           attributes={'id': self.id},
                           optional_attrs={'type': self.type,
                                           'lemma': self.lemma,
                                           'pos': self.pos,
                                           'morphofeat': self.morphofeat,
                                           'netype': self.netype,
                                           'case': self.case,
                                           'head': self.head,
                                           'component_of': self.component_of,
                                           'compound_type': self.compound_type})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Term(node.get('id'),
                    Span.object(node.find('span')),
                    [Component.object(n) for n in node.findall('component')],
                    ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                    Sentiment.object(node.find('sentiment')),
                    node.get('type'),
                    node.get('lemma'),
                    node.get('pos'),
                    node.get('morphofeat'),
                    node.get('netype'),
                    node.get('case'),
                    node.get('component_of'),
                    node.get('compound_type'))

    @staticmethod
    def create(term_id, target_ids, **attrs):
        """creates a basic term with id, attributes and target ids"""
        return Term(term_id, Span.create(target_ids), **attrs)


@dataclass
class Terms:
    """Terms layer class"""
    items: List[Term]
    """list of terms"""

    def node(self):
        """Create etree node from object"""
        return create_node('terms', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Term` objects from etree node"""
        return [Term.object(n) for n in node]
