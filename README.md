*nafparserpy* is a lightweight python XML wrapper for [NAF](https://github.com/cltl/NAF-4-Development/). 

The parser wraps [lxml](https://lxml.de/) to handle NAF trees, providing convenience classes for NAF layers and elements. 
The resulting objects are decoupled from the underlying `lxml` tree: the user is responsible for creating
and handling NAF objects, while the parser handles tree manipulation.

To install the parser, run:
```
pip install nafparserpy
```

[USAGE](https://cltl.github.io/nafparserpy/) 