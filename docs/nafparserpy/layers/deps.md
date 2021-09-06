Module nafparserpy.layers.deps
==============================

Classes
-------

`Dep(from_idref: str, to: str, rfunc: str, attrs: dict = <factory>)`
:   Represents a Dependency

    ### Class variables

    `attrs: dict`
    :   optional attributes: 'case'

    `from_idref: str`
    :   id of 'from' node

    `rfunc: str`
    :   dependency relation

    `to: str`
    :   id of 'to' node

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Deps(items: List[nafparserpy.layers.deps.Dep])`
:   Deps (dependencies) layer class

    ### Class variables

    `items: List[nafparserpy.layers.deps.Dep]`
    :   list of dependencies

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object