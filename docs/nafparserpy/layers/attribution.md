Module nafparserpy.layers.attribution
=====================================

Classes
-------

`Attribution(items: List[nafparserpy.layers.attribution.Statement])`
:   Attribution-layer class

    ### Class variables

    `items: List[nafparserpy.layers.attribution.Statement]`
    :   list of attribution statements

    ### Static methods

    `object(node)`
    :   Create list of `Statement` objects from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`Statement(id: str, targets: List[nafparserpy.layers.attribution.StatementTarget], sources: List[nafparserpy.layers.attribution.StatementSource], cues: List[nafparserpy.layers.attribution.StatementCue])`
:   A statement has an id and one or more targets, sources or cues

    ### Class variables

    `cues: List[nafparserpy.layers.attribution.StatementCue]`
    :

    `id: str`
    :

    `sources: List[nafparserpy.layers.attribution.StatementSource]`
    :

    `targets: List[nafparserpy.layers.attribution.StatementTarget]`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `cue_spans(self)`
    :

    `node(self)`
    :   Create etree node from object

    `source_spans(self)`
    :

    `target_spans(self)`
    :

`StatementCue(span: nafparserpy.layers.elements.Span)`
:   StatementCue(span: nafparserpy.layers.elements.Span)

    ### Class variables

    `span: nafparserpy.layers.elements.Span`
    :   span covered by the statement cue

    ### Static methods

    `create(target_ids)`
    :

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`StatementSource(span: nafparserpy.layers.elements.Span)`
:   Represents the source of a statement

    ### Class variables

    `span: nafparserpy.layers.elements.Span`
    :   span covered by the statement source

    ### Static methods

    `create(target_ids)`
    :

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`StatementTarget(span: nafparserpy.layers.elements.Span)`
:   StatementTarget(span: nafparserpy.layers.elements.Span)

    ### Class variables

    `span: nafparserpy.layers.elements.Span`
    :   span covered by the statement target

    ### Static methods

    `create(target_ids)`
    :

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object