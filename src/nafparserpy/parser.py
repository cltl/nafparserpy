"""
Wraps lxml to facilitate handling of NAF documents
"""
import datetime
import re
from typing import Any, Tuple, Dict, List

from nafparserpy.layers.naf_header import NafHeader, LP, LinguisticProcessors
from nafparserpy.layers.raw import Raw
from lxml import etree

from nafparserpy.layers.factory import create_from_node, create_from_elements

NAF_VERSION = '3.3'


def split_naf_header_attrs(attrs):
    """Split input attributes in public or fileDesc attributes

    Parameters
    ----------
    attrs : dict
        dictionary of public/fileDesc attributes

    Returns
    -------
    a tuple of attribute dictionaries for fileDesc and public

    Raises
    ------
    KeyError: if the input dictionary contains keywords not pertaining to public/fileDesc attributes
        """
    public_attrs = {}
    filedesc_attrs = {}
    public_keys = ['publicId', 'uri']
    filedesc_keys = ['title', 'author', 'creationtime', 'filename', 'filetype', 'pages']
    for k in attrs:
        if k in public_keys:
            public_attrs.update({k: attrs[k]})
        elif k in filedesc_keys:
            filedesc_attrs.update({k: attrs[k]})
        else:
            raise KeyError('unknown public/fileDesc key: {}'.format(k))
    return filedesc_attrs, public_attrs


def validate_dtd(tree, dtd='naf_v3.3.dtd'):
    """Validate tree against DTD

    Parameters
    ----------
    tree : ElementTree
        NAF tree
    dtd : str
        path to DTD

    Raises
    ------
    ValueError : if tree is not valid
    """
    with open(dtd) as infile:
        dtd = etree.DTD(infile)
    if not dtd.validate(tree.getroot()):
        raise ValueError(f"Input tree does not conform to DTD {dtd}")


def remove_lps(ling_processors_layer_node):
    lps = [child for child in ling_processors_layer_node]
    for lp in lps:
        ling_processors_layer_node.remove(lp)


class NafParser:
    def __init__(self, tree=None, lang='en', version=None, decorate=True, **attrs):
        """
        Create a NAF document from an existing tree or from scratch.

        Parameters
        ----------
        tree : etree
            input tree
        lang : str
            document language, defaults to `en`. This parameter is ignored if tree is not None
        version : str
            NAF version, defaults to `parser.NAF_VERSION`; ignored if tree is not None
        decorate : bool
            adds covered text to span nodes
        attrs : dict
            nafHeader fileDesc and public attributes; ignored if tree is not None
        """
        self.decorate = decorate
        naf_version = NAF_VERSION
        if version is not None:
            naf_version = version
        if tree is None:
            self.tree = etree.ElementTree(etree.Element('NAF'))
            self.root = self.tree.getroot()
            self.root.set('{http://www.w3.org/XML/1998/namespace}lang', lang)
            self.root.set('version', naf_version)
            if attrs:
                filedesc_attrs, public_attrs = split_naf_header_attrs(attrs)
                self.add_naf_header(fileDesc_attrs=filedesc_attrs, public_attrs=public_attrs)
            self.id_map = {}
        else:
            self.tree = tree
            self.root = self.tree.getroot()
            self.id_map = self.targets2indices()

    @staticmethod
    def load(naf_file, validate_against_dtd=False, decorate=True):
        """Create a NAF document from a NAF file

        Parameters
        ----------
        naf_file : str
            path to NAF file
        validate_against_dtd : bool
            validates input tree against DTD if True
        decorate : bool
            adds covered text to span nodes

        Raises
        ------
        ValueError: if `validate_against_dtd` is True, and input file does not conform to the DTD
        """
        tree = etree.parse(naf_file, etree.XMLParser(remove_blank_text=True, strip_cdata=False))

        if validate_against_dtd:
            validate_dtd(tree)

        return NafParser(tree, decorate=decorate)

    def write(self, file_path):
        """Write NAF tree to file or stdout if no file path is given"""
        if file_path is None:
            print(etree.tostring(self.root, encoding='UTF-8', pretty_print=True, xml_declaration=True))
        else:
            self.tree.write(file_path, encoding='UTF-8', pretty_print=True, xml_declaration=True)

    def has_layer(self, layer: str):
        """Returns True if layer with given name exists"""
        return self.root.findall('.//{}'.format(layer))

    def get(self, layer_name: str):
        """Return a layer object for the layer with the given layer-name.

        Returns only the first object if more elements carry the same name."""
        if not self.has_layer(layer_name):
            raise ValueError("layer {} does not exist".format(layer_name))
        nodes = self.root.findall('.//{}'.format(layer_name))
        return create_from_node[layer_name](nodes[0])

    def getall(self, layer_name: str):
        """Return a list of layer objects for each layer carrying the given layer-name
        """
        if not self.has_layer(layer_name):
            raise ValueError("layer {} does not exist".format(layer_name))
        nodes = self.root.findall('.//{}'.format(layer_name))
        return [create_from_node[layer_name](node) for node in nodes]

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
            if layer_name in ('text', 'terms'):
                self.reset_targets2indices()
            if self.decorate:
                self.add_comments()

    def add_layer_from_elements(self, layer_name: str, elements: list, exist_ok=False):
        """Create container layer from its elements.

        This method can be applied to non-empty layers without attributes. This concerns almost all layers,
        except for `NafHeader`, `Raw` and `TemporalRelations`

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
                       create_from_elements[layer_name](elements),
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

    def add_linguistic_processor(self, layer: str, name: str, version: str, lpDependencies=[], attributes={},
                                 add_time_stamp=True, replace=False):
        """Add a `linguistic processor` element to the linguistic processors list for the given layer.

        Creates a `nafHeader` layer and/or a `linguisticProcessors` layer if there is not one yet.

        Parameters
        ----------
        layer : str
            the name of the layer
        name : str
            the name of the linguistic processor
        version : str
            the version of the linguistic processor
        lpDependencies : List(LPDependency)
            list of linguistic processor dependencies
        attributes : dict
            optional linguistic processor attributes ('timestamp', 'beginTimestamp', 'endTimestamp', 'hostname')
        add_time_stamp : bool
            create time stamp
        replace : bool
            replace or append to `lp` elements for that layer
        """
        if not self.has_layer('nafHeader'):
            self.add_naf_header()
        if add_time_stamp:
            attributes['timestamp'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
        self.add_lp(layer, LP(name, version, lpDependencies, attributes), replace)

    def add_lp(self, layer: str, linguistic_processor: LP, replace: bool):
        """Add a linguistic processor element to the linguistic processors list for the given layer.

        Creates a `linguisticProcessors` layer if there is not one yet. Pre-existing linguistic processor elements are
        replaced if `replace` is True.

        Parameters
        ----------
        layer : str
            the name of the layer
        linguistic_processor : LP
            the linguistic processor
        replace : bool
            replace or append to `lp` elements for that layer
        """
        naf_header_node = self.root.find('nafHeader')
        ling_processors_layer_nodes = [lps for lps in naf_header_node.findall('linguisticProcessors')
                                       if lps.get('layer') == layer]
        if not ling_processors_layer_nodes:
            ling_processors_layer_node = LinguisticProcessors(layer, [linguistic_processor]).node()
            naf_header_node.append(ling_processors_layer_node)
        elif replace:
            remove_lps(ling_processors_layer_nodes[0])
            ling_processors_layer_nodes[0].append(linguistic_processor.node())
        else:
            ling_processors_layer_nodes[0].append(linguistic_processor.node())

    def extend_lps(self, layer: str, linguistic_processors: List[LP], replace=False):
        """Add linguistic processor elements to the linguistic processors list for the given layer.

        Creates a `linguisticProcessors` layer if there is not one yet.

        Parameters
        ----------
        layer : str
            the name of the layer
        linguistic_processors : List[LP]
            the linguistic processors
        """
        naf_header_node = self.root.find('nafHeader')
        ling_processors_layer_nodes = [lps for lps in naf_header_node.findall('linguisticProcessors')
                                       if lps.get('layer') == layer]
        if not ling_processors_layer_nodes:
            ling_processors_layer_node = LinguisticProcessors(layer, linguistic_processors).node()
            naf_header_node.append(ling_processors_layer_node)
        elif replace:
            remove_lps(ling_processors_layer_nodes[0])
            ling_processors_layer_nodes[0] = [lp.node() for lp in linguistic_processors]
        else:
            ling_processors_layer_nodes[0].extend([lp.node() for lp in linguistic_processors])

    def add_raw_layer(self, text: str, exist_ok=False):
        """Add (or replace) raw layer from text

        Parameters
        ----------
        text : str
            raw layer text
        exist_ok : bool
            allows replacement of existing layer"""
        self.add_layer('raw', Raw(text), exist_ok)

    def get_lps(self, layer_name):
        """Return list of linguistic processors for a given layer

        Parameters
        ----------
        layer_name: str
            layer name

        Returns
        -------
        list of Lp objects

        Raises
        ------
        ValueError: if the NAF header has no linguisticProcessors element for that layer"""

        lprocessors = [x for x in self.getall('linguisticProcessors') if x.layer_name == layer_name]
        if lprocessors:
            return lprocessors[0].lps
        else:
            return None

    def targets2indices(self) -> Dict[str, Tuple[int, int]]:
        """Map each word form, subtoken or term id to its begin and end indices

        Returns
        -------
        map of target ids to start and end indices
        """
        if not self.has_layer('text'):
            return {}
        id_map = {}
        for wf in self.get('text'):
            id_map[wf.id] = (int(wf.offset), int(wf.offset) + int(wf.length))
            if wf.subtokens:
                id_map.update({st.id: (int(st.offset), int(st.offset) + int(st.length)) for st in wf.subtokens})
        if self.has_layer('terms'):     # higher layers may reference to terms
            # map term ids to begin/end indices through word-form ids
            twf_map = {t.id: id_map[t.span.target_ids()[0]] for t in self.get('terms')}
            id_map.update(twf_map)
        return id_map

    def add_comments(self):
        """Add covered text as comment to all Span elements that have no comment yet"""
        spans = [x for x in self.root.findall('.//span') if not [_ for _ in x.iter(tag=etree.Comment)]]
        target_ids = [[t.get('id') for t in span.findall('target')] for span in spans]
        if spans and not self.id_map:
            self.id_map = self.targets2indices()
        for span_node, tid_span in zip(spans, target_ids):
            begin, end = self.id_map[tid_span[0]][0], self.id_map[tid_span[-1]][1]
            comment = self.get('raw').text[begin:end]
            comment = comment.replace('--', '-~')
            comment = re.sub('-$', '~', comment)
            span_node.append(etree.Comment(comment))

    def covered_text(self, target_ids: List[str]) -> str:
        """Return text covered by the target ids

        Parameters
        ----------
        target_ids: List[str]
            target ids

        Returns
        -------
        covered text
        """
        start, end = self.start_end_indices(target_ids)
        return self.get('raw').text[start:end]

    def start_end_indices(self, target_ids: List[str]) -> Tuple[int, int]:
        """Return the start and end indices of the span represented by the target ids

        Parameters
        ----------
        target_ids: List[str]
            target ids

        Returns
        -------
        tuple of start and end indices
        """
        if not self.id_map:
            self.id_map = self.targets2indices()
            if not self.id_map:
                raise ValueError('No target ids found')
        return self.id_map[target_ids[0]][0], self.id_map[target_ids[-1]][1]

    def reset_targets2indices(self):
        """Recomputes the mapping of all word forms, subtokens and terms to their start and end indices.

        This mapping is computed in a restricted number of cases: when loading a existing NAF document, or when
        retrieving the covered text on a newly created NAF document. The present function can be called when
        adding layers for which the mapping will be relevant, such as subtokens or terms on a NAF document already
        annotated with word forms.
        """
        self.id_map = self.targets2indices()
