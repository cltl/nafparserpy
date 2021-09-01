from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import create_node
from nafparserpy.layers.sublayers import Span


@dataclass
class Edge:
    """Represents an edge"""
    from_idref: str
    # id of 'from' node (note that the field name differs from the NAF attribute 'from')
    to: str
    # id of 'to' node
    attrs: dict = field(default_factory=dict)
    # optional attributes ('id' and 'head')

    def node(self):
        attrib = {'from': self.from_idref, 'to': self.to}
        attrib.update(self.attrs)
        return create_node('edge', None, [], attrib)

    @staticmethod
    def get_obj(node):
        return Edge(node.get('from'), node.get('to'), node.get('id'), node.get('head'))


@dataclass
class T:
    """Represents a terminal"""
    id: str
    span: Span

    def node(self):
        return create_node('t', None, [self.span], {'id': self.id})

    @staticmethod
    def get_obj(node):
        return T(node.get('id'), Span.get_obj(node.find('span')))


@dataclass
class Nt:
    """Represents a nonterminal"""
    id: str
    label: str

    def node(self):
        return create_node('nt', None, [], {'id': self.id, 'label': self.label})

    @staticmethod
    def get_obj(node):
        return Nt(node.get('id'), node.get('label'))


@dataclass
class Tree:
    """Represents a tree"""
    nts: List[Nt]
    # nonterminals
    ts: List[T]
    # terminals
    edges: List[Edge]
    # edges

    def node(self):
        return create_node('tree', None, self.nts + self.ts + self.edges, {})

    @staticmethod
    def get_obj(node):
        return Tree([Nt.get_obj(n) for n in node.findall('nt')],
                    [T.get_obj(n) for n in node.findall('t')],
                    [Edge.get_obj(n) for n in node.findall('edge')])


@dataclass
class Constituency:
    """Constituency layer class"""
    items: List[Tree]

    def node(self):
        return create_node('constituency', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Tree.get_obj(n) for n in node]
