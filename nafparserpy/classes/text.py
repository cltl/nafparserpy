from dataclasses import dataclass, field
from typing import List

from nafparserpy.utils import create_node, AttributeGetter


@dataclass
class Subtoken:
    text: str
    id: str
    offset: str
    length: str

    def node(self):
        return create_node('subtoken', self.text, [], {'id': self.id, 'offset': self.offset, 'length': self.length})

    @staticmethod
    def get_obj(node):
        return Subtoken(node.text, node.get('id'), node.get('offset'), node.get('length'))


@dataclass
class Wf(AttributeGetter):
    text: str
    id: str
    offset: str
    length: str
    attrs: dict = field(default_factory=dict)
    subtokens: List[Subtoken] = field(default_factory=list)

    def node(self):
        all_attrs = {'id': self.id, 'offset': self.offset, 'length': self.length}
        all_attrs.update(self.attrs)
        return create_node('wf', self.text, [], all_attrs)

    @staticmethod
    def get_obj(node):
        return Wf(node.text, node.get('id'), node.get('offset'), node.get('length'), node.attrib)


@dataclass
class Text:
    items: List[Wf]

    def node(self):
        return create_node('text', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """directly retrieves list of Wf objects in Text layer"""
        return [Wf.get_obj(n) for n in node]
