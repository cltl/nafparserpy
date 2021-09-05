from nafparserpy.parser import NafParser

testfile = 'tests/data/coreference.naf'


def test_parse():
    naf = NafParser.load(testfile)
    for layer in ['nafHeader', 'raw', 'text', 'terms', 'coreferences']:
        assert naf.has_layer(layer)
    assert len(naf.get('nafHeader').linguisticProcessors) == 4
    assert not naf.get('public').has('filename')
    assert len(naf.get('text')) == 17
    assert len(naf.get('coreferences')) == 1
    assert naf.get('coreferences')[0].target_ids() == [['t7']]
    coref = naf.get('coreferences')[0]
    ext_ref = naf.get('coreferences')[0].externalReferences.items[0]
    assert 'wikidata' in ext_ref.reference 

