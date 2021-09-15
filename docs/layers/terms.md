Module nafparserpy.layers.terms
===============================

Classes
-------

`Term(id: str, span: nafparserpy.layers.elements.Span, components: List[nafparserpy.layers.elements.Component] = <factory>, externalReferences: nafparserpy.layers.elements.ExternalReferences = <factory>, sentiment: nafparserpy.layers.elements.Sentiment = None, attrs: dict = <factory>)`
:   Represents a term

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter
    * nafparserpy.layers.utils.IdrefGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'netype', 'case', 'head', 'component_of',
        'compound_type')

    `components: List[nafparserpy.layers.elements.Component]`
    :   optional list of morphemes in term

    `externalReferences: nafparserpy.layers.elements.ExternalReferences`
    :   optional ExternalReferences

    `id: str`
    :

    `sentiment: nafparserpy.layers.elements.Sentiment`
    :   optional sentiment

    `span: nafparserpy.layers.elements.Span`
    :   span of covered idrefs

    ### Static methods

    `create(term_id, target_ids, term_attrs)`
    :   creates a basic term with id, attributes and target ids

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Terms(items: List[nafparserpy.layers.terms.Term])`
:   Terms layer class

    ### Class variables

    `items: List[nafparserpy.layers.terms.Term]`
    :   list of terms

    ### Static methods

    `object(node)`
    :   Create list of `Term` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object