Module nafparserpy.layers.tunits
================================

Classes
-------

`Tunit(id: str, offset: str, length: str, attrs: dict = <factory>)`
:   Represents a text unit

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('type', 'xpath')

    `id: str`
    :

    `length: str`
    :

    `offset: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Tunits(items: List[nafparserpy.layers.tunits.Tunit])`
:   Tunits layer class

    ### Class variables

    `items: List[nafparserpy.layers.tunits.Tunit]`
    :   list of text units

    ### Static methods

    `object(node)`
    :   Create list of `Tunit` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object