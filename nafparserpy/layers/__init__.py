"""
Layer modules provide convenience classes for NAF elements.
The objects instantiated from these classes are decoupled from the NAF tree:
each class provides a factory method to create objects from nodes, and a method to
create nodes from objects.

## Class implementation
Classes are implemented as dataclasses with the following fields:

* compulsory attributes, e.g., 'id'
* compulsory elements, e.g., 'span'
* optional elements, e.g., 'externalReferences' with default value
* optional attributes; these appear together in a dict field, 'attrs'

## Naming

Naming follows the NAF element/attribute names as much as possible
* Classes are named after their corresponding NAF element
* compulsory NAF element attributes appear as fields with the same name in the element class. Exceptions to this are:
* optional elements appear as keys with the same name in the 'attrs' class field

Some class fields do not directly correspond to a NAF element or attribute, but are
list of NAF elements. These are named 'items' when they are the sole NAF subelements in a given layer; otherwise they
take the plural of the NAF element name, e.g., 'factVals' for a list of FactVal objects.

#### Exceptions
* NAF attribute names which collide with python:

    * 'from' appears as a field named 'from_idref'


## Class instantiation
Classes can be instantiated through their (dataclass) constructor.
You should pass (in order): compulsory attributes, compulsory subelements (as objects),
optional subelements (as objects), optional attributes (as a dict)

Additionally, some classes provide a higher-level `create` method. For instance, the `Entity` class `create` method
allows to create an entity from its id, type, and covered tokens/terms:
```
# create an Entity object with id='e1', type='PER' and covered elements 'w1' and 'w2'
e = Entity.create('e1', 'PER', ['w1', 'w2'])
```
Creating the same entity with the class constructor takes:
```
e = Entity('e1', Span([Target(i) for in ['w1', 'w2']]), attrs={'type': 'PER'})
```

"""