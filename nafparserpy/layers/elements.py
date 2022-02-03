from dataclasses import dataclass, field
from typing import List, Any

from nafparserpy.layers.utils import AttributeGetter, AttributeLayer, IdrefGetter, create_node, ExternalReferenceHolder


@dataclass
class Target:
    """Defines target id for the Span class"""
    id: str
    attrs: dict = field(default_factory=dict)
    """optional attributes: 'head'"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id})

    def node(self):
        """Create etree node from object"""
        return create_node('target', None, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Target(node.get('id'), node.attrib)


@dataclass
class Span:
    targets: List[Target]
    attrs: dict = field(default_factory=dict)
    """optional attributes ('primary', 'status')"""

    def node(self):
        """Create etree node from object"""
        return create_node('span', None, self.targets, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return Span([Target.object(n) for n in node], node.attrib)

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
    def object(node):
        """Create object from etree node

        Parameters
        ----------
        node : etree
            node may be None as `sentiment` elements are optional subelements"""
        if node is None:
            return None
        return AttributeLayer('sentiment', node.attrib)


@dataclass
class ExternalRef(AttributeGetter):
    """Represents an external reference"""
    reference: str
    sentiment: Sentiment = None
    externalRefs: List[Any] = field(default_factory=list)
    """list of ExternalRef objects (declared as Any because of circularity of definition)"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('resource', 'reftype', 'status', 'source', 'confidence', 'timestamp')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'reference': self.reference})

    def node(self):
        """Create etree node from object"""
        children = []
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.externalRefs:
            children.extend(self.externalRefs)
        return create_node('externalRef', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return ExternalRef(node.get('reference'),
                           Sentiment.object(node.find('sentiment')),
                           [ExternalRef.object(n) for n in node.findall('externalRef')],
                           node.attrib)


@dataclass
class ExternalReferences:
    """ExternalReferences container"""
    items: List[ExternalRef] = field(default_factory=list)
    """optional list of external references"""

    def node(self):
        """Create etree node from object"""
        return create_node('externalReferences', None, self.items, {})

    @staticmethod
    def object(node):
        """Creates list of `ExternalRef` objects from node

        Parameters
        ----------
        node : etree
            node may be None as `ExternalReferences` elements are optional subelements"""
        if node is None:
            return []
        return [ExternalRef.object(n) for n in node]


@dataclass
class Component(AttributeGetter, IdrefGetter, ExternalReferenceHolder):
    """Represents a component"""
    id: str
    span: Span
    sentiment: Sentiment = None
    external_references: ExternalReferences = ExternalReferences([])
    attrs: dict = field(default_factory=dict)
    """optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'netype', 'case', 'head')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id})

    def node(self):
        """Create etree node from object"""
        children = list()
        children.append(self.span)
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.external_references.items:
            children.append(self.external_references)
        create_node('component', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Component(node.get('id'),
                         Span.object(node.find('span')),
                         Sentiment.object(node.find('sentiment')),
                         ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                         node.attrib)
