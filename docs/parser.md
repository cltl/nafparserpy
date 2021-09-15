Module nafparserpy.parser
=========================
Wraps lxml to facilitate handling of NAF documents

Functions
---------

    
`split_naf_header_attrs(attrs)`
:   Split input attributes in public or fileDesc attributes
    
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

Classes
-------

`NafParser(tree=None, lang='en', version=None, **attrs)`
:   Create a NAF document from an existing tree or from scratch.
    
    Parameters
    ----------
    tree : etree
        input tree
    lang : str
        document language, defaults to `en`. This parameter is ignored if tree is not None
    version : str
        NAF version, defaults to `parser.NAF_VERSION`; ignored if tree is not None
    attrs : dict
        nafHeader fileDesc and public attributes; ignored if tree is not None

    ### Static methods

    `load(filename)`
    :   Create a NAF document from a NAF file

    ### Methods

    `add_layer(self, layer_name: str, element: Any, exist_ok=False)`
    :   Add a layer to the NAF xml tree
        
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

    `add_layer_from_elements(self, layer_name: str, elements: list, exist_ok=False)`
    :   Create container layer from its elements.
        
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

    `add_linguistic_processor(self, layer: str, name: str, version: str, lpDependencies=[], attributes={})`
    :   Add a `linguistic processor` element to the linguistic processors list for the given layer.
        
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

    `add_naf_header(self, fileDesc_attrs={}, public_attrs={}, linguistic_processors=[], exist_ok=False)`
    :   Create and add `nafHeader` layer
        
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

    `add_raw_layer(self, text: str, exist_ok=False)`
    :   Add (or replace) raw layer from text
        
        Parameters
        ----------
        text : str
            raw layer text
        exist_ok : bool
            allows replacement of existing layer

    `get(self, layer_name: str)`
    :   Return a layer object for the layer with the given layer-name.
        
        Returns only the first object if more elements carry the same name.

    `get_lps(self, layer_name)`
    :   Return list of linguistic processors for a given layer
        
        Parameters
        ----------
        layer_name: str
            layer name
        
        Returns
        -------
        list of Lp objects
        
        Raises
        ------
        ValueError: if the NAF header has no linguisticProcessors element for that layer

    `getall(self, layer_name: str)`
    :   Return a list of layer objects for each layer carrying the given layer-name

    `has_layer(self, layer: str)`
    :   Returns True if layer with given name exists

    `write(self, file_path)`
    :   Write NAF tree to file or stdout if no file path is given