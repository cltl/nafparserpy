from dataclasses import dataclass, field
from typing import List, Any, Union

from nafparserpy.layers.utils import IdrefGetter, create_node, ExternalReferenceHolder


@dataclass
class Target:
    """Defines target id for the Span class"""
    id: str
    head: Union[str, None] = None
    """optional attribute: 'head'"""

    def node(self):
        """Create etree node from object"""
        return create_node('target', attributes={'id': self.id}, optional_attrs={'head': self.head})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Target(node.get('id'), node.get('head'))


@dataclass
class Span:
    targets: List[Target]
    primary: Union[str, None] = None
    """optional attribute 'primary'"""
    status: Union[str, None] = None
    """optional attribute 'status'"""

    def node(self):
        """Create etree node from object"""
        return create_node('span', children=self.targets,
                           optional_attrs={'primary': self.primary, 'status': self.status})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return Span([Target.object(n) for n in node.findall('target')], node.get('primary'), node.get('status'))

    @staticmethod
    def create(target_ids):
        return Span([Target(i) for i in target_ids])

    def target_ids(self):
        return [t.id for t in self.targets]


@dataclass
class Sentiment:
    """Represents a sentiment.

    Optional attributes are: 'resource', 'polarity', 'strength', 'subjectivity', 'sentiment_semantic_type',
    'sentiment_product_feature', 'sentiment_modifier', 'sentiment_marker'
    """
    resource: Union[str, None] = None
    polarity: Union[str, None] = None
    strength: Union[str, None] = None
    subjectivity: Union[str, None] = None
    sentiment_semantic_type: Union[str, None] = None
    sentiment_product_feature: Union[str, None] = None
    sentiment_modifier: Union[str, None] = None
    sentiment_marker: Union[str, None] = None

    def node(self):
        return create_node('sentiment', optional_attrs={'resource': self.resource,
                                                        'polarity': self.polarity,
                                                        'strength': self.strength,
                                                        'subjectivity': self.subjectivity,
                                                        'sentiment_semantic_type': self.sentiment_semantic_type,
                                                        'sentiment_product_feature': self.sentiment_product_feature,
                                                        'sentiment_modifier': self.sentiment_modifier,
                                                        'sentiment_marker': self.sentiment_marker})

    @staticmethod
    def object(node):
        """Create object from etree node

        Parameters
        ----------
        node : etree
            node may be None as `sentiment` elements are optional subelements"""
        if node is None:
            return None
        return Sentiment(node.get('resource'),
                         node.get('polarity'),
                         node.get('strength'),
                         node.get('subjectivity'),
                         node.get('sentiment_semantic_type'),
                         node.get('sentiment_product_feature'),
                         node.get('sentiment_modifier'),
                         node.get('sentiment_marker'))


@dataclass
class ExternalRef:
    """Represents an external reference"""
    reference: str
    sentiment: Union[Sentiment, None] = None
    externalRefs: List[Any] = field(default_factory=list)
    """list of ExternalRef objects (declared as Any because of circularity of definition)"""
    resource: Union[str, None] = None
    """optional attribute"""
    reftype: Union[str, None] = None
    """optional attribute"""
    status: Union[str, None] = None
    """optional attribute"""
    source: Union[str, None] = None
    """optional attribute"""
    confidence: Union[str, None] = None
    """optional attribute"""
    timestamp: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        children = []
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.externalRefs:
            children.extend(self.externalRefs)
        return create_node('externalRef',
                           children=children,
                           attributes={'reference': self.reference},
                           optional_attrs={'resource': self.resource,
                                           'reftype': self.reftype,
                                           'status': self.status,
                                           'source': self.source,
                                           'confidence': self.confidence,
                                           'timestamp': self.timestamp})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return ExternalRef(node.get('reference'),
                           Sentiment.object(node.find('sentiment')),
                           [ExternalRef.object(n) for n in node.findall('externalRef')],
                           node.get('resource'),
                           node.get('reftype'),
                           node.get('status'),
                           node.get('source'),
                           node.get('confidence'),
                           node.get('timestamp')
                           )


@dataclass
class ExternalReferences:
    """ExternalReferences container"""
    items: List[ExternalRef] = field(default_factory=list)
    """optional list of external references"""

    def node(self):
        """Create etree node from object"""
        return create_node('externalReferences', children=self.items)

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
class Component(IdrefGetter, ExternalReferenceHolder):
    """Represents a component"""
    id: str
    span: Span
    sentiment: Union[Sentiment, None] = None
    external_references: ExternalReferences = ExternalReferences([])
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

    def node(self):
        """Create etree node from object"""
        children = list()
        children.append(self.span)
        if self.sentiment is not None:
            children.append(self.sentiment)
        if self.external_references.items:
            children.append(self.external_references)
        create_node('component',
                    children=children,
                    attributes={'id': self.id},
                    optional_attrs={
                        'type': self.type,
                        'lemma': self.lemma,
                        'pos': self.pos,
                        'morphofeat': self.morphofeat,
                        'netype': self.netype,
                        'case': self.case,
                        'head': self.head
                    })

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Component(node.get('id'),
                         Span.object(node.find('span')),
                         Sentiment.object(node.find('sentiment')),
                         ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                         node.get('type'),
                         node.get('lemma'),
                         node.get('pos'),
                         node.get('morphofeat'),
                         node.get('netype'),
                         node.get('case'),
                         node.get('head'))
