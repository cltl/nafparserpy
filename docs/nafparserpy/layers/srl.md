Module nafparserpy.layers.srl
=============================

Classes
-------

`Predicate(id: str, span: nafparserpy.layers.elements.Span, externalReferences: nafparserpy.layers.elements.ExternalReferences = <factory>, roles: List[nafparserpy.layers.srl.Role] = <factory>, attrs: dict = <factory>)`
:   Represents a predicate

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('confidence', 'status')

    `externalReferences: nafparserpy.layers.elements.ExternalReferences`
    :   optional external references

    `id: str`
    :

    `roles: List[nafparserpy.layers.srl.Role]`
    :   optional list of predicate arguments

    `span: nafparserpy.layers.elements.Span`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Role(id: str, span: nafparserpy.layers.elements.Span, external_references: nafparserpy.layers.elements.ExternalReferences = <factory>, attrs: dict = <factory>)`
:   Represents a predicate argument

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('confidence' and 'status')

    `external_references: nafparserpy.layers.elements.ExternalReferences`
    :   optional external references

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

`Srl(items: List[nafparserpy.layers.srl.Predicate])`
:   SRL layer class

    ### Class variables

    `items: List[nafparserpy.layers.srl.Predicate]`
    :   list of predicates

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object