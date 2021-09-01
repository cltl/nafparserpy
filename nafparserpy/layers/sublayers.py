from dataclasses import dataclass, field
from typing import List, Any

from nafparserpy.layers.utils import AttributeGetter, AttributeLayer, IdrefGetter, create_node


@dataclass
class Target:
    """Defines target id for the Span class"""
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
    # optional attributes ('primary', 'status')

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
    """Represents a sentiment.

    Optional attributes are: 'resource', 'polarity', 'strength', 'subjectivity', 'sentiment_semantic_type',
    'sentiment_product_feature', 'sentiment_modifier', 'sentiment_marker'
    """
    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return AttributeLayer('sentiment', node.attrib)


@dataclass
class ExternalRef(AttributeGetter):
    """Represents an external reference"""
    reference: str
    sentiment: Sentiment = None
    externalRefs: List[Any] = field(default_factory=list)
    # list of ExternalRef objects (declared as Any because of circularity of definition)
    attrs: dict = field(default_factory=dict)
    # optional attributes ('resource', 'reftype', 'status', 'source', 'confidence', 'timestamp')

    def node(self):

        children = []
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.externalRefs:
            children.extend(self.externalRefs)
        attrib = {'reference': self.reference}
        attrib.update(self.attrs)
        return create_node('externalRef', None, children, attrib)

    @staticmethod
    def get_obj(node):
        # FIXME does lxml includes the node itself in 'findall' ?
        return ExternalRef(node.get('reference'),
                           Sentiment.get_obj(node.find('sentiment')),
                           [ExternalRef.get_obj(n) for n in node.findall('externalRef')],
                           node.attrib)


@dataclass
class ExternalReferences:
    """ExternalReferences container"""
    items: List[ExternalRef] = field(default_factory=list)
    # list of external references

    def node(self):
        return create_node('externalRefs', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """Returns the list of external references"""
        if node is None:
            return None
        return [ExternalRef.get_obj(n) for n in node]


@dataclass
class Component(AttributeGetter, IdrefGetter):
    """Represents a component"""
    id: str
    span: Span
    sentiment: Sentiment = None
    externalReferences: ExternalReferences = ExternalReferences([])
    attrs: dict = field(default_factory=dict)
    # optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'netype', 'case', 'head')

    def node(self):
        children = list()
        children.append(self.span)
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.externalReferences.items:
            children.append(self.externalReferences)
        all_attrs = {'id': self.id}
        all_attrs.update(self.attrs)
        create_node('component', None, children, all_attrs)

    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return Component(node.get('id'),
                         Span.get_obj(node.find('span')),
                         Sentiment.get_obj(node.find('sentiment')),
                         ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                         node.attrib)
<<<<<<< HEAD

=======
>>>>>>> wip
