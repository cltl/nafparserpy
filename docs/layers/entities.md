Module nafparserpy.layers.entities
==================================

Classes
-------

`Entities(items: List[nafparserpy.layers.entities.Entity])`
:   Entities layer class

    ### Class variables

    `items: List[nafparserpy.layers.entities.Entity]`
    :   list of entities in the layer

    ### Static methods

    `object(node)`
    :   Create list of `Entity` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Entity(id: str, span: nafparserpy.layers.elements.Span, external_references: nafparserpy.layers.elements.ExternalReferences = <factory>, attrs: dict = <factory>)`
:   Represents a named entity

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter
    * nafparserpy.layers.utils.IdrefGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('type', 'status', 'source')

    `external_references: nafparserpy.layers.elements.ExternalReferences`
    :   An optional list of external references

    `id: str`
    :   Entity id

    `span: nafparserpy.layers.elements.Span`
    :   Span of idrefs covered by the entity

    ### Static methods

    `create(entity_id, entity_type, target_ids)`
    :

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object