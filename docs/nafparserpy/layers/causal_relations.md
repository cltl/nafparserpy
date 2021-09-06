Module nafparserpy.layers.causal_relations
==========================================

Classes
-------

`CLink(id: str, from_idref: str, to: str, attrs: dict = <factory>)`
:   Represents a causal link

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes: 'relType' (causal relation type)

    `from_idref: str`
    :   field for NAF attribute 'from' (note difference in name)

    `id: str`
    :   causal link if

    `to: str`
    :   field for NAF attribute 'to'

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`CausalRelations(items: List[nafparserpy.layers.causal_relations.CLink])`
:   Causal Relations layer class

    ### Class variables

    `items: List[nafparserpy.layers.causal_relations.CLink]`
    :   list of causal links

    ### Static methods

    `object(node)`
    :   Create list of `CLink` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object