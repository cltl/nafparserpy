from dataclasses import dataclass
from typing import List
from nafparserpy.layers.utils import IdrefGetter, create_node
from nafparserpy.layers.sublayers import Span


@dataclass
class StatementObj(IdrefGetter):
    """Generic statement object class for statement sources, targets and cues"""
    type: str
    """type of the statement object"""
    span: Span
    """span covered by the statement"""

    def node(self):
        return create_node(self.type, None, [self.span], {})

    @staticmethod
    def get_obj(type, node):
        return StatementObj(type, Span.get_obj(node.find('span')))


@dataclass
class StatementSource(StatementObj):
    @staticmethod
    def get_obj(node):
        return StatementObj.get_obj('statement_source', node)


@dataclass
class StatementTarget(StatementObj):
    @staticmethod
    def get_obj(node):
        return StatementObj.get_obj('statement_target', node)


@dataclass
class StatementCue(StatementObj):
    @staticmethod
    def get_obj(node):
        return StatementObj.get_obj('statement_cue', node)


@dataclass
class Statement:
    """A statement has an id and one or more targets, sources or cues"""
    id: str
    targets: List[StatementObj]
    sources: List[StatementObj]
    cues: List[StatementObj]

    def node(self):
        return create_node('statement', None, self.sources + self.targets + self.cues, {})

    @staticmethod
    def get_obj(node):
        return Statement(node.get('id'),
                         [StatementTarget.get_obj(n) for n in node.findall('statement_target')],
                         [StatementSource.get_obj(n) for n in node.findall('statement_source')],
                         [StatementCue.get_obj(n) for n in node.findall('statement_cue')])


@dataclass
class Attribution:
    """Attribution-layer class """
    items: List[Statement]
    """list of attribution statements"""

    def node(self):
        return create_node('attribution', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Statement.get_obj(n) for n in node]
