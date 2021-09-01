from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, IdrefGetter, create_node
from nafparserpy.layers.sublayers import Span, ExternalReferences


@dataclass
class Entity(AttributeGetter, IdrefGetter):
    """Represents a named entity"""
    id: str
    span: Span
    external_references: ExternalReferences = ExternalReferences([])
    attrs: dict = field(default_factory=dict)
    # optional attributes ('type', 'status', 'source')

    def node(self):
        attrib = {'id': self.id}
        attrib.update(self.attrs)
        return create_node('entity', None, [self.span] + [self.external_references], attrib)

    @staticmethod
    def get_obj(node):
        return Entity(node.get('id'),
                      Span.get_obj(node.find('span')),
                      ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                      node.attrib)

    @staticmethod
    def create(entity_id, entity_type, target_ids):
        return Entity(entity_id, Span.create(target_ids), [], {'type': entity_type})


@dataclass
class Entities:
    """Entities layer class"""
    items: List[Entity]

    def node(self):
        return create_node('entities', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Entity.get_obj(n) for n in node]
