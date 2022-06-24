from dataclasses import dataclass
from typing import List, Union

from nafparserpy.layers.utils import IdrefGetter, create_node, ExternalReferenceHolder
from nafparserpy.layers.elements import Span, ExternalReferences


@dataclass
class Entity(IdrefGetter, ExternalReferenceHolder):
    """Represents a named entity"""
    id: str
    """Entity id"""
    span: Span
    """Span of idrefs covered by the entity"""
    external_references: ExternalReferences = ExternalReferences([])
    """An optional list of external references"""
    type: Union[str, None] = None
    """optional type"""
    status: Union[str, None] = None
    """optional status"""
    source: Union[str, None] = None
    """optional source"""

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.external_references.items:
            children.append(self.external_references)
        return create_node('entity',
                           children=children,
                           attributes={'id': self.id},
                           optional_attrs={'type': self.type, 'status': self.status, 'source': self.source})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Entity(node.get('id'),
                      Span.object(node.find('span')),
                      ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                      node.get('type'),
                      node.get('status'),
                      node.get('source'))

    @staticmethod
    def create(entity_id, entity_type, target_ids):
        return Entity(entity_id, Span.create(target_ids), type=entity_type)


@dataclass
class Entities:
    """Entities layer class"""
    items: List[Entity]
    """list of entities in the layer"""

    def node(self):
        """Create etree node from object"""
        return create_node('entities', children=self.items)

    @staticmethod
    def object(node):
        """Create list of `Entity` objects from etree node"""
        return [Entity.object(n) for n in node]
