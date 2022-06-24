from typing import Union

from nafparserpy.layers.utils import create_node


class Locations:
    text: Union[str, None] = None

    def node(self):
        """Create etree node from object"""
        return create_node('locations', text=self.text)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Locations(node.text)


class Dates:
    text: Union[str, None] = None

    def node(self):
        """Create etree node from object"""
        return create_node('dates', text=self.text)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Dates(node.text)
