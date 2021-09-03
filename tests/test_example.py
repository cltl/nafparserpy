import os

from nafparserpy.layers.elements import Span
from nafparserpy.layers.entities import Entity, Entities
from nafparserpy.parser import NafParser


def test_coreference():

    naf = NafParser.load('tests/data/coreference.naf')

    # adding a layer
    e1 = Entity.create('e1', 'LOC', ['w10'])
    e2 = Entity.create('e2', 'PER', ['w12', 'w13'])

    entities = Entities([e1, e2])
    naf.add_layer('entities', entities)

    naf.add_layer_from_elements('entities', [e1, e2], exist_ok=True)

    assert naf.has_layer('entities')

    naf.add_linguistic_processor('entities', 'linguistic intuition', '1.0')

    assert len(naf.get('nafHeader').get_lps('entities')) == 1

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
    assert header.fileDesc.get('filename') == 'chomsky_colorless.naf'

    assert header.fileDesc.get('author') == 'Noam Chomsky'
    assert naf.get('fileDesc').get('author') == 'Noam Chomsky'

    naf.add_raw_layer('colorless green ideas sleep furiously')
    naf.add_linguistic_processor('raw', 'linguistic intuition', '1.0')

    naf.write('tests/chomsky_colorless.naf')
    assert os.path.exists('tests/chomsky_colorless.naf')
