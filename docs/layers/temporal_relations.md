Module nafparserpy.layers.temporal_relations
============================================

Classes
-------

`PredicateAnchor(spans: List[nafparserpy.layers.elements.Span], attrs: dict = <factory>)`
:   PredicateAnchor(spans: List[nafparserpy.layers.elements.Span], attrs: dict = <factory>)

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('id', 'anchorTime', 'beginPoint', 'endPoint')

    `spans: List[nafparserpy.layers.elements.Span]`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`TLink(id: str, from_idref: str, fromType: str, to: str, toType: str, reTlype: str)`
:   Represents a temporal link

    ### Class variables

    `fromType: str`
    :

    `from_idref: str`
    :   represents the 'from' NAF attribute

    `id: str`
    :

    `reTlype: str`
    :

    `to: str`
    :

    `toType: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`TemporalRelations(tlinks: List[nafparserpy.layers.temporal_relations.TLink] = <factory>, predicate_anchors: List[nafparserpy.layers.temporal_relations.PredicateAnchor] = <factory>)`
:   Temporal Relations layer class
    
    TODO check the specification (is the DTD too liberal?)

    ### Class variables

    `predicate_anchors: List[nafparserpy.layers.temporal_relations.PredicateAnchor]`
    :

    `tlinks: List[nafparserpy.layers.temporal_relations.TLink]`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object