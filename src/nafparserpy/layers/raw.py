from dataclasses import dataclass

from nafparserpy.layers.utils import create_node


@dataclass
class Raw:
    """Raw layer class"""
    text: str
    """raw text"""

    def node(self):
        """Create etree node from object"""
        return create_node('raw', text=self.text)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Raw(node.text)
