from dataclasses import dataclass
from typing import List

from nafparserpy.utils import create_node


@dataclass
class Dep:
    from_idref: str
    to_idref: str
    rfunc: str
    case: str = None

    def node(self):
        attrs = {'from': self.from_idref, 'to': self.to_idref, 'rfunc': self.rfunc}
        if self.case is not None:
            attrs.update({'case': self.case})
        return create_node('dep', None, [], attrs)

    @staticmethod
    def get_obj(node):
        return Dep(node.get('from'), node.get('to'), node.get('rfunc'), node.get('case'))


@dataclass
class Deps:
    items: List[Dep]

    def node(self):
        return create_node('deps', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Dep.get_obj(n) for n in node]

