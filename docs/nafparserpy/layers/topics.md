Module nafparserpy.layers.topics
================================

Classes
-------

`Topic(text: str, attrs: dict = <factory>)`
:   Represents a topic

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('source', 'method', 'confidence', 'uri')

    `text: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Topics(items: List[nafparserpy.layers.topics.Topic])`
:   Topics layer class

    ### Class variables

    `items: List[nafparserpy.layers.topics.Topic]`
    :   list of topics

    ### Static methods

    `object(node)`
    :   Create list of `Topic` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object