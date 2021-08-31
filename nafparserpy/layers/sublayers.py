from dataclasses import dataclass, field
from typing import List, Any

from nafparserpy.layers.utils import AttributeGetter, AttributeLayer, IdrefGetter, create_node


@dataclass
class Target:
    id: str
    head: str = None

    def node(self):
        attrs = {'id': self.id}
        if self.head is not None:
            attrs.update({'head': self.head})
        return create_node('target', None, [], attrs)

    @staticmethod
    def get_obj(node):
        return Target(node.get('id'), node.get('head'))


@dataclass
class Span:
    targets: List[Target]
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node('span', None, self.targets, self.attrs)

    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return Span([Target.get_obj(n) for n in node], node.attrib)

    @staticmethod
    def create(target_ids):
        return Span([Target(i) for i in target_ids])

    def target_ids(self):
        return [t.id for t in self.targets]


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
                         ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                         node.attrib)

