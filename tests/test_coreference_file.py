import pytest

from nafparserpy.parser import NafParser

testfile = 'tests/data/coreference.naf'


def test_parse():
    naf = NafParser.parse(testfile)
    for layer in ['nafHeader', 'raw', 'text', 'terms', 'coreferences']:
        assert naf.has_layer(layer)
    assert len(naf.get('nafHeader').linguisticProcessors) == 4
    assert naf.get('nafHeader').public.get('filename') is None
    assert len(naf.get('text')) == 17
    assert len(naf.get('coreferences')) == 1
    assert naf.get('coreferences')[0].target_ids() == ['t7']
    coref = naf.get('coreferences')[0]
    ext_ref = naf.get('coreferences')[0].externalReferences[0]
    assert 'wikidata' in ext_ref.get('reference')

