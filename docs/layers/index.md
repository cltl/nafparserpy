Module nafparserpy.layers
=========================
Layer modules provide convenience classes for NAF layers and their elements.

The objects instantiated from these classes are decoupled from the NAF tree:
each class provides a factory method to create objects from nodes, and a method to
create nodes from objects.

## Class implementation
Classes are implemented as dataclasses with the following fields:

* compulsory attributes, e.g., 'id'
* compulsory elements, e.g., 'span'
* optional elements, e.g., 'externalReferences'
* optional attributes; these are stored together with compulsory attributes in a dict field, 'attrs'

Classes that have both compulsory and optional attributes implement the `AttributeGetter` class, that provides
`has`/`get` methods to test attribute existence and retrieve them. Compulsory attributes are copied to the 'attrs' dict
field after class instantiation, to make these methods available for both compulsory and optional attributes.

## Naming

Naming follows the NAF element/attribute names as much as possible

* classes are named after their corresponding NAF element
* compulsory NAF element attributes appear as fields with the same name in the element class, with one
exception (because the attribute name is a python keyword):

    * 'from' attributes appear as fields named 'from_idref'

* optional elements appear as keys with the same name in the 'attrs' class field

Some class fields do not directly correspond to a NAF element or attribute, but are
lists of NAF elements. These are named 'items' when they are elements of a container layer (`ExternalReferences` and
most NAF layers); otherwise they take the plural of the NAF element name, e.g., 'factVals' for a list of `FactVal`
objects.

## Class instantiation
Classes can be instantiated through their (dataclass) constructor.
You should pass (in order): compulsory attributes, compulsory subelements (as objects),
optional subelements (as objects), optional attributes (as a dict).

Additionally, some classes provide a higher-level `create` method. For instance, the `Entity` class `create` method
allows to create an entity from its id, type, and covered tokens/terms:
```
# create an Entity object with id='e1', type='PER' and covered elements 'w1' and 'w2'
e = Entity.create('e1', 'PER', ['w1', 'w2'])
```
Creating the same entity with the class constructor requires:
```
e = Entity('e1', Span([Target(i) for in ['w1', 'w2']]), ExternalReferences([]), attrs={'type': 'PER'})
```

Sub-modules
-----------
* nafparserpy.layers.attribution
* nafparserpy.layers.causal_relations
* nafparserpy.layers.chunks
* nafparserpy.layers.constituency
* nafparserpy.layers.coreferences
* nafparserpy.layers.deps
* nafparserpy.layers.elements
* nafparserpy.layers.entities
* nafparserpy.layers.factualities
* nafparserpy.layers.locations_dates
* nafparserpy.layers.markables
* nafparserpy.layers.multiwords
* nafparserpy.layers.naf_header
* nafparserpy.layers.opinions
* nafparserpy.layers.raw
* nafparserpy.layers.srl
* nafparserpy.layers.temporal_relations
* nafparserpy.layers.terms
* nafparserpy.layers.text
* nafparserpy.layers.time_expressions
* nafparserpy.layers.topics
* nafparserpy.layers.tunits
* nafparserpy.layers.utils