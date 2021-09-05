from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node
from nafparserpy.layers.elements import Span, ExternalReferences


@dataclass
class Entity(AttributeGetter, IdrefGetter):
    """Represents a named entity"""
    id: str
    """Entity id"""
    span: Span
    """Span of idrefs covered by the entity"""
    external_references: ExternalReferences = field(default_factory=ExternalReferences([]))
    """An optional list of external references"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('type', 'status', 'source')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id})

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.external_references.items:
            children.append(self.external_references)
        return create_node('entity', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Entity(node.get('id'),
                      Span.object(node.find('span')),
                      ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                      node.attrib)

    @staticmethod
    def create(entity_id, entity_type, target_ids):
        return Entity(entity_id, Span.create(target_ids), ExternalReferences([]), {'type': entity_type})


@dataclass
class Entities:
    """Entities layer class"""
    items: List[Entity]
    """list of entities in the layer"""

    def node(self):
        """Create etree node from object"""
        return create_node('entities', None, self.items, {})

    @staticmethod
    def object(node):
        """Create list of `Entity` objects from etree node"""
        return [Entity.object(n) for n in node]
