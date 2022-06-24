from dataclasses import dataclass, field
from typing import List, Union

from nafparserpy.layers.utils import create_node, ExternalReferenceHolder, IdrefGetter
from nafparserpy.layers.elements import Span, ExternalReferences


@dataclass
class Role(IdrefGetter, ExternalReferenceHolder):
    """Represents a predicate argument"""
    id: str
    span: Span
    external_references: ExternalReferences = ExternalReferences([])
    """optional external references"""
    confidence: Union[str, None] = None
    """optional attribute"""
    status: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.external_references.items:
            children.append(self.external_references)
        return create_node('role', children=children,
                           attributes={'id': self.id},
                           optional_attrs={'confidence': self.confidence, 'status': self.status})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Role(node.get('id'),
                    Span.object(node.find('span')),
                    ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                    node.get('confidence'),
                    node.get('status'))


@dataclass
class Predicate(IdrefGetter, ExternalReferenceHolder):
    """Represents a predicate"""
    id: str
    span: Span
    external_references: ExternalReferences = ExternalReferences([])
    """optional external references"""
    roles: List[Role] = field(default_factory=list)
    """optional list of predicate arguments"""
    confidence: Union[str, None] = None
    """optional attribute"""
    status: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.external_references.items:
            children.append(self.external_references)
        if self.roles:
            children.extend(self.roles)
        return create_node('predicate',
                           children=children,
                           attributes={'id': self.id},
                           optional_attrs={'confidence': self.confidence, 'status': self.status})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Predicate(node.get('id'),
                         Span.object(node.find('span')),
                         ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                         [Role.object(n) for n in node.findall('role')],
                         node.get('confidence'),
                         node.get('status'))


@dataclass
class Srl:
    """SRL layer class"""
    items: List[Predicate]
    """list of predicates"""

    def node(self):
        """Create etree node from object"""
        return create_node('srl', children=self.items)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return [Predicate.object(n) for n in node]
