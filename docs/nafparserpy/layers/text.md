Module nafparserpy.layers.text
==============================

Classes
-------

`Subtoken(text: str, id: str, offset: str, length: str)`
:   Represents a subtoken

    ### Class variables

    `id: str`
    :

    `length: str`
    :

    `offset: str`
    :

    `text: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Text(items: List[nafparserpy.layers.text.Wf])`
:   Text layer class

    ### Class variables

    `items: List[nafparserpy.layers.text.Wf]`
    :   list of word forms

    ### Static methods

    `object(node)`
    :   Create list of `Wf` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Wf(text: str, id: str, offset: str, length: str, subtokens: List[nafparserpy.layers.text.Subtoken] = <factory>, attrs: dict = <factory>)`
:   Represents a word's surface form

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('sent', 'para', 'page', 'xpath')

    `id: str`
    :

    `length: str`
    :

    `offset: str`
    :

    `subtokens: List[nafparserpy.layers.text.Subtoken]`
    :   optional list of subtokens

    `text: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object