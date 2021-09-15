Module nafparserpy.layers.constituency
======================================

Classes
-------

`Constituency(items: List[nafparserpy.layers.constituency.Tree])`
:   Constituency layer class

    ### Class variables

    `items: List[nafparserpy.layers.constituency.Tree]`
    :   list of trees

    ### Static methods

    `object(node)`
    :   Create list of `Tree` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Edge(from_idref: str, to: str, attrs: dict = <factory>)`
:   Represents an edge

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('id' and 'head')

    `from_idref: str`
    :   id of 'from' node (note that the field name differs from the NAF attribute 'from')

    `to: str`
    :   id of 'to' node

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Nt(id: str, label: str)`
:   Represents a nonterminal

    ### Class variables

    `id: str`
    :

    `label: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`T(id: str, span: nafparserpy.layers.elements.Span)`
:   Represents a terminal

    ### Class variables

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

`Tree(nts: List[nafparserpy.layers.constituency.Nt], ts: List[nafparserpy.layers.constituency.T], edges: List[nafparserpy.layers.constituency.Edge])`
:   Represents a tree

    ### Class variables

    `edges: List[nafparserpy.layers.constituency.Edge]`
    :   edges

    `nts: List[nafparserpy.layers.constituency.Nt]`
    :   nonterminals

    `ts: List[nafparserpy.layers.constituency.T]`
    :   terminals

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object