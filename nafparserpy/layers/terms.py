from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.sublayers import Component
from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node
from nafparserpy.layers.sublayers import Span, ExternalReferences, Sentiment


@dataclass
class Term(AttributeGetter, IdrefGetter):
    """Represents a term """
    id: str
    span: Span
    """span of covered idrefs"""
    externalReferences: ExternalReferences = field(default_factory=ExternalReferences([]))
    """optional ExternalReferences"""
    component: Component = None
    """optional component"""
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
        if self.component is not None:
            children.append(self.component)
        all_attrs = {'id': self.id}
        all_attrs.update(self.attrs)
        return create_node('term', None, children, all_attrs)

    @staticmethod
    def get_obj(node):
        return Term(node.get('id'),
                    Span.get_obj(node.find('span')),
                    ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                    Component.get_obj(node.find('component')),
                    Sentiment.get_obj(node.find('sentiment')),
                    node.attrib)

    @staticmethod
    def create(term_id, target_ids, term_attrs):
        """creates a basic term with id, attributes and target ids"""
        return Term(term_id, Span.create(target_ids), ExternalReferences([]), attrs=term_attrs)


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

