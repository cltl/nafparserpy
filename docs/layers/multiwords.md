Module nafparserpy.layers.multiwords
====================================

Classes
-------

`Multiwords(items: List[nafparserpy.layers.multiwords.Mw])`
:   Multiwords layer class

    ### Class variables

    `items: List[nafparserpy.layers.multiwords.Mw]`
    :   list of multiwords

    ### Static methods

    `object(node)`
    :   Create list of `Mw` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Mw(id: str, type: str, components: List[nafparserpy.layers.elements.Component], externalRefs: nafparserpy.layers.elements.ExternalReferences = ExternalReferences(items=[]), attrs: dict = <factory>)`
:   Represents a multiword expression

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :

    `components: List[nafparserpy.layers.elements.Component]`
    :

    `externalRefs: nafparserpy.layers.elements.ExternalReferences`
    :

    `id: str`
    :

    `type: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object