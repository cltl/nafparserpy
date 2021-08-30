# NafParserPy
NafParserPy is a parser for [NAF]() in python that follows on [KafNafParserPy]().
Compared to KafNafParserPy, NafParserPy:
* only supports NAF (KafNafParserPy also supports KAF)
* supports NAF 3.1+ (KafNafParserPy supports NAF 3.0; NafParserPy was developed to support the extension of NAF elements 
from v3.1 onwards)
* is not compatible with Python 2 (the parser is written in Python 3.7)

Like KafNafParserPy, the parser is built around [lxml]() and offers convenience objects for 
creation and access of NAF layers. The parser was designed with the following guidelines:
* the parser is not intended for extensive manipulation of NAF objects, which is left to user applications.
With a few exceptions, like the addition of linguistic processors, layer objects have to be created as a block before 
adding to the NAF tree (objects are created when accessing the tree, so that changes made to them are not transferred
to the tree). 
 Modifications to existing layers should then be performed in the user application; the modified layers can then 
 replace existing layers in the tree (the user has control over layer addition and replacement).
* convenience objects follow on the NAF DTD but stay close to the xml tree structure: 
    * required attributes must be declared when instantiating objects (and are implemented as object fields) 
    * optional attributes are passed on as a dictionary

