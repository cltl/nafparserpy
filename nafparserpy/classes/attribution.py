from dataclasses import dataclass
from typing import List
from nafparserpy.utils import create_node, IdrefGetter
from nafparserpy.classes.span import Span


@dataclass
class StatementObj(IdrefGetter):
    type: str
    span: Span

    def node(self):
        return create_node(self.type, None, [self.span], {})

    @staticmethod
    def _get_obj(type, node):
        return StatementObj(type, Span.get_obj(node.find('span')))


@dataclass
class StatementSource(StatementObj):
    @staticmethod
    def get_obj(node):
        return StatementObj._get_obj('statement_source', node)


@dataclass
class StatementTarget(StatementObj):
    @staticmethod
    def get_obj(node):
        return StatementObj._get_obj('statement_target', node)


@dataclass
class StatementCue(StatementObj):
    @staticmethod
    def get_obj(node):
        return StatementObj._get_obj('statement_cue', node)


@dataclass
class Statement:
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
    items: List[Statement]

    def node(self):
        return create_node('attribution', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Statement.get_obj(n) for n in node]
