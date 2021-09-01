from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node


@dataclass
class Subtoken:
    """Represents a subtoken"""
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
    """Represents a word's surface form"""
    text: str
    id: str
    offset: str
    length: str
    subtokens: List[Subtoken] = field(default_factory=list)
    """optional list of subtokens"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('sent', 'para', 'page', 'xpath')"""

    def node(self):
        all_attrs = {'id': self.id, 'offset': self.offset, 'length': self.length}
        all_attrs.update(self.attrs)
        return create_node('wf', self.text, self.subtokens, all_attrs)

    @staticmethod
    def get_obj(node):
        return Wf(node.text, node.get('id'), node.get('offset'), node.get('length'),
                  [Subtoken.get_obj(n) for n in node],
                  node.attrib)


@dataclass
class Text:
    """Text layer class"""
    items: List[Wf]
    """list of word forms"""

    def node(self):
        return create_node('text', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """returns list of Wf objects in Text layer"""
        return [Wf.get_obj(n) for n in node]
