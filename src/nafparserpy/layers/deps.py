from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.utils import create_node


@dataclass
class Dep:
    """Represents a Dependency"""
    from_idref: str
    """id of 'from' node"""
    to: str
    """id of 'to' node"""
    rfunc: str
    """dependency relation"""
    case: Union[str, None] = None
    """optional attribute: 'case'"""

    def node(self):
        """Create etree node from object"""
        return create_node('dep',
                           attributes={'from': self.from_idref, 'to': self.to, 'rfunc': self.rfunc},
                           optional_attrs={'case': self.case})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Dep(node.get('from'), node.get('to'), node.get('rfunc'), node.get('case'))


@dataclass
class Deps:
    """Deps (dependencies) layer class"""
    items: List[Dep]
    """list of dependencies"""

    def node(self):
        """Create etree node from object"""
        return create_node('deps', children=self.items)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return [Dep.object(n) for n in node]
