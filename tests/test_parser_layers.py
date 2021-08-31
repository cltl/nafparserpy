import pytest

from nafparserpy.layers.terms import Term
from nafparserpy.parser import NafParser
from nafparserpy.layers.topics import *
from nafparserpy.layers.text import *
import os
text = 'colorless green ideas sleep furiously'
text2 = 'said Noam Chomsky'

naf = NafParser()


def test_naf_header():
    naf.add_naf_header(fileDesc_attrs={'filename': 'test.naf'})
    assert naf.has_layer('nafHeader')
    os.makedirs('tests/out', exist_ok=True)
    naf.write('tests/out/test.naf')
    assert naf.has_layer('fileDesc')
    assert naf.get('fileDesc').get('filename') == 'test.naf'
    assert not naf.has_layer('linguisticProcessors')
    naf.add_linguistic_processor('raw', 'rawLp', '0.1')
    naf.write('tests/out/test.naf')
    assert naf.has_layer('linguisticProcessors')
    lp1 = naf.getall('linguisticProcessors')[0].items[0]
    # NOTE compulsory attributes appear both as fields and attributes
    assert lp1.name == 'rawLp'
    assert lp1.get('name') == 'rawLp'
    assert naf.get('nafHeader') is not None


def test_raw_layer():
    assert not naf.has_layer('raw')
    naf.add_raw_layer(text)
    assert naf.has_layer('raw')
    assert naf.get('raw').text == text
    with pytest.raises(ValueError):
        naf.add_raw_layer(text2)
    naf.add_raw_layer(text2, exist_ok=True)
    assert naf.get('raw').text == text2


def test_topics_layer():
    topic1 = Topic(text, {'source': 'unk', 'method': 'unk', 'uri': 'unk', 'confidence': '0'})
    assert topic1.get('confidence') == '0'
    topic2 = Topic(text2)
    assert topic2.get('confidence') is None
    naf.add_container_layer('topics', [topic1, topic2])
    assert naf.get('topics') == [topic1, topic2]
    os.makedirs('tests/out', exist_ok=True)
    naf.write('tests/out/test.naf')


def test_text_layer():
    wf1 = Wf('colorless', 'w1', str(0), str(9), {'sent': str(1)})
    naf.add_container_layer('text', [wf1])
    assert naf.get('text')[0].get('id') == 'w1'


def test_term_layer():
    t1 = Term.create('t1', {'lemma': 'in', 'pos': 'ADP'}, ['w1'])
    naf.add_container_layer('terms', [t1])
    terms = naf.get('terms')
    assert len(terms) == 1
    term = terms[0]
    assert term.span is not None
    targets = term.span.targets
    assert len(targets) == 1
    target = targets[0]
    assert target.id == 'w1'
    assert naf.get('terms')[0].span.targets[0].id == 'w1'
    assert naf.get('terms')[0].target_ids() == ['w1']

