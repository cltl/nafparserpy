from dataclasses import dataclass
from typing import List, Union
from nafparserpy.layers.utils import create_node, IdrefGetter
from nafparserpy.layers.elements import Span


@dataclass
class OpinionHolder(IdrefGetter):
    """Represents an opinion holder

    Optional attributes: 'type'"""
    span: Span
    type: Union[str, None] = ""
    """list of optional attributes (subclass dependent)"""

    def node(self):
        """Create etree node from object"""
        return create_node('opinion_holder', children=[self.span], optional_attrs={'type': self.type})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return OpinionHolder(Span.object(node.find('span')), node.get('type'))


@dataclass
class OpinionTarget(IdrefGetter):
    """Represents an opinion target

    Optional attributes: 'type'"""
    span: Span
    type: Union[str, None] = None
    """list of optional attributes (subclass dependent)"""

    def node(self):
        """Create etree node from object"""
        return create_node('opinion_target', children=[self.span], optional_attrs={'type': self.type})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return OpinionTarget(Span.object(node.find('span')), node.attrib)


@dataclass
class OpinionExpression(IdrefGetter):
    """Represents an opinion expression

    Optional attributes: 'polarity', 'strength', 'subjectivity', 'sentiment_semantic_type', 'sentiment_product_feature'
    """
    span: Span
    polarity: Union[str, None] = None
    """optional attribute"""
    strength: Union[str, None] = None
    """optional attribute"""
    subjectivity: Union[str, None] = None
    """optional attribute"""
    sentiment_semantic_type: Union[str, None] = None
    """optional attribute"""
    sentiment_product_feature: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        return create_node('opinion_expression',
                           children=[self.span],
                           optional_attrs={'polarity': self.polarity,
                                           'strength': self.strength,
                                           'subjectivity': self.subjectivity,
                                           'sentiment_semantic_type': self.sentiment_semantic_type,
                                           'sentiment_product_feature': self.sentiment_product_feature})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return OpinionExpression(Span.object(node.find('span')),
                                 node.get('polarity'),
                                 node.get('strength'),
                                 node.get('subjectivity'),
                                 node.get('sentiment_semantic_type'),
                                 node.get('sentiment_product_feature'))


@dataclass
class Opinion:
    """Represents an opinion"""
    id: str
    expression: OpinionExpression
    holder: Union[OpinionHolder, None] = None
    target: Union[OpinionTarget, None] = None

    def node(self):
        """Create etree node from object"""
        children = [self.expression]
        if self.holder is not None:
            children.append(self.holder)
        if self.target is not None:
            children.append(self.target)
        return create_node('opinion', children=children)

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
        return create_node('opinions', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Opinion` objects from etree node"""
        return [Opinion.object(n) for n in node]
