from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node


@dataclass
class Topic(AttributeGetter):
    """Represents a topic"""
    text: str
    attrs: dict = field(default_factory=dict)
    # optional attributes ('source', 'method', 'confidence', 'uri')

    def node(self):
        return create_node('topic', self.text, [], self.attrs)

    @staticmethod
    def get_obj(node):
        return Topic(node.text, node.attrib)


@dataclass
class Topics:
    """Topics layer class"""
    items: List[Topic]
    # list of topics

    def node(self):
        return create_node('topics', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """returns list of topics"""
        return [Topic.get_obj(n) for n in node]

