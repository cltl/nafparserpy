from dataclasses import dataclass
from typing import List, Union

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
    relType: Union[str, None] = None
    """optional attribute: 'relType' (causal relation type)"""

    def node(self):
        """Create etree node from object"""
        return create_node('clink',
                           attributes={'id': self.id, 'from': self.from_idref, 'to': self.to},
                           optional_attrs={'relType': self.relType})

    @staticmethod
    def object(node):
        """Create object from etree node"""
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
        """Create etree node from object"""
        return create_node('causalRelations', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `CLink` objects from etree node"""
        return [CLink.object(n) for n in node]
