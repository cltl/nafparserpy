from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import create_node


@dataclass
class CLink:
    """Causal link class"""
    id: str
    from_idref: str
    to_idref: str
    rel_type: str = None

    def node(self):
        attrib = {'id': self.id,
                  'from': self.from_idref,
                  'to': self.to_idref}
        if self.rel_type is not None:
            attrib.update({'relType': self.rel_type})
        return create_node('clink', None, [], attrib)

    @staticmethod
    def get_obj(node):
        return CLink(node.get('id'),
                     node.get('from'),
                     node.get('to'),
                     node.get('relType'))


@dataclass
class CausalRelations:
    """CausalRelations layer class"""
    clinks: List[CLink] = field(default_factory=list)

    def node(self):
        return create_node('causalRelations', None, self.clinks, {})

    @staticmethod
    def get_obj(node):
        return CausalRelations([CLink.get_obj(n) for n in node])
