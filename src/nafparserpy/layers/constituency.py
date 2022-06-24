from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.utils import create_node, IdrefGetter
from nafparserpy.layers.elements import Span


@dataclass
class Edge:
    """Represents an edge"""
    from_idref: str
    """id of 'from' node """
    to: str
    """id of 'to' node"""
    id: Union[str, None] = None
    """optional id"""
    head: Union[str, None] = None
    """optional head"""

    def node(self):
        """Create etree node from object"""
        return create_node('edge',
                           attributes={'from': self.from_idref, 'to': self.to},
                           optional_attrs={'id': self.id, 'head': self.head})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Edge(node.get('from'), node.get('to'), node.get('id'), node.get('head'))


@dataclass
class T(IdrefGetter):
    """Represents a terminal"""
    id: str
    span: Span

    def node(self):
        """Create etree node from object"""
        return create_node('t', children=[self.span], attributes={'id': self.id})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return T(node.get('id'), Span.object(node.find('span')))


@dataclass
class Nt:
    """Represents a nonterminal"""
    id: str
    label: str

    def node(self):
        """Create etree node from object"""
        return create_node('nt', attributes={'id': self.id, 'label': self.label})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Nt(node.get('id'), node.get('label'))


@dataclass
class Tree:
    """Represents a tree"""
    nts: List[Nt]
    """nonterminals"""
    ts: List[T]
    """terminals"""
    edges: List[Edge]
    """edges"""

    def node(self):
        """Create etree node from object"""
        return create_node('tree', children=self.nts + self.ts + self.edges)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Tree([Nt.object(n) for n in node.findall('nt')],
                    [T.object(n) for n in node.findall('t')],
                    [Edge.object(n) for n in node.findall('edge')])


@dataclass
class Constituency:
    """Constituency layer class"""
    items: List[Tree]
    """list of trees"""

    def node(self):
        """Create etree node from object"""
        return create_node('constituency', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Tree` objects from etree node"""
        return [Tree.object(n) for n in node]
