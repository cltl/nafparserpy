from dataclasses import dataclass, field
from typing import List
from lxml import etree

from nafparserpy.layers.utils import AttributeLayer, AttributeGetter, create_node


@dataclass
class FileDesc(AttributeLayer):
    """Represents a fileDesc element"""
    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return AttributeLayer('fileDesc', node.attrib)


@dataclass
class Public(AttributeLayer):
    """Represents a public element"""
    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return AttributeLayer('public', node.attrib)


@dataclass
class LPDependency(AttributeGetter):
    """Represents a dependency (tool/model/data) of a linguistic processor"""
    name: str
    attrs: dict = field(default_factory=dict)
    """optional attributes ('version', 'type')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'name': self.name})

    def node(self):
        """Create etree node from object"""
        return create_node('lpDependency', None, [], self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return LPDependency(node.get('name'), node.attrib)


@dataclass
class LP(AttributeGetter):
    """Represents a linguistic processor"""
    name: str
    version: str
    lpDependencies: List[LPDependency]
    attrs: dict = field(default_factory=dict)
    """optional attributes ('timestamp', 'beginTimestamp', 'endTimestamp', 'hostname', 'id')"""

    def __post_init__(self):
        """Copy compulsory attributes to `attrs` field"""
        self.attrs.update({'name': self.name, 'version': self.version})

    def node(self):
        """Create etree node from object"""
        return create_node('lp', None, self.lpDependencies, self.attrs)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return LP(node.get('name'), node.get('version'), [LPDependency.object(n) for n in node], node.attrib)


@dataclass
class LinguisticProcessors:
    """Represents a linguisticProcessors element: the list of linguistic processors for a given layer."""
    layer_name: str
    lps: List[LP]
    """list of linguistic processors"""

    def node(self):
        """Create etree node from object"""
        return create_node('linguisticProcessors', None, self.lps, {'layer': self.layer_name})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return LinguisticProcessors(node.get('layer'), [LP.object(n) for n in node])


@dataclass
class NafHeader:
    fileDesc: AttributeLayer
    public: AttributeLayer
    linguisticProcessors: List[LinguisticProcessors] = field(default_factory=list)

    def node(self):
        """Create etree node from object"""
        node = etree.Element('nafHeader')
        if self.fileDesc.attrs:
            node.append(self.fileDesc.node())
        if self.public.attrs:
            node.append(self.public.node())
        if self.linguisticProcessors is not None:
            for linguisticProcessor in self.linguisticProcessors:
                node.append(linguisticProcessor.node())
        return node

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return NafHeader(FileDesc.object(node.find('fileDesc')),
                         Public.object(node.find('public')),
                         [LinguisticProcessors.object(n) for n in node.findall('linguisticProcessors')])

    @staticmethod
    def create(filedesc_attr, public_attr, linguistic_processors):
        return NafHeader(AttributeLayer('fileDesc', filedesc_attr),
                         AttributeLayer('public', public_attr),
                         linguistic_processors)
