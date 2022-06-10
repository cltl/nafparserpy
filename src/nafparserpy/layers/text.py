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
        """Create etree node from object"""
        return create_node('subtoken', self.text, [], {'id': self.id, 'offset': self.offset, 'length': self.length})

    @staticmethod
    def object(node):
        """Create object from etree node"""
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

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id, 'offset': self.offset, 'length': self.length})

    def node(self):
        """Create etree node from object"""
        return create_node('wf', self.text, self.subtokens, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Wf(node.text, node.get('id'), node.get('offset'), node.get('length'),
                  [Subtoken.object(n) for n in node],
                  node.attrib)


@dataclass
class Text:
    """Text layer class"""
    items: List[Wf]
    """list of word forms"""

    def node(self):
        """Create etree node from object"""
        return create_node('text', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Wf` objects from etree node"""
        return [Wf.object(n) for n in node]
