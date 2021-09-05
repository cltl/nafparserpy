from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import create_node, AttributeGetter


@dataclass
class CLink(AttributeGetter):
    """Represents a causal link"""
    id: str
    """causal link if"""
    from_idref: str
    """field for NAF attribute 'from' (note difference in name)"""
    to: str
    """field for NAF attribute 'to'"""
    attrs: dict = field(default_factory=dict)
    """optional attributes: 'relType' (causal relation type)"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id, 'from': self.from_idref, 'to': self.to})

    def node(self):
        """Create etree node from object"""
        return create_node('clink', None, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return CLink(node.get('id'),
                     node.get('from'),
                     node.get('to'),
                     node.attrib)


@dataclass
class CausalRelations:
    """Causal Relations layer class"""
    items: List[CLink]
    """list of causal links"""

    def node(self):
        """Create etree node from object"""
        return create_node('causalRelations', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `CLink` objects from etree node"""
        return [CLink.object(n) for n in node]
