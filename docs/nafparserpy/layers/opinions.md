Module nafparserpy.layers.opinions
==================================

Classes
-------

`Opinion(id: str, expression: nafparserpy.layers.opinions.OpinionExpression, holder: nafparserpy.layers.opinions.OpinionHolder = None, target: nafparserpy.layers.opinions.OpinionTarget = None)`
:   Represents an opinion

    ### Class variables

    `expression: nafparserpy.layers.opinions.OpinionExpression`
    :

    `holder: nafparserpy.layers.opinions.OpinionHolder`
    :

    `id: str`
    :

    `target: nafparserpy.layers.opinions.OpinionTarget`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`OpinionExpression(span: nafparserpy.layers.elements.Span, attrs: dict = <factory>)`
:   Represents an opinion expression
    
    Optional attributes: 'polarity', 'strength', 'subjectivity', 'sentiment_semantic_type', 'sentiment_product_feature'

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   list of optional attributes (subclass dependent)

    `span: nafparserpy.layers.elements.Span`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`OpinionHolder(span: nafparserpy.layers.elements.Span, attrs: dict = <factory>)`
:   Represents an opinion holder
    
    Optional attributes: 'type'

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   list of optional attributes (subclass dependent)

    `span: nafparserpy.layers.elements.Span`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`OpinionTarget(span: nafparserpy.layers.elements.Span, attrs: dict = <factory>)`
:   Represents an opinion target
    
    Optional attributes: 'type'

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   list of optional attributes (subclass dependent)

    `span: nafparserpy.layers.elements.Span`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Opinions(items: List[nafparserpy.layers.opinions.Opinion])`
:   Opinions layer class

    ### Class variables

    `items: List[nafparserpy.layers.opinions.Opinion]`
    :   list of opinions

    ### Static methods

    `object(node)`
    :   Create list of `Opinion` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object