Module nafparserpy.layers.markables
===================================

Classes
-------

`Mark(id: str, span: nafparserpy.layers.elements.Span, sentiment: nafparserpy.layers.elements.Sentiment = None, externalReferences: nafparserpy.layers.elements.ExternalReferences = ExternalReferences(items=[]), attrs: dict = <factory>)`
:   Represents a mark

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter
    * nafparserpy.layers.utils.IdrefGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'case', 'source')

    `externalReferences: nafparserpy.layers.elements.ExternalReferences`
    :   optional externalReferences

    `id: str`
    :

    `sentiment: nafparserpy.layers.elements.Sentiment`
    :   optional sentiment

    `span: nafparserpy.layers.elements.Span`
    :   span of covered target ids

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Markables(items: List[nafparserpy.layers.markables.Mark])`
:   Markables layer class

    ### Class variables

    `items: List[nafparserpy.layers.markables.Mark]`
    :

    ### Static methods

    `object(node)`
    :   Create list of `Mark` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object