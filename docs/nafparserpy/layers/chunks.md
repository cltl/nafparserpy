Module nafparserpy.layers.chunks
================================

Classes
-------

`Chunk(id: str, head: str, phrase: str, attrs: dict)`
:   Represents a chunk

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes: 'case'

    `head: str`
    :

    `id: str`
    :

    `phrase: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Chunks(items: List[nafparserpy.layers.chunks.Chunk])`
:   Chunks layer class

    ### Class variables

    `items: List[nafparserpy.layers.chunks.Chunk]`
    :

    ### Static methods

    `object(node)`
    :   Create list of `Chunk` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object