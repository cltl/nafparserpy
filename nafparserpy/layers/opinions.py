from dataclasses import dataclass, field
from typing import List
from nafparserpy.layers.utils import AttributeGetter, create_node
from nafparserpy.layers.elements import Span


@dataclass
class OpinionObj(AttributeGetter):
    """Generic representation of opinion object (holder, target or expression)"""
    type: str
    span: Span
    attrs: dict = field(default_factory=dict)
    """list of optional attributes (subclass dependent)"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'type': self.type})

    def node(self):
        """Create etree node from object"""
        return create_node(self.type, None, self.span, self.attrs)

    @staticmethod
    def object(type, node):
        """Create object of type `opinion_holder`/`opinion_target`/`opinion_expression` from etree node"""
        return OpinionObj(type, Span.object(node.find('span')), node.attrib)


@dataclass
class OpinionHolder(OpinionObj):
    """Represents an opinion holder

    Optional attributes: 'type'"""
    @staticmethod
    def object(node):
        """Create object from etree node"""
        return OpinionObj.object('opinion_holder', node)


@dataclass
class OpinionTarget(OpinionObj):
    """Represents an opinion target

    Optional attributes: 'type'"""
    @staticmethod
    def object(node):
        """Create object from etree node"""
        return OpinionObj.object('opinion_target', node)


@dataclass
class OpinionExpression(OpinionObj):
    """Represents an opinion expression

    Optional attributes: 'polarity', 'strength', 'subjectivity', 'sentiment_semantic_type', 'sentiment_product_feature'
    """
    @staticmethod
    def object(node):
        """Create object from etree node"""
        return OpinionObj.object('opinion_expression', node)


@dataclass
class Opinion:
    """Represents an opinion"""
    id: str
    expression: OpinionExpression
    holder: OpinionHolder = None
    target: OpinionTarget = None

    def node(self):
        """Create etree node from object"""
        children = [self.expression]
        if self.holder is not None:
            children.append(self.holder)
        if self.target is not None:
            children.append(self.target)
        return create_node('opinion', None, children, {})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        # TODO test me
        return Opinion(node.get('id'),
                       OpinionHolder.object(node.find('opinion_holder')),
                       OpinionTarget.object(node.find('opinion_target')),
                       OpinionExpression.object(node.find('opinion_expression')),
                       node.attrib)


@dataclass
class Opinions:
    """Opinions layer class"""
    items: List[Opinion]
    """list of opinions"""

    def node(self):
        """Create etree node from object"""
        return create_node('opinions', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Opinion` objects from etree node"""
        return [Opinion.object(n) for n in node]
