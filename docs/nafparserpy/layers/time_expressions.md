Module nafparserpy.layers.time_expressions
==========================================

Classes
-------

`TimeExpressions(items: List[nafparserpy.layers.time_expressions.Timex3] = <factory>)`
:   TimeExpressions layer class

    ### Class variables

    `items: List[nafparserpy.layers.time_expressions.Timex3]`
    :   list of time expressions

    ### Static methods

    `object(node)`
    :   Create list of `Timex3` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Timex3(id: str, type: str, spans: List[nafparserpy.layers.elements.Span] = <factory>, attrs: dict = <factory>)`
:   Represents a time expression
    
    TODO verify element specification in DTD for spans

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('beginPoint', 'endPoint', 'quant', 'freq', 'functionInDocument', 'temporalFunction',
        'value', 'valueFromFunction', 'mod', 'anchorTimeID')

    `id: str`
    :

    `spans: List[nafparserpy.layers.elements.Span]`
    :   optional list of spans

    `type: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object