import os

from lxml import etree

from nafparserpy.layers.entities import Entity
from nafparserpy.parser import NafParser

testfile = 'tests/data/coreference.naf'
out_file = 'tests/out/test.naf'
os.makedirs('tests/out', exist_ok=True)


def test_parse():
    naf = NafParser.load(testfile)
    for layer in ['nafHeader', 'raw', 'text', 'terms', 'coreferences']:
        assert naf.has_layer(layer)
    assert len(naf.get('nafHeader').linguisticProcessors) == 4
    assert not naf.get('public').has('filename')
    assert len(naf.get('text')) == 17
    assert len(naf.get('coreferences')) == 1
    coref0 = naf.get('coreferences')[0]
    assert coref0.spans[0].target_ids() == ['t7']
    coref = naf.get('coreferences')[0]
    coref.external_references
    ext_refs = coref.get_external_refs()
    assert len(ext_refs) == 1
    assert 'wikidata' in ext_refs[0]

    # no comments yet
    spans = naf.root.findall('.//span')
    assert all(x == 0 for x in [len([_ for _ in s.iter(tag=etree.Comment)]) for s in spans])
    naf.add_layer_from_elements('entities', [Entity.create('e0', 'PER', ['w1'])])
    # comments added together with layer
    assert all(x == 1 for x in [len([_ for _ in s.iter(tag=etree.Comment)]) for s in spans])
    naf.add_linguistic_processor('entities', 'test', '0.1', add_time_stamp=True)
    assert not naf.get('entities')[0].get_external_refs()

    timestamp = naf.get_lps('entities')[0].get('timestamp')
    assert timestamp

    entities = naf.get('entities')
    entities.append(Entity.create('e1', 'LOC', ['w2']))
    naf.add_linguistic_processor('entities', 'test', '0.2')
    assert len(naf.get_lps('entities')) == 2

    naf.write(out_file)

