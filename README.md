*nafparserpy* is a lightweight python XML wrapper for [NAF](https://github.com/cltl/NAF-4-Development/). 

The parser follows on [KafNafParserPy](https://github.com/cltl/KafNafParserPy/tree/master/KafNafParserPy) by wrapping
[lxml](https://lxml.de/) to handle NAF XML trees, and providing convenience classes for handling NAF layers.
Unlike KafNafParserPy, layer objects are decoupled from the underlying lxml etree, so that the user is responsible for creating
and handling NAF objects, while the parser handles tree manipulation:
* the parser allows to add full NAF layer objects to the NAF tree. The user
  application is responsible for creating these objects; the parser recursively creates and adds nodes for the full layer.
* the parser creates layer objects when retrieving layers; these objects are decoupled from
  the lxml tree


## NAF version and DTD
The currently supported NAF version is [3.3](https://github.com/cltl/NAF-4-Development/blob/master/resources/dtd/naf_v3.3.dtd).
Layer and element classes follow closely the NAF DTD:

* compulsory NAF attributes appear as fields (object attributes)
* NAF subelements appear as fields of the corresponding class
* all attributes (compulsory and optional) appear in an `attrs` dict attribute

See [NAF-4-Development](https://github.com/cltl/NAF-4-Development/) for more information on NAF.



## Installation
*nafparserpy* is compatible with Python 3.7+ (for Python 3.6 you will need to install [dataclasses](https://pypi.org/project/dataclasses/)).

To install the parser, run:
```
pip install .
```

[USAGE](./USAGE.md) [API](https://cltl.github.io/nafparserpy/)