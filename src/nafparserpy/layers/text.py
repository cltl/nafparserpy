from dataclasses import dataclass, field
from typing import List, Union

from nafparserpy.layers.utils import create_node


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
class Wf:
    """Represents a word's surface form"""
    text: str
    id: str
    offset: str
    length: str
    subtokens: List[Subtoken] = field(default_factory=list)
    """optional list of subtokens"""
    sent: Union[str, None] = None
    """optional attribute"""
    para: Union[str, None] = None
    """optional attribute"""
    page: Union[str, None] = None
    """optional attribute"""
    xpath: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        return create_node('wf',
                           self.text,
                           self.subtokens,
                           {'id': self.id, 'offset': self.offset, 'length': self.length},
                           {'sent': self.sent, 'para': self.para, 'page': self.page, 'xpath': self.xpath})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Wf(node.text, node.get('id'), node.get('offset'), node.get('length'),
                  [Subtoken.object(n) for n in node],
                  node.get('sent'), node.get('para'), node.get('page'), node.get('xpath'))


@dataclass
class Text:
    """Text layer class"""
    items: List[Wf]
    """list of word forms"""

    def node(self):
        """Create etree node from object"""
        return create_node('text', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Wf` objects from etree node"""
        return [Wf.object(n) for n in node]
