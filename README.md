*nafparserpy* is a python [NAF](https://github.com/newsreader/NAF) parser that follows on
[KafNafParserPy](https://github.com/cltl/KafNafParserPy/tree/master/KafNafParserPy).

## Introduction
Like KafNafParserPy, the parser wraps [lxml](https://lxml.de/) to handle NAF XML trees, and
provides convenience classes for handling NAF layers.
Compared to KafNafParserPy, layer objects are decoupled from the underlying lxml etree, allowing for a clear separation
between object and tree manipulation.

*nafparserpy* is compatible with Python 3.7 (for Python 3.6 you
will need to install [dataclasses](https://pypi.org/project/dataclasses/)).

See the [pages](https://cltl.github.io/nafparserpy/) for the documentation.

### NAF version and DTD
The currently supported NAF version is [3.3.a](naf_v3.3.a.dtd).

See [naf_development_doc](naf_development_doc) for changes with regard to NAF 3.2


### NAF tree handling and layer objects
*nafparserpy* is restrictive when it comes to tree manipulation:

* the parser allows to add full NAF layer objects to the NAF tree (`linguisticProcessors` excepted). The user
application is responsible for creating these objects; the parser recursively creates and adds nodes for the full layer.
* the parser creates layer objects when retrieving layers; these objects are decoupled from
the lxml tree

Layer and element classes follow closely the NAF DTD:

* compulsory NAF attributes appear as fields (object attributes)
* NAF subelements appear as fields of the corresponding class
* all attributes (compulsory and optional) appear in an `attrs` dict attribute


## Installation
To install the parser, run:
```
pip install .
```

## Example


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
Like `entities` and most NAF layers, the `coreferences` is a container element; we can index it to retrieve its `Coref` 
elements:  
```python
co1 = coreferences[0]
```
`Coref` objects have a `spans` attribute listing their `span` subelements.
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

Let us record this NAF document and write it to file:
```
os.makedirs('tests/out', exist_ok=True)
naf.write('tests/out/chomsky_colorless.naf')
```

To write to stdout:
```
> naf.write()
<?xml version='1.0' encoding='UTF-8'?>
<NAF xml:lang="en" version="3.3.a">
  <nafHeader>
    <fileDesc author="Noam Chomsky" filename="chomsky_colorless.naf"/>
    <linguisticProcessors layer="raw">
      <lp name="linguistic intuition" version="1.0"/>
    </linguisticProcessors>
  </nafHeader>
  <raw><![CDATA[colorless green ideas sleep furiously]]></raw>
</NAF>
```

### More examples
See the [test modules](tests) for more examples
