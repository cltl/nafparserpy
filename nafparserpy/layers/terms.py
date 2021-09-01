from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.sublayers import Component
from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node
from nafparserpy.layers.sublayers import Span, ExternalReferences, Sentiment


@dataclass
class Term(AttributeGetter, IdrefGetter):
    """Represents a term.

    TODO check the DTD"""
    id: str
    sentiment: Sentiment = None
    span: Span = None
    externalReferences: ExternalReferences = ExternalReferences([])
    component: Component = None
    attrs: dict = field(default_factory=dict)
    # optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'netype', 'case', 'head', 'component_of',
    # 'compound_type')

    def node(self):
        children = []
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.span is not None:
            children.append(self.span)
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
                    Sentiment.get_obj(node.find('sentiment')),
                    Span.get_obj(node.find('span')),
                    ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                    Component.get_obj(node.find('component')),
                    node.attrib)

    @staticmethod
    def create(term_id, term_attrs, target_ids):
        """creates a basic term with id, attributes and target ids"""
        return Term(term_id, span=Span.create(target_ids), attrs=term_attrs)


@dataclass
class Terms:
    """Terms layer class"""
    items: List[Term]
    # list of terms

    def node(self):
        return create_node('terms', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """retrieves list of Term objects"""
        return [Term.get_obj(n) for n in node]

