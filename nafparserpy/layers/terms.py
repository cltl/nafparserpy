from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node
from nafparserpy.layers.elements import Component, Span, ExternalReferences, Sentiment


@dataclass
class Term(AttributeGetter, IdrefGetter):
    """Represents a term """
    id: str
    span: Span
    """span of covered idrefs"""
    components: List[Component] = field(default_factory=list)
    """optional list of morphemes in term"""
    externalReferences: ExternalReferences = field(default_factory=ExternalReferences([]))
    """optional ExternalReferences"""
    sentiment: Sentiment = None
    """optional sentiment"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'netype', 'case', 'head', 'component_of',
    'compound_type')"""

    def node(self):
        children = [self.span]
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.externalReferences is not None:
            children.append(self.externalReferences)
        if self.components:
            children.extend(self.components)
        all_attrs = {'id': self.id}
        all_attrs.update(self.attrs)
        return create_node('term', None, children, all_attrs)

    @staticmethod
    def get_obj(node):
        return Term(node.get('id'),
                    Span.get_obj(node.find('span')),
                    [Component.get_obj(n) for n in node.findall('component')],
                    ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                    Sentiment.get_obj(node.find('sentiment')),
                    node.attrib)

    @staticmethod
    def create(term_id, target_ids, term_attrs):
        """creates a basic term with id, attributes and target ids"""
        return Term(term_id, Span.create(target_ids), externalReferences=ExternalReferences([]), attrs=term_attrs)


@dataclass
class Terms:
    """Terms layer class"""
    items: List[Term]
    """list of terms"""

    def node(self):
        return create_node('terms', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """retrieves list of Term objects"""
        return [Term.get_obj(n) for n in node]

