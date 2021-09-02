from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import create_node


@dataclass
class CLink:
    """Represents a causal link"""
    id: str
    """causal link if"""
    from_idref: str
    """field for NAF attribute 'from' (note difference in name)"""
    to: str
    """field for NAF attribute 'to'"""
    relType: str = None
    """causal relation type (optional)"""

    def node(self):
        attrib = {'id': self.id,
                  'from': self.from_idref,
                  'to': self.to}
        if self.relType is not None:
            attrib.update({'relType': self.relType})
        return create_node('clink', None, [], attrib)

    @staticmethod
    def get_obj(node):
        return CLink(node.get('id'),
                     node.get('from'),
                     node.get('to'),
                     node.get('relType'))


@dataclass
class CausalRelations:
    """Causal Relations layer class"""
    items: List[CLink]
    """list of causal links"""

    def node(self):
        return create_node('causalRelations', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return CausalRelations([CLink.get_obj(n) for n in node])
