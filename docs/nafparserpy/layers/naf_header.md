Module nafparserpy.layers.naf_header
====================================

Classes
-------

`FileDesc(layer: str, attrs: dict = <factory>)`
:   Represents a fileDesc element

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeLayer
    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `layer: str`
    :

`LP(name: str, version: str, lpDependencies: List[nafparserpy.layers.naf_header.LPDependency], attrs: dict = <factory>)`
:   Represents a linguistic processor

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('timestamp', 'beginTimestamp', 'endTimestamp', 'hostname')

    `lpDependencies: List[nafparserpy.layers.naf_header.LPDependency]`
    :

    `name: str`
    :

    `version: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`LPDependency(name: str, attrs: dict = <factory>)`
:   Represents a dependency (tool/model/data) of a linguistic processor

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('version', 'type')

    `name: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`LinguisticProcessors(layer_name: str, lps: List[nafparserpy.layers.naf_header.LP])`
:   Represents a linguisticProcessors element: the list of linguistic processors for a given layer.

    ### Class variables

    `layer_name: str`
    :

    `lps: List[nafparserpy.layers.naf_header.LP]`
    :   list of linguistic processors

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`NafHeader(fileDesc: nafparserpy.layers.utils.AttributeLayer, public: nafparserpy.layers.utils.AttributeLayer, linguisticProcessors: List[nafparserpy.layers.naf_header.LinguisticProcessors] = <factory>)`
:   NafHeader(fileDesc: nafparserpy.layers.utils.AttributeLayer, public: nafparserpy.layers.utils.AttributeLayer, linguisticProcessors: List[nafparserpy.layers.naf_header.LinguisticProcessors] = <factory>)

    ### Class variables

    `fileDesc: nafparserpy.layers.utils.AttributeLayer`
    :

    `linguisticProcessors: List[nafparserpy.layers.naf_header.LinguisticProcessors]`
    :

    `public: nafparserpy.layers.utils.AttributeLayer`
    :

    ### Static methods

    `create(filedesc_attr, public_attr, linguistic_processors)`
    :

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Public(layer: str, attrs: dict = <factory>)`
:   Represents a public element

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeLayer
    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `layer: str`
    :