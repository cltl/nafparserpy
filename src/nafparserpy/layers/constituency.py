from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import create_node, AttributeGetter, IdrefGetter
from nafparserpy.layers.elements import Span


@dataclass
class Edge(AttributeGetter):
    """Represents an edge"""
    from_idref: str
    """id of 'from' node (note that the field name differs from the NAF attribute 'from')"""
    to: str
    """id of 'to' node"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('id' and 'head')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'from': self.from_idref, 'to': self.to})

    def node(self):
        """Create etree node from object"""
        return create_node('edge', None, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Edge(node.get('from'), node.get('to'), node.attrib)


@dataclass
class T(IdrefGetter):
    """Represents a terminal"""
    id: str
    span: Span

    def node(self):
        """Create etree node from object"""
        return create_node('t', None, [self.span], {'id': self.id})

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
        return create_node('nt', None, [], {'id': self.id, 'label': self.label})

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
        return create_node('tree', None, self.nts + self.ts + self.edges, {})

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
        return create_node('constituency', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Tree` objects from etree node"""
        return [Tree.object(n) for n in node]
