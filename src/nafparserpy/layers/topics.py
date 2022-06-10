from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node


@dataclass
class Topic(AttributeGetter):
    """Represents a topic"""
    text: str
    attrs: dict = field(default_factory=dict)
    """optional attributes ('source', 'method', 'confidence', 'uri')"""

    def node(self):
        """Create etree node from object"""
        return create_node('topic', self.text, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Topic(node.text, node.attrib)


@dataclass
class Topics:
    """Topics layer class"""
    items: List[Topic]
    """list of topics"""

    def node(self):
        """Create etree node from object"""
        return create_node('topics', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Topic` objects from etree node"""
        return [Topic.object(n) for n in node]
