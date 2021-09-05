from dataclasses import dataclass
from typing import List
from nafparserpy.layers.utils import IdrefGetter, create_node
from nafparserpy.layers.elements import Span


@dataclass
class StatementObj(IdrefGetter):
    """Generic statement object class for statement sources, targets and cues"""
    type: str
    """type of the statement object"""
    span: Span
    """span covered by the statement"""

    def node(self):
        """Create etree node from object"""
        return create_node(self.type, None, [self.span], {})

    @staticmethod
    def object(type, node):
        """Create object from etree node"""
        return StatementObj(type, Span.object(node.find('span')))


@dataclass
class StatementSource(StatementObj):
    @staticmethod
    def object(node):
        """Create object from etree node"""
        return StatementObj.object('statement_source', node)


@dataclass
class StatementTarget(StatementObj):
    @staticmethod
    def object(node):
        """Create object from etree node"""
        return StatementObj.object('statement_target', node)


@dataclass
class StatementCue(StatementObj):
    @staticmethod
    def object(node):
        """Create object from etree node"""
        return StatementObj.object('statement_cue', node)


@dataclass
class Statement:
    """A statement has an id and one or more targets, sources or cues"""
    id: str
    targets: List[StatementObj]
    sources: List[StatementObj]
    cues: List[StatementObj]

    def node(self):
        """Create etree node from object"""
        return create_node('statement', None, self.sources + self.targets + self.cues, {})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Statement(node.get('id'),
                         [StatementTarget.object(n) for n in node.findall('statement_target')],
                         [StatementSource.object(n) for n in node.findall('statement_source')],
                         [StatementCue.object(n) for n in node.findall('statement_cue')])


@dataclass
class Attribution:
    """Attribution-layer class """
    items: List[Statement]
    """list of attribution statements"""

    def node(self):
        """Create etree node from object"""
        return create_node('attribution', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Statement` objects from etree node"""
        return [Statement.object(n) for n in node]
