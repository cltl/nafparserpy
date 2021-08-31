from dataclasses import dataclass
from typing import List

from nafparserpy.layers.utils import create_node
from nafparserpy.layers.sublayers import Span


@dataclass
class Edge:
    from_idref: str
    to_idref: str
    id: str
    head: str = None

    def node(self):
        attrs = {'from': self.from_idref, 'to': self.to_idref, 'id': self.id}
        if self.head is not None:
            attrs.update({'head': self.head})
        return create_node('edge', None, [], attrs)

    @staticmethod
    def get_obj(node):
        return Edge(node.get('from'), node.get('to'), node.get('id'), node.get('head'))


@dataclass
class T:
    span: Span
    id: str

    def node(self):
        return create_node('t', None, [self.span], {'id': self.id})

    @staticmethod
    def get_obj(node):
        return T(Span.get_obj(node.find('span')), node.get('id'))


@dataclass
class Nt:
    id: str
    label: str

    def node(self):
        return create_node('nt', None, [], {'id': self.id, 'label': self.label})

    @staticmethod
    def get_obj(node):
        return Nt(node.get('id'), node.get('label'))


@dataclass
class Tree:
    nts: List[Nt]
    ts: List[T]
    edges: List[Edge]

    def node(self):
        return create_node('tree', None, self.nts + self.ts + self.edges, {})

    @staticmethod
    def get_obj(node):
        return Tree([Nt.get_obj(n) for n in node.findall('nt')],
                    [T.get_obj(n) for n in node.findall('t')],
                    [Edge.get_obj(n) for n in node.findall('edge')])


@dataclass
class Constituency:
    items: List[Tree]

    def node(self):
        return create_node('constituency', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Tree.get_obj(n) for n in node]
