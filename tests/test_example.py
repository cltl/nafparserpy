import os

from nafparserpy.layers.elements import Span
from nafparserpy.layers.entities import Entity, Entities
from nafparserpy.parser import NafParser

testfile = 'tests/data/coreference.naf'
out_file = 'tests/out/chomsky_colorless.naf'
os.makedirs('tests/out', exist_ok=True)


def test_coreference():

    naf = NafParser.load(testfile)

    # adding a layer
    e1 = Entity.create('e1', 'LOC', ['w10'])
    e2 = Entity.create('e2', 'PER', ['w12', 'w13'])

    entities = Entities([e1, e2])
    naf.add_layer('entities', entities)

    naf.add_layer_from_elements('entities', [e1, e2], exist_ok=True)

    assert naf.has_layer('entities')

    naf.add_linguistic_processor('entities', 'linguistic intuition', '1.0')

    assert len(naf.get_lps('entities')) == 1

    # modifying a layer
    coreferences = naf.get('coreferences')
    co1 = coreferences[0]
    co1.spans.append(Span.create(['t12', 't13']))
    naf.add_layer_from_elements('coreferences', [co1], exist_ok=True)
    naf.add_linguistic_processor('coreferences', 'linguistic intuition', '1.0')

    assert len(naf.get('coreferences')[0].spans) == 2


def test_newdocument():
    naf = NafParser(author='Noam Chomsky', filename='chomsky_colorless.naf')
    header = naf.get('nafHeader')
    assert header.fileDesc.filename is not None
    assert header.fileDesc.filename == 'chomsky_colorless.naf'

    assert header.fileDesc.author == 'Noam Chomsky'
    assert naf.get('fileDesc').author == 'Noam Chomsky'

    naf.add_raw_layer('colorless green ideas sleep furiously')
    naf.add_linguistic_processor('raw', 'linguistic intuition', '1.0')
    naf.add_linguistic_processor('raw', 'linguistic intuition', '1.1')
    assert len(naf.get_lps('raw')) == 2
    naf.add_linguistic_processor('raw', 'linguistic intuition', '1.0', replace=True)
    assert len(naf.get_lps('raw')) == 1

    naf.write(out_file)
    assert os.path.exists(out_file)
