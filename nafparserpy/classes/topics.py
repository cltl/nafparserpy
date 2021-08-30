from dataclasses import dataclass, field
from typing import List
from lxml import etree

from nafparserpy.utils import create_node, AttributeGetter


@dataclass
class Topic(AttributeGetter):
    text: str
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node('topic', self.text, [], self.attrs)

    @staticmethod
    def get_obj(node):
        return Topic(node.text, node.attrib)


@dataclass
class Topics:
    items: List[Topic]

    def node(self):
        return create_node('topics', None, self.items, {})

    @staticmethod
    def get_obj(node):
        """retrieves list of Topic objects in Topic layer"""
        return [Topic.get_obj(n) for n in node]

