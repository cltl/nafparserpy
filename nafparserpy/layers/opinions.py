from dataclasses import dataclass, field
from typing import List
from nafparserpy.layers.utils import AttributeGetter, create_node
from nafparserpy.layers.sublayers import Span


@dataclass
class OpinionObj(AttributeGetter):
    type: str
    span: List[Span]    # FIXME is this right? shouldn't there be a single span?
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node(self.type, None, self.span, self.attrs)

    @staticmethod
    def _get_obj(type, node):
        return OpinionObj(type, [Span.get_obj(n) for n in node], node.attrib)


@dataclass
class OpinionHolder(OpinionObj):
    @staticmethod
    def get_obj(node):
        return OpinionObj._get_obj('opinion_holder', node)


@dataclass
class OpinionTarget(OpinionObj):
    @staticmethod
    def get_obj(node):
        return OpinionObj._get_obj('opinion_target', node)


@dataclass
class OpinionExpression(OpinionObj):
    @staticmethod
    def get_obj(node):
        return OpinionObj._get_obj('opinion_expression', node)


@dataclass
class Opinion:
    id: str
    holders: List[OpinionHolder]
    targets: List[OpinionTarget]
    expressions: List[OpinionExpression]

    def node(self):
        return create_node('opinion', None, self.holders + self.targets + self.expressions, {})

    @staticmethod
    def get_obj(node):
        return Opinion(node.get('id'),
                       [OpinionHolder.get_obj(n) for n in node.findall('opinion_holder')],
                       [OpinionTarget.get_obj(n) for n in node.findall('opinion_target')],
                       [OpinionExpression.get_obj(n) for n in node.findall('opinion_expression')],
                       node.attrib)


@dataclass
class Opinions:
    items: List[Opinion]

    def node(self):
        return create_node('opinions', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Opinion.get_obj(n) for n in node]
