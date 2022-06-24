"""
Layer modules provide convenience classes for NAF layers and their elements.

The objects instantiated from these classes are decoupled from the NAF tree:
each class provides a factory method `object()` to create objects from nodes, and a method `node()` to
create nodes from objects.

## Class implementation
Classes are implemented as dataclasses with the following fields:

* compulsory attributes, e.g., 'id'
* compulsory elements, e.g., 'span'
* optional elements, e.g., 'externalReferences'
* optional attributes, e.g., 'status'; these default to None

## Naming

Naming follows the NAF element/attribute names as much as possible

* classes are named after their corresponding NAF element
* NAF element attributes appear as fields with the same name in the element class, with one
exception (because the attribute name is a python keyword):

    * 'from' attributes appear as fields named 'from_idref'

Some class fields do not directly correspond to a NAF element or attribute, but are
lists of NAF elements. These are named 'items' when they are elements of a container layer (`ExternalReferences` and
most NAF layers); otherwise they take the plural of the NAF element name, e.g., 'factVals' for a list of `FactVal`
objects.


## Class instantiation
Classes can be instantiated through their (dataclass) constructor. The constructor signature takes arguments in the
following order: compulsory attributes, compulsory subelements, optional subelements, optional attributes.

Additionally, some classes provide a higher-level `create` method. For instance, the `Entity` class `create` method
allows to create an entity from its id, type, and covered tokens/terms:
```
# create an Entity object with id='e1', type='PER' and covered elements 'w1' and 'w2'
e = Entity.create('e1', 'PER', ['w1', 'w2'])
```
Creating the same entity with the class constructor requires:
```
e = Entity('e1', Span([Target(i) for in ['w1', 'w2']]), type='PER'})
```
"""
