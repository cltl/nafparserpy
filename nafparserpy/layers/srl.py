from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import AttributeGetter, create_node, ExternalReferenceHolder
from nafparserpy.layers.elements import Span, ExternalReferences


@dataclass
class Role(AttributeGetter, ExternalReferenceHolder):
    """Represents a predicate argument"""
    id: str
    span: Span
    external_references: ExternalReferences = ExternalReferences([])
    """optional external references"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('confidence' and 'status')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id})

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.external_references.items:
            children.append(self.external_references)
        return create_node('role', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Role(node.get('id'),
                    Span.object(node.find('span')),
                    ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                    node.attrib)


@dataclass
class Predicate(AttributeGetter, ExternalReferenceHolder):
    """Represents a predicate"""
    id: str
    span: Span
    external_references: ExternalReferences = ExternalReferences([])
    """optional external references"""
    roles: List[Role] = field(default_factory=list)
    """optional list of predicate arguments"""
    attrs: dict = field(default_factory=dict)
    """optional attributes ('confidence', 'status')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'id': self.id})

    def node(self):
        """Create etree node from object"""
        children = [self.span]
        if self.external_references.items:
            children.append(self.external_references)
        if self.roles:
            children.extend(self.roles)
        return create_node('predicate', None, children, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return Predicate(node.get('id'),
                         Span.object(node.find('span')),
                         ExternalReferences(ExternalReferences.object(node.find('externalReferences'))),
                         [Role.object(n) for n in node.findall('role')],
                         node.attrib)


@dataclass
class Srl:
    """SRL layer class"""
    items: List[Predicate]
    """list of predicates"""

    def node(self):
        """Create etree node from object"""
        return create_node('srl', None, self.items, {})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return [Predicate.object(n) for n in node]
