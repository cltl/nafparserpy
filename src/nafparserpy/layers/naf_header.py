from dataclasses import dataclass, field
from typing import List, Union

from nafparserpy.layers.utils import create_node


@dataclass
class FileDesc:
    """Represents a fileDesc element"""
    title: Union[str, None] = None
    author: Union[str, None] = None
    creationtime: Union[str, None] = None
    filename: Union[str, None] = None
    filetype: Union[str, None] = None
    pages: Union[str, None] = None

    def node(self):
        """Create etree node from object"""
        return create_node('fileDesc', optional_attrs={'title': self.title,
                                                       'author': self.author,
                                                       'creationtime': self.creationtime,
                                                       'filename': self.filename,
                                                       'filetype': self.filetype,
                                                       'pages': self.pages})

    def has_attrs(self):
        return any([x is not None for x in
                    [self.title, self.author, self.creationtime, self.filename, self.filetype, self.pages]])

    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return FileDesc(node.get('title'),
                        node.get('author'),
                        node.get('creationtime'),
                        node.get('filename'),
                        node.get('filetype'),
                        node.get('pages'))


@dataclass
class Public:
    """Represents a public element"""
    publicId: Union[str, None] = None
    uri: Union[str, None] = None

    def node(self):
        """Create etree node from object"""
        return create_node('public', optional_attrs={'publicId': self.publicId,
                                                     'uri': self.uri})

    def has_attrs(self):
        return any([x is not None for x in [self.publicId, self.uri]])

    @staticmethod
    def object(node):
        """Create object from etree node"""
        if node is None:
            return None
        return Public(node.get('publicId'), node.get('uri'))


@dataclass
class LPDependency:
    """Represents a dependency (tool/model/data) of a linguistic processor"""
    name: str
    version: Union[str, None] = None
    """optional attribute"""
    type: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        return create_node('lpDependency',
                           attributes={'name': self.name},
                           optional_attrs={'version': self.version, 'type': self.type})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return LPDependency(node.get('name'), node.get('version'), node.get('type'))


@dataclass
class LP:
    """Represents a linguistic processor"""
    name: str
    version: str
    lpDependencies: List[LPDependency]
    timestamp: Union[str, None] = None
    """optional attribute"""
    beginTimestamp: Union[str, None] = None
    """optional attribute"""
    endTimestamp: Union[str, None] = None
    """optional attribute"""
    hostname: Union[str, None] = None
    """optional attribute"""
    id: Union[str, None] = None
    """optional attribute"""

    def node(self):
        """Create etree node from object"""
        return create_node('lp',
                           children=self.lpDependencies,
                           attributes={'name': self.name, 'version': self.version},
                           optional_attrs={
                               'timestamp': self.timestamp,
                               'beginTimestamp': self.beginTimestamp,
                               'endTimestamp': self.endTimestamp,
                               'hostname': self.hostname,
                               'id': self.id
                           })

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return LP(node.get('name'),
                  node.get('version'),
                  [LPDependency.object(n) for n in node],
                  node.get('timestamp'),
                  node.get('beginTimestamp'),
                  node.get('endTimestamp'),
                  node.get('hostname'),
                  node.get('id'))


@dataclass
class LinguisticProcessors:
    """Represents a linguisticProcessors element: the list of linguistic processors for a given layer."""
    layer_name: str
    lps: List[LP]
    """list of linguistic processors"""

    def node(self):
        """Create etree node from object"""
        return create_node('linguisticProcessors', children=self.lps, attributes={'layer': self.layer_name})

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return LinguisticProcessors(node.get('layer'), [LP.object(n) for n in node])


@dataclass
class NafHeader:
    fileDesc: FileDesc = FileDesc()
    public: Public = Public()
    linguisticProcessors: List[LinguisticProcessors] = field(default_factory=list)

    def node(self):
        """Create etree node from object"""
        children = []
        if self.fileDesc.has_attrs():
            children.append(self.fileDesc)
        if self.public.has_attrs():
            children.append(self.public)
        children.extend(self.linguisticProcessors)
        return create_node('nafHeader', children=children)

    @staticmethod
    def object(node):
        """Create object from etree node"""
        return NafHeader(FileDesc.object(node.find('fileDesc')),
                         Public.object(node.find('public')),
                         [LinguisticProcessors.object(n) for n in node.findall('linguisticProcessors')])
