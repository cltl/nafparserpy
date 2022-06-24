from dataclasses import dataclass
from typing import List
from nafparserpy.layers.utils import create_node, IdrefGetter
from nafparserpy.layers.elements import Span


@dataclass
class StatementSource(IdrefGetter):
    """Represents the source of a statement"""
    span: Span
    """span covered by the statement source"""

    def node(self):
        """Create etree node from object"""
        return create_node('statement_source', children=[self.span])

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return StatementSource(Span.object(node.find('span')))

    @staticmethod
    def create(target_ids):
        return StatementSource(Span.create(target_ids))


@dataclass
class StatementTarget(IdrefGetter):
    span: Span
    """span covered by the statement target"""

    def node(self):
        """Create etree node from object"""
        return create_node('statement_target', children=[self.span])

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return StatementTarget(Span.object(node.find('span')))

    @staticmethod
    def create(target_ids):
        return StatementTarget(Span.create(target_ids))


@dataclass
class StatementCue(IdrefGetter):
    span: Span
    """span covered by the statement cue"""

    def node(self):
        """Create etree node from object"""
        return create_node('statement_cue', children=[self.span])

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return StatementCue(Span.object(node.find('span')))

    @staticmethod
    def create(target_ids):
        return StatementCue(Span.create(target_ids))


@dataclass
class Statement:
    """A statement has an id and one or more targets, sources or cues"""
    id: str
    targets: List[StatementTarget]
    sources: List[StatementSource]
    cues: List[StatementCue]

    def node(self):
        """Create etree node from object"""
        return create_node('statement', children=self.sources + self.targets + self.cues, attributes={'id': self.id})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Statement(node.get('id'),
                         [StatementTarget.object(n) for n in node.findall('statement_target')],
                         [StatementSource.object(n) for n in node.findall('statement_source')],
                         [StatementCue.object(n) for n in node.findall('statement_cue')])

    def target_spans(self):
        return [t.span.target_ids() for t in self.targets]

    def source_spans(self):
        return [t.span.target_ids() for t in self.sources]

    def cue_spans(self):
        return [t.span.target_ids() for t in self.cues]


@dataclass
class Attribution:
    """Attribution-layer class """
    items: List[Statement]
    """list of attribution statements"""

    def node(self):
        """Create etree node from object"""
        return create_node('attribution', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Statement` objects from etree node"""
        return [Statement.object(n) for n in node]
