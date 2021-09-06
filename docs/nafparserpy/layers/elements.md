Module nafparserpy.layers.elements
==================================

Classes
-------

`Component(id: str, span: nafparserpy.layers.elements.Span, sentiment: nafparserpy.layers.elements.Sentiment = None, externalReferences: nafparserpy.layers.elements.ExternalReferences = ExternalReferences(items=[]), attrs: dict = <factory>)`
:   Represents a component

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter
    * nafparserpy.layers.utils.IdrefGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('type', 'lemma', 'pos', 'morphofeat', 'netype', 'case', 'head')

    `externalReferences: nafparserpy.layers.elements.ExternalReferences`
    :

    `id: str`
    :

    `sentiment: nafparserpy.layers.elements.Sentiment`
    :

    `span: nafparserpy.layers.elements.Span`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`ExternalRef(reference: str, sentiment: nafparserpy.layers.elements.Sentiment = None, externalRefs: List[Any] = <factory>, attrs: dict = <factory>)`
:   Represents an external reference

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `attrs: dict`
    :   optional attributes ('resource', 'reftype', 'status', 'source', 'confidence', 'timestamp')

    `externalRefs: List[Any]`
    :   list of ExternalRef objects (declared as Any because of circularity of definition)

    `reference: str`
    :

    `sentiment: nafparserpy.layers.elements.Sentiment`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

`ExternalReferences(items: List[nafparserpy.layers.elements.ExternalRef] = <factory>)`
:   ExternalReferences container

    ### Class variables

    `items: List[nafparserpy.layers.elements.ExternalRef]`
    :   optional list of external references

    ### Static methods

    `object(node)`
    :   Creates list of `ExternalRef` objects from node
        
        Parameters
        ----------
        node : etree
            node may be None as `ExternalReferences` elements are optional subelements

    ### Methods

    `node(self)`
    :   Create etree node from object

`Sentiment(layer: str, attrs: dict = <factory>)`
:   Represents a sentiment.
    
    Optional attributes are: 'resource', 'polarity', 'strength', 'subjectivity', 'sentiment_semantic_type',
    'sentiment_product_feature', 'sentiment_modifier', 'sentiment_marker'

    ### Ancestors (in MRO)

    * nafparserpy.layers.utils.AttributeLayer
    * nafparserpy.layers.utils.AttributeGetter

    ### Class variables

    `layer: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node
        
        Parameters
        ----------
        node : etree
            node may be None as `sentiment` elements are optional subelements

`Span(targets: List[nafparserpy.layers.elements.Target], attrs: dict = <factory>)`
:   Span(targets: List[nafparserpy.layers.elements.Target], attrs: dict = <factory>)

    ### Class variables

    `attrs: dict`
    :   optional attributes ('primary', 'status')

    `targets: List[nafparserpy.layers.elements.Target]`
    :

    ### Static methods

    `create(target_ids)`
    :

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object

    `target_ids(self)`
    :

`Target(id: str, attrs: dict = <factory>)`
:   Defines target id for the Span class

    ### Class variables

    `attrs: dict`
    :   optional attributes: 'head'

    `id: str`
    :

    ### Static methods

    `object(node)`
    :   Create object from etree node

    ### Methods

    `node(self)`
    :   Create etree node from object