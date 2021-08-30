from dataclasses import dataclass, field
from typing import List

from nafparserpy.utils import create_node


@dataclass
class Target:
    id: str
    head: str = None

    def node(self):
        attrs = {'id': self.id}
        if self.head is not None:
            attrs.update({'head': self.head})
        return create_node('target', None, [], attrs)

    @staticmethod
    def get_obj(node):
        return Target(node.get('id'), node.get('head'))


@dataclass
class Span:
    targets: List[Target]
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node('span', None, self.targets, self.attrs)

    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return Span([Target.get_obj(n) for n in node], node.attrib)

    @staticmethod
    def create(target_ids):
        return Span(Target(i) for i in target_ids)

    def target_ids(self):
        return [t.id for t in self.targets]
