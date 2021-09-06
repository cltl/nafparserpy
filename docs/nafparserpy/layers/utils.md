Module nafparserpy.layers.utils
===============================

Functions
---------

    
`create_node(layer, text, children, attributes)`
:   Create an etree Element node from the text, children and attributes of NAF objects
    
    Parameters
    ----------
    layer : str
        layer name
    text : str
        text of node
    children : list
        list of NAF objects to add as subelements in the node
    attributes : dict
        node attributes (whether compulsory or optional)

Classes
-------

`AttributeGetter()`
:   Provides an attribute getter

    ### Descendants

    * nafparserpy.layers.causal_relations.CLink
    * nafparserpy.layers.chunks.Chunk
    * nafparserpy.layers.constituency.Edge
    * nafparserpy.layers.coreferences.Coref
    * nafparserpy.layers.elements.Component
    * nafparserpy.layers.elements.ExternalRef
    * nafparserpy.layers.entities.Entity
    * nafparserpy.layers.factualities.FactVal
    * nafparserpy.layers.markables.Mark
    * nafparserpy.layers.multiwords.Mw
    * nafparserpy.layers.naf_header.LP
    * nafparserpy.layers.naf_header.LPDependency
    * nafparserpy.layers.opinions.OpinionExpression
    * nafparserpy.layers.opinions.OpinionHolder
    * nafparserpy.layers.opinions.OpinionTarget
    * nafparserpy.layers.srl.Predicate
    * nafparserpy.layers.srl.Role
    * nafparserpy.layers.temporal_relations.PredicateAnchor
    * nafparserpy.layers.terms.Term
    * nafparserpy.layers.text.Wf
    * nafparserpy.layers.time_expressions.Timex3
    * nafparserpy.layers.topics.Topic
    * nafparserpy.layers.tunits.Tunit
    * nafparserpy.layers.utils.AttributeLayer

    ### Methods

    `get(self, attribute)`
    :   Get attribute from `attrs` field
        
        Parameters
        ----------
        attribute : str
            attribute name
        
        Raises
        ------
        KeyError: if the layer has no such attribute

    `has(self, attribute)`
    :   Test if attribute appears in `attrs` field

`AttributeLayer(layer: str, attrs: dict = <factory>)`
:   A layer containing only attributes

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Descendants

    * nafparserpy.layers.elements.Sentiment
    * nafparserpy.layers.naf_header.FileDesc
    * nafparserpy.layers.naf_header.Public

    ### Class variables

    `attrs: dict`
    :   optional attributes (keys are subclass dependent)

    `layer: str`
    :

    ### Static methods

    `object(layer_name, node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`IdrefGetter()`
:   Provides a target ids getter for layers with a `span` field

    ### Descendants

    * nafparserpy.layers.coreferences.Coref
    * nafparserpy.layers.elements.Component
    * nafparserpy.layers.entities.Entity
    * nafparserpy.layers.factualities.Factuality
    * nafparserpy.layers.markables.Mark
    * nafparserpy.layers.terms.Term

    ### Methods

    `target_ids(self)`
    :   Return list of target ids covered by the layer's span