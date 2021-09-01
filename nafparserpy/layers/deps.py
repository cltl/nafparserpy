from dataclasses import dataclass
from typing import List

from nafparserpy.layers.utils import create_node


@dataclass
class Dep:
    """Represents a Dependency"""
    from_idref: str
    # id of 'from' node
    to: str
    # id of 'to' node
    rfunc: str
    # dependency relation
    case: str = None
    # FIXME document this

    def node(self):
        attrs = {'from': self.from_idref, 'to': self.to, 'rfunc': self.rfunc}
        if self.case is not None:
            attrs.update({'case': self.case})
        return create_node('dep', None, [], attrs)

    @staticmethod
    def get_obj(node):
        return Dep(node.get('from'), node.get('to'), node.get('rfunc'), node.get('case'))


@dataclass
class Deps:
    """Deps (dependencies) layer class"""
    items: List[Dep]

    def node(self):
        return create_node('deps', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Dep.get_obj(n) for n in node]

