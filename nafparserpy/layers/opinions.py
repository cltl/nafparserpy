from dataclasses import dataclass, field
from typing import List
from nafparserpy.layers.utils import AttributeGetter, create_node, IdrefGetter
from nafparserpy.layers.elements import Span


@dataclass
class OpinionHolder(AttributeGetter, IdrefGetter):
    """Represents an opinion holder

    Optional attributes: 'type'"""
    span: Span
    attrs: dict = field(default_factory=dict)
    """list of optional attributes (subclass dependent)"""

    def node(self):
        """Create etree node from object"""
        return create_node('opinion_holder', None, self.span, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return OpinionHolder(Span.object(node.find('span')), node.attrib)


@dataclass
class OpinionTarget(AttributeGetter, IdrefGetter):
    """Represents an opinion target

    Optional attributes: 'type'"""
    span: Span
    attrs: dict = field(default_factory=dict)
    """list of optional attributes (subclass dependent)"""

    def node(self):
        """Create etree node from object"""
        return create_node('opinion_target', None, self.span, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return OpinionTarget(Span.object(node.find('span')), node.attrib)


@dataclass
class OpinionExpression(AttributeGetter, IdrefGetter):
    """Represents an opinion expression

    Optional attributes: 'polarity', 'strength', 'subjectivity', 'sentiment_semantic_type', 'sentiment_product_feature'
    """
    span: Span
    attrs: dict = field(default_factory=dict)
    """list of optional attributes (subclass dependent)"""

    def node(self):
        """Create etree node from object"""
        return create_node('opinion_expression', None, [self.span], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return OpinionExpression(Span.object(node.find('span')), node.attrib)


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
        return Opinion(node.get('id'),
                       OpinionExpression.object(node.find('opinion_expression')),
                       OpinionHolder.object(node.find('opinion_holder')),
                       OpinionTarget.object(node.find('opinion_target')))


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
