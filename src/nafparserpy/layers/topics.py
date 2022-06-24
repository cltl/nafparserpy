from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.utils import create_node


@dataclass
class Topic:
    """Represents a topic"""
    text: str
    source: Union[str, None] = None
    method: Union[str, None] = None
    confidence: Union[str, None] = None
    uri: Union[str, None] = None

    def node(self):
        """Create etree node from object"""
        return create_node('topic', text=self.text, optional_attrs={'source': self.source, 'method': self.method,
                                                                    'confidence': self.confidence, 'uri': self.uri})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Topic(node.text, node.get('source'), node.get('method'), node.get('confidence'), node.get('uri'))


@dataclass
class Topics:
    """Topics layer class"""
    items: List[Topic]
    """list of topics"""

    def node(self):
        """Create etree node from object"""
        return create_node('topics', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Topic` objects from etree node"""
        return [Topic.object(n) for n in node]
