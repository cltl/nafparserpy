# nafparserpy
*nafparserpy* is a lightweight python XML wrapper for [NAF](https://github.com/cltl/NAF-4-Development/). 

The parser wraps [lxml](https://lxml.de/) to handle NAF trees, providing convenience classes for NAF layers and elements. 
The resulting objects are decoupled from the underlying `lxml` tree: the user is responsible for creating
and handling NAF objects, while the parser handles tree manipulation.

## NAF version and DTD
The currently supported NAF version is [3.3](https://github.com/cltl/NAF-4-Development/blob/master/resources/dtd/naf_v3.3.dtd).
Layer and element classes follow closely the NAF DTD:

* compulsory NAF attributes appear as fields (object attributes)
* NAF subelements appear as fields of the corresponding class
* all attributes (compulsory and optional) appear in an `attrs` dict attribute

See [NAF-4-Development](https://github.com/cltl/NAF-4-Development/) for more information on NAF.

## Background
`nafparserpy` follows on [KafNafParserPy](https://github.com/cltl/KafNafParserPy/tree/master/KafNafParserPy) by wrapping
[lxml](https://lxml.de/) to handle NAF XML trees, and providing convenience classes for handling NAF layers.
Unlike KafNafParserPy, layer objects are decoupled from the underlying lxml etree, so that the user is responsible for creating
and handling NAF objects, while the parser handles tree manipulation:

* the parser allows to add full NAF layer objects to the NAF tree. The user
  application is responsible for creating these objects; the parser recursively creates and adds nodes for the full layer.
* the parser creates layer objects when retrieving layers; these objects are decoupled from
  the lxml tree

## Example usage
The following examples illustrate basic features of the parser. 
See the [test modules](../tests) for more examples.

### Adding and modifying layers

In this example we will look at the file `tests/data/coreference.naf` and

* add an `entities` layer to the tree
* modify the `coreferences` layer by adding a new span to the 'co1' `coref` element

We will start by loading the NAF document:
```python
naf = NafParser.load('tests/data/coreference.naf')
```

#### Adding layers

We want to add two entities, for the location *USA* and the person *Kitty Genovese*.

The `Entity` class provides a factory method to create entities from their id, type and target ids:

```python
e1 = Entity.create('e1', 'LOC', ['w10'])
e2 = Entity.create('e2', 'PER', ['w12', 'w13'])
```

Now create the `entities` layer and add it to the tree:
```python
entities = Entities([e1, e2])
naf.add_layer('entities', entities)
```
Alternatively, and because the `entities` layer is a container layer, it can be created directly from its elements list:
```python
naf.add_layer_from_elements('entities', [e1, e2])
```

To verify that the layer has been added:
```python
> naf.has_layer('entities')
True
```

We should also add a linguistic processor to the NAF header to explain how we came about these entities:
Our linguistic processor is called 'linguistic intuition', version 1.0:

```python
naf.add_linguistic_processor('entities', 'linguistic intuition', '1.0')
```
We could also have passed tool/data dependencies to this processor, and optional attributes like a timestamp.

The NAF header now holds one linguistic processor for the `entities` layer:
```python
> len(naf.get_lps('entities'))
1
```

#### Modifying layers

The `coreferences` layer links the term 'murder' to the event *murder of Kitty Genovese*.
We will add 'Kitty Genovese' as corefering to the event.

Retrieve the `coreferences` layer:
```python
coreferences = naf.get('coreferences')
```
Like `entities` and most NAF layers, the `coreferences` layer is a container element; we can index it to retrieve its `Coref`
elements:
```python
co1 = coreferences[0]
```
NAF `coref` elements take one or more `span` children and optionally an `externalReferences` element. They are mapped to
`Coref` objects, which have a `spans` attribute listing their `Span` subelements, and a possibly `ExternalReferences` attribute.
Let us add a span over the terms 't12' and 't13':
```python
co1.spans.append(Span.create(['t12', 't13']))
```
NAF objects are decoupled from the tree, we need now to replace the existing `coreferences` layer with a new one
constructed from our modified 'co1' `coref`. We will simply create a new layer object from its elements, and
allow it to replace the existing layer:
```python
naf.add_layer_from_elements('coreferences', [co1], exist_ok=True)
```

Let us add a linguistic processor to record this modification

```python
naf.add_linguistic_processor('coreferences', 'linguistic intuition', '1.0')
```

We now have 2 spans in the first `coref` element in the `coreferences` layer:
```python
> len(naf.get('coreferences')[0].spans)
2
```


### Adding covered text as comments
The parser is set to add the covered text of span elements as comments to span nodes.
To disable this, one can set the `decorate` flag of the constructor to `False`:
```python
NafParser.load(file, decorate=False)
``` 
or
```python
naf = NafParser(tree, decorate=False)
```
Note however that comments coming from an input file/tree are preserved.

### Creating a NAF document from scratch
What if you have no NAF document yet, only text?
We will create a NAF document, with the text "Colorless green ideas sleep furiously". The author is Noam Chomsky,
and we will call this document 'chomsky_colorless.naf'.

Initiate a NAF document:
```python
naf = NafParser(author='Noam Chomsky', filename='chomsky_colorless.naf')
```

Author name and filename are `fileDesc` attributes. Let us verify that they are now in the NAF header:
```python
header = naf.get('nafHeader')
> header.fileDesc.has('author')
True
> header.fileDesc.get('author')
Noam Chomsky
> header.fileDesc.has('filename')
True
> header.fileDesc.get('filename')
chomsky_colorless.naf
```
Alternatively, and because `fileDesc` is the only element of its kind in NAF documents, we can directly retrieve it:
```python
> naf.get('fileDesc').get('author')
Noam Chomsky
```

Now we can add a raw text layer:
```python
naf.add_raw_layer('colorless green ideas sleep furiously')
```

Add the corresponding linguistic processor:

```python
naf.add_linguistic_processor('raw', 'linguistic intuition', '1.0')
```

By default, the parser is set to keep previously defined linguistic processors for a given layer, so that each layer can have  
several `lp` elements attached to it. To disable this and keep a single `lp` per layer, use the `replace` flag:

```python
naf.add_linguistic_processor('raw', 'linguistic intuition', '1.0', replace=True)
```

Let us record this NAF document and write it to file:
```
os.makedirs('tests/out', exist_ok=True)
naf.write('tests/out/chomsky_colorless.naf')
```

To write to stdout:
```
> naf.write()
<?xml version='1.0' encoding='UTF-8'?>
<NAF xml:lang="en" version="3.3">
  <nafHeader>
    <fileDesc author="Noam Chomsky" filename="chomsky_colorless.naf"/>
    <linguisticProcessors layer="raw">
      <lp name="linguistic intuition" version="1.0"/>
    </linguisticProcessors>
  </nafHeader>
  <raw><![CDATA[colorless green ideas sleep furiously]]></raw>
</NAF>
```

