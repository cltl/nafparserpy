Module nafparserpy.layers.factualities
======================================

Classes
-------

`FactVal(value: str, resource: str, attrs: dict = <factory>)`
:   Represents a factuality value

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('confidence', 'source')

    `resource: str`
    :

    `value: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Factualities(items: List[nafparserpy.layers.factualities.Factuality])`
:   Factualities layer class

    ### Class variables

    `items: List[nafparserpy.layers.factualities.Factuality]`
    :   list of factualities

    ### Static methods

    `object(node)`
    :   Create list of `Factuality` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Factuality(id: str, span: nafparserpy.layers.elements.Span, fact_vals: List[nafparserpy.layers.factualities.FactVal])`
:   Represents a factuality

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.IdrefGetter

    ### Class variables

    `fact_vals: List[nafparserpy.layers.factualities.FactVal]`
    :

    `id: str`
    :

    `span: nafparserpy.layers.elements.Span`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object