from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node, ExternalReferenceHolder
from nafparserpy.layers.elements import Component, Span, ExternalReferences, Sentiment


@dataclass
class Term(AttributeGetter, IdrefGetter, ExternalReferenceHolder):
    """Represents a term """
    id: str
    span: Span
    """span of covered idrefs"""
    components: List[Component] = field(default_factory=list)
    """optional list of morphemes in term"""
    external_references: ExternalReferences = ExternalReferences([])
    """optional ExternalReferences"""
    sentiment: Sentiment = None
    """optional sentiment"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'netype', 'case', 'head', 'component_of',
    'compound_type')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id})

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.external_references.items:
            children.append(self.external_references)
        if self.components:
            children.extend(self.components)
        return create_node('term', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Term(node.get('id'),
                    Span.object(node.find('span')),
                    [Component.object(n) for n in node.findall('component')],
                    ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                    Sentiment.object(node.find('sentiment')),
                    node.attrib)

    @staticmethod
    def create(term_id, target_ids, term_attrs):
        """creates a basic term with id, attributes and target ids"""
        return Term(term_id, Span.create(target_ids), external_references=ExternalReferences([]), attrs=term_attrs)


@dataclass
class Terms:
    """Terms layer class"""
    items: List[Term]
    """list of terms"""

    def node(self):
        """Create etree node from object"""
        return create_node('terms', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Term` objects from etree node"""
        return [Term.object(n) for n in node]

