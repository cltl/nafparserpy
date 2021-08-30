"""
This module implements a parser for NAF files and is based on the Kafnafparserpy.
Compared to Kafnafparserpy, the module: only supports NAF; supports a more recent version
of NAF; is compatible with Python 3.7+.


@author: U{Sophie Arnoult}
@version: 0.1
@contact: U{s.i.arnoult@vu.nl<mailto:s.i.arnoult@vu.nl>}
@since: 27-Aug-2021
"""

from nafparserpy.classes.attribution import Attribution
from nafparserpy.classes.causal_relations import CausalRelations
from nafparserpy.classes.chunks import Chunks
from nafparserpy.classes.constituency import Constituency
from nafparserpy.classes.coreferences import Coreferences
from nafparserpy.classes.deps import Deps
from nafparserpy.classes.entities import Entities
from nafparserpy.classes.factualities import Factualities
from nafparserpy.classes.markables import Markables
from nafparserpy.classes.multiwords import Multiwords
from nafparserpy.classes.naf_header import *
from nafparserpy.classes.opinions import Opinions
from nafparserpy.classes.raw import Raw
from nafparserpy.classes.srl import Srl
from nafparserpy.classes.temporal_relations import TemporalRelations
from nafparserpy.classes.terms import Terms
from nafparserpy.classes.text import Text
from nafparserpy.classes.time_expressions import TimeExpressions
from nafparserpy.classes.topics import Topics
from nafparserpy.classes.tunits import Tunits
from lxml import etree

__last_modified__ = '27Augustus2021'
__version__ = '0.1'
__author__ = 'Sophie Arnoult'

NAF_VERSION = '3.2'


class Locations(object):
    """FIXME clarify DTD"""
    pass


class Dates(object):
    """FIXME clarify DTD"""
    pass


layers = {'nafHeader': NafHeader, 'fileDesc': FileDesc, 'public': Public, 'linguisticProcessors': LinguisticProcessors,
          'lp': LP, 'raw': Raw, 'topics': Topics, 'text': Text, 'terms': Terms, 'chunks': Chunks,
          'multiwords': Multiwords, 'deps': Deps, 'constituency': Constituency, 'coreferences': Coreferences,
          'srl': Srl, 'opinions': Opinions, 'timeExpressions': TimeExpressions, 'tunits': Tunits,
          'locations': Locations, 'dates': Dates, 'temporalRelations': TemporalRelations, 'entities': Entities,
          'causalRelations': CausalRelations, 'markables': Markables, 'attribution': Attribution,
          'factualities': Factualities}


class NafParser:
    def __init__(self, tree=None, lang='en', version=None, filename=None):
        """
        Creates a NAF document. Use U{parse} to parse an existing document.
        @type filename: string
        @param filename: NAF filename
        @type lang: string
        @param lang: language of document
        """
        naf_version = NAF_VERSION
        if version is not None:
            naf_version = version
        if tree is None:
            self.tree = etree.ElementTree(etree.Element('NAF'))
            self.root = self.tree.getroot()
            self.root.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
            self.root.set('version', naf_version)
        else:
            self.tree = tree
            self.root = self.tree.getroot()
        self.filename = filename

    @staticmethod
    def parse(filename):
        filename = filename
        tree = etree.parse(filename, etree.XMLParser(remove_blank_text=True, strip_cdata=False))
        return NafParser(tree)

    def write(self, filename=None):
        if filename is None:
            print(etree.tostring(self.root, encoding='UTF-8', pretty_print=True, xml_declaration=True))
        else:
            self.tree.write(filename, encoding='UTF-8', pretty_print=True, xml_declaration=True)

    def has_layer(self, layer):
        return self.root.findall('.//{}'.format(layer))

    def get(self, layer):
        if not self.has_layer(layer):
            raise ValueError("layer {} does not exist".format(layer))
        nodes = self.root.findall('.//{}'.format(layer))
        return layers[layer].get_obj(nodes[0])

    def getall(self, layer):
        if not self.has_layer(layer):
            raise ValueError("layer {} does not exist".format(layer))
        nodes = self.root.findall('.//{}'.format(layer))
        return [layers[layer].get_obj(node) for node in nodes]

    def add_layer(self, layer_name, element, exist_ok=False):
        """adds a layer to the xml tree.
        :param layer_name: naf layer name
        :type layer_name: str
        :param element: new layer
        :type element: U{Layer} class or subclass object
        :param exist_ok: allows replacement of existing layer
        :raises ValueError: if layer already exists and U{exist_ok} is False
        """
        if self.has_layer(layer_name) and not exist_ok:
            raise ValueError('Layer {} already exists'.format(layer_name))
        else:
            if self.has_layer(layer_name):
                self.root.remove(self.root.find(layer_name))
            self.root.append(element.node())

    def add_container_layer(self, layer_name, elements, exist_ok=False):
        """creates container layer from its elements and adds it to the xml tree.

        This method can be applied to almost all layers, with the exception of
        U{NafHeader}, U{Raw} and U{TemporalRelations}

        :param layer_name: naf layer name
        :type layer_name: str
        :param elements: layer elements
        :type element: U{List[T]} where T is the type of layer elements
        :param exist_ok: allows replacement of existing layer
        :raises ValueError: if layer already exists and U{exist_ok} is False
        """
        self.add_layer(layer_name,
                       layers[layer_name](elements),
                       exist_ok=exist_ok)

    def add_naf_header(self, fileDesc_attrs={}, public_attrs={}, linguistic_processors=[], exist_ok=False):
        """
        creates naf header and attaches it to xml tree
        :param fileDesc_attrs: fileDesc attributes
        :type fileDesc_attrs: dict
        :param public_attrs: public attributes
        :param linguistic_processors: linguistic processor objects
        :type linguistic_processors: U{List[LinguisticProcessor]}
        :param exist_ok: allows replacement of existing layer
        """
        self.add_layer('nafHeader', NafHeader.create(fileDesc_attrs, public_attrs, linguistic_processors), exist_ok)

    def add_linguistic_processor(self, layer, name, version, attributes={}):
        """adds a linguistic processor to a given layer.

        Creates a NafHeader is there is not already one
        :param layer: the name of the layer
        :param name: the name of the linguistic processor
        :param version: the version of the linguistic processor"""
        if not self.has_layer('nafHeader'):
            self.add_naf_header()
        naf_header_node = self.root.find('nafHeader')
        ling_processors_layer_node = self.root.xpath('//linguisticProcessors[@layer={}]'.format(layer))
        if not ling_processors_layer_node:
            ling_processors_layer_node = LinguisticProcessors(layer, [LP(name, version, attributes)]).node()
            naf_header_node.append(ling_processors_layer_node)
        else:
            ling_processors_layer_node.append(LP(name, version, attributes).node())

    def add_raw_layer(self, text, exist_ok=False):
        """add (or replace) raw layer
        :param text: raw text
        :type text: str
        :param exist_ok: allows replacement of existing layer"""
        self.add_layer('raw', Raw(text), exist_ok)

