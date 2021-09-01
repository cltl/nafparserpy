"""
Wraps lxml to facilitate handling of NAF documents
"""
from typing import Any

from nafparserpy.layers.attribution import Attribution
from nafparserpy.layers.causal_relations import CausalRelations
from nafparserpy.layers.chunks import Chunks
from nafparserpy.layers.constituency import Constituency
from nafparserpy.layers.coreferences import Coreferences
from nafparserpy.layers.deps import Deps
from nafparserpy.layers.entities import Entities
from nafparserpy.layers.factualities import Factualities
from nafparserpy.layers.locations_dates import Locations, Dates
from nafparserpy.layers.markables import Markables
from nafparserpy.layers.multiwords import Multiwords
from nafparserpy.layers.naf_header import *
from nafparserpy.layers.opinions import Opinions
from nafparserpy.layers.raw import Raw
from nafparserpy.layers.srl import Srl
from nafparserpy.layers.temporal_relations import TemporalRelations
from nafparserpy.layers.terms import Terms
from nafparserpy.layers.text import Text
from nafparserpy.layers.time_expressions import TimeExpressions
from nafparserpy.layers.topics import Topics
from nafparserpy.layers.tunits import Tunits
from lxml import etree

__version__ = '0.1'
__author__ = 'Sophie Arnoult'

NAF_VERSION = '3.2'

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
        Create a NAF document.

        Parameters
        ----------
        tree : etree
            input tree
        lang : str
            document language, defaults to `en` if not specified by input `tree`
        version : str
            NAF version, defaults to `parser.NAF_VERSION` if not specified by input `tree`
        filename : str
            NAF filename; triggers creation of nafHeader layer when creating document from scratch
        """
        naf_version = NAF_VERSION
        self.filename = filename
        if version is not None:
            naf_version = version
        if tree is None:
            self.tree = etree.ElementTree(etree.Element('NAF'))
            self.root = self.tree.getroot()
            self.root.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
            self.root.set('version', naf_version)
            if self.filename is not None:
                self.add_naf_header(fileDesc_attrs={'filename': filename})
        else:
            self.tree = tree
            self.root = self.tree.getroot()

    @staticmethod
    def parse(filename):
        filename = filename
        tree = etree.parse(filename, etree.XMLParser(remove_blank_text=True, strip_cdata=False))
        return NafParser(tree)

    def write(self, filename=None):
        """Write NAF tree to file or stdout if no file-name is given"""
        if filename is None:
            print(etree.tostring(self.root, encoding='UTF-8', pretty_print=True, xml_declaration=True))
        else:
            self.tree.write(filename, encoding='UTF-8', pretty_print=True, xml_declaration=True)

    def has_layer(self, layer: str):
        """Returns True if layer with given name exists"""
        return self.root.findall('.//{}'.format(layer))

    def get(self, layer_name: str):
        """Return a layer object for the layer with the given layer-name.

        Returns only the first object if more elements carry the same name."""
        if not self.has_layer(layer_name):
            raise ValueError("layer {} does not exist".format(layer_name))
        nodes = self.root.findall('.//{}'.format(layer_name))
        return layers[layer_name].get_obj(nodes[0])

    def getall(self, layer_name: str):
        """Return a list of layer objects for each layer carrying the given layer-name
        """
        if not self.has_layer(layer_name):
            raise ValueError("layer {} does not exist".format(layer_name))
        nodes = self.root.findall('.//{}'.format(layer_name))
        return [layers[layer_name].get_obj(node) for node in nodes]

    def add_layer(self, layer_name: str, element: Any, exist_ok=False):
        """Add a layer to the NAF xml tree

        Parameters
        ----------
        layer_name : str
            naf layer name
        element : Any
            layer object
        exist_ok : bool
            allows replacement of existing layer

        Raises
        ------
        ValueError: if layer already exists and `exist_ok` is False
        """
        if self.has_layer(layer_name) and not exist_ok:
            raise ValueError('Layer {} already exists'.format(layer_name))
        else:
            if self.has_layer(layer_name):
                self.root.remove(self.root.find(layer_name))
            self.root.append(element.node())

    def add_container_layer(self, layer_name: str, elements: list, exist_ok=False):
        """Create container layer from its elements.

        This method can be applied to non-empty layers without attributes. This concerns almost all layers,
        with the exception of `NafHeader`, `Raw` and `TemporalRelations`

        Parameters
        ----------
        layer_name : str
            naf layer name
        elements : list
            list of layer elements objects
        exist_ok : bool
            allows replacement of existing layer

        Raises
        ------
        ValueError: if layer already exists and `exist_ok` is False
        """
        self.add_layer(layer_name,
                       layers[layer_name](elements),
                       exist_ok=exist_ok)

    def add_naf_header(self, fileDesc_attrs={}, public_attrs={}, linguistic_processors=[], exist_ok=False):
        """
        Create and add `nafHeader` layer

        Parameters
        ----------
        fileDesc_attrs : dict
            `fileDesc` layer attributes
        public_attrs : dict
            `public` layer attributes
        linguistic_processors : list[LinguisticProcessors]
            list of `LinguisticProcessors` objects per layer
        exist_ok : bool
            allows replacement of existing layer
        """
        self.add_layer('nafHeader', NafHeader.create(fileDesc_attrs, public_attrs, linguistic_processors), exist_ok)

    def add_linguistic_processor(self, layer: str, name: str, version: str, attributes={}):
        """Add a `linguistic processor` element to the linguistic processors list for the given layer.

        Creates a `nafHeader` layer and/or a `linguisticProcessors` layer there is not already one.

        Parameters
        ----------
        layer : str
            the name of the layer
        name : str
            the name of the linguistic processor
        version : str
            the version of the linguistic processor
        attributes : dict
            optional linguistic processor attributes ('timestamp', 'beginTimestamp', 'endTimestamp', 'hostname')"""
        if not self.has_layer('nafHeader'):
            self.add_naf_header()
        naf_header_node = self.root.find('nafHeader')
        ling_processors_layer_node = self.root.xpath('//linguisticProcessors[@layer={}]'.format(layer))
        if not ling_processors_layer_node:
            ling_processors_layer_node = LinguisticProcessors(layer, [LP(name, version, attributes)]).node()
            naf_header_node.append(ling_processors_layer_node)
        else:
            ling_processors_layer_node.append(LP(name, version, attributes).node())

    def add_raw_layer(self, text: str, exist_ok=False):
        """Add (or replace) raw layer from text

        Parameters
        ----------
        text : str
            raw layer text
        exist_ok : bool
            allows replacement of existing layer"""
        self.add_layer('raw', Raw(text), exist_ok)

