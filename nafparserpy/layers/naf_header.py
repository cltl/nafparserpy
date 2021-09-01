from dataclasses import dataclass, field
from typing import List
from lxml import etree

from nafparserpy.layers.utils import AttributeLayer, AttributeGetter, create_node


@dataclass
class FileDesc(AttributeLayer):
    """Represents a fileDesc element"""
    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return AttributeLayer('fileDesc', node.attrib)


@dataclass
class Public(AttributeLayer):
    """Represents a public element"""
    @staticmethod
    def get_obj(node):
        if node is None:
            return None
        return AttributeLayer('public', node.attrib)


@dataclass
class LP(AttributeGetter):
    """Represents a linguistic processor"""
    name: str
    version: str
    attrs: dict = field(default_factory=dict)
    # optional attributes ('timestamp', 'beginTimestamp', 'endTimestamp', 'hostname')

    def node(self):
        all_attrs = {'name': self.name, 'version': self.version}
        all_attrs.update(self.attrs)
        return create_node('lp', None, [], all_attrs)

    @staticmethod
    def get_obj(node):
        return LP(node.get('name'), node.get('version'), node.attrib)


@dataclass
class LinguisticProcessors:
    """Represents a linguisticProcessors element: the list of linguistic processors for a given layer."""
    layer_name: str
    items: List[LP]
    # list of linguistic processors

    def node(self):
        return create_node('linguisticProcessors', None, self.items, {'layer': self.layer_name})

    @staticmethod
    def get_obj(node):
        return LinguisticProcessors(node.get('layer'), [LP.get_obj(n) for n in node])


@dataclass
class NafHeader:
    fileDesc: AttributeLayer
    public: AttributeLayer
    linguisticProcessors: List[LinguisticProcessors] = field(default_factory=list)

    def node(self):
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
    def get_obj(node):
        return NafHeader(FileDesc.get_obj(node.find('fileDesc')),
                         Public.get_obj(node.find('public')),
                         [LinguisticProcessors.get_obj(n) for n in node.findall('linguisticProcessors')])

    @staticmethod
    def create(filedesc_attr, public_attr, linguistic_processors):
        return NafHeader(AttributeLayer('fileDesc', filedesc_attr), AttributeLayer('public', public_attr), linguistic_processors)


