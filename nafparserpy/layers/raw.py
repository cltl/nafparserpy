from dataclasses import dataclass

from nafparserpy.layers.utils import create_node


@dataclass
class Raw:
    """Raw layer class"""
    text: str
    """raw text"""

    def node(self):
        return create_node('raw', self.text, [], {})

    @staticmethod
    def get_obj(node):
        return Raw(node.text)
