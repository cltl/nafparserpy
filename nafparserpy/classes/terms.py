from dataclasses import dataclass, field
from typing import List, Any

from nafparserpy.utils import AttributeLayer, create_node, AttributeGetter, IdrefGetter
from nafparserpy.classes.span import Span


@dataclass
class Sentiment(AttributeLayer):
    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return AttributeLayer('sentiment', node.attrib)


@dataclass
class ExternalRef(AttributeGetter):
    sentiment: Sentiment = None
    externalRefs: List[Any] = field(default_factory=list)
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node('externalRef', None, self.sentiment + self.externalRefs, self.attrs)

    @staticmethod
    def get_obj(node):
        # FIXME does lxml includes the node itself in 'findall' ?
        return ExternalRef(Sentiment.get_obj(node.find('sentiment')),
                           [ExternalRef.get_obj(n) for n in node.findall('externalRef')],
                           node.attrib)


@dataclass
class ExternalReferences:
    items: List[ExternalRef] = field(default_factory=list)

    def node(self):
        return create_node('externalRefs', None, self.items, {})

    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return [ExternalRef.get_obj(n) for n in node]


@dataclass
class Component(AttributeGetter, IdrefGetter):
    id: str
    sentiment: Sentiment = None
    span: Span = None
    externalReferences: ExternalReferences = None
    attrs: dict = field(default_factory=dict)

    def node(self):
        children = []
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.span is not None:
            children.append(self.span)
        if self.externalReferences is not None:
            children.append(self.externalReferences)
        all_attrs = {'id': self.id}
        all_attrs.update(self.attrs)
        create_node('component', None, children, all_attrs)

    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return Component(node.get('id'),
                         Sentiment.get_obj(node.find('sentiment')),
                         Span.get_obj(node.find('span')),
                         ExternalReferences.get_obj(node.find('externalReferences')),
                         node.attrib)


@dataclass
class Term(AttributeGetter, IdrefGetter):
    id: str
    sentiment: Sentiment = None
    span: Span = None
    externalReferences: ExternalReferences = None
    component: Component = None
    attrs: dict = field(default_factory=dict)

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
                    ExternalReferences.get_obj(node.find('externalReferences')),
                    Component.get_obj(node.find('component')),
                    node.attrib)

    @staticmethod
    def create(term_id, term_attrs, target_ids):
        """creates a basic term with id, attributes and target ids"""
        return Term(term_id, span=Span.create(target_ids), attrs=term_attrs)


@dataclass
class Terms:
    items: List[Term]

    def node(self):
        return create_node('terms', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """retrieves list of Term objects"""
        return [Term.get_obj(n) for n in node]

