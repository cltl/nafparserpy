Module nafparserpy.layers.coreferences
======================================

Classes
-------

`Coref(id: str, status: str, spans: List[nafparserpy.layers.elements.Span], externalReferences: nafparserpy.layers.elements.ExternalReferences = <factory>, attrs: dict = <factory>)`
:   Represents a coreference

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.IdrefGetter
    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes: 'type', 'status'

    `externalReferences: nafparserpy.layers.elements.ExternalReferences`
    :   optional external references

    `id: str`
    :

    `spans: List[nafparserpy.layers.elements.Span]`
    :   list of coreferent mention spans

    `status: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

    `target_ids(self)`
    :   Returns list of target ids covered for each of the layer's spans

`Coreferences(items: List[nafparserpy.layers.coreferences.Coref])`
:   Coreference layer class

    ### Class variables

    `items: List[nafparserpy.layers.coreferences.Coref]`
    :   list of coreferences

    ### Static methods

    `object(node)`
    :   Create list of `Coref` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object