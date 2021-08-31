`nafparserpy` is a simple [NAF](https://github.com/newsreader/NAF) parser, that follows on
[KafNafParserPy](https://github.com/cltl/KafNafParserPy/tree/master/KafNafParserPy).

Like KafNafParserPy, the parser wraps [lxml](https://lxml.de/) to handle NAF XML trees, and
provides convenience classes for handling NAF layers. `nafparserpy` is implemented in python 3.7,
and should be compatible with Python 3.6+. The currently supported NAF version is 3.2.


## Naf tree handling
Compared to KafNafParserPy, `nafparserpy` is restrictive when it comes to tree manipulation:

* the parser only creates layer objects when retrieving layers, but the created objects are decoupled from
the lxml tree
* the parser only allows the addition to the NAF tree of full NAF layers (`linguisticProcessors` excepted).

The recommended workflow to modify a given layer consists in:

 * [retrieving the given layer](#retrieving_layers)
 * [modifying the object(s) in that layer](#modifying_objects)
 * [replacing the layer](#replacing_layers)


#### Retrieving layers
The parser allows to retrieve layers from the NAF tree as layer objects.

#### Modifying objects
Attributes and subelements are represented as fields in layer objects. NAF
attributes are stored as a dictionary in an `attrs` field; besides, compulsory attributes
have their own field.

Objects are created by specifying their compusory attributes, subelements (as objects of the corresponding class),
and a dictionary of optional attributes.

#### Replacing layers
The parser allows to add new layers, and to control for destructive replacement


## DTD
The parser implementation follows the
[NAF v3.2 DTD](https://github.com/cltl/NAF-4-Development/blob/master/res/naf_development/naf_v3.2.dtd),
with a few differences:

* `factualityValue` is not implemented, since it is marked as old in the DTD
* some layer classes are more strict than the DTD in their sublayer declarations. For instance, the
`Entity` class implements `ELEMENT entity (span,externalReferences?)` instead of
`ELEMENT entity (span|externalReferences)+`


