import pytest

from nafparserpy.layers.attribution import Statement, StatementSource, StatementTarget, StatementCue
from nafparserpy.layers.causal_relations import CLink
from nafparserpy.layers.elements import Span, ExternalRef
from nafparserpy.layers.opinions import Opinion, OpinionExpression
from nafparserpy.layers.terms import Term
from nafparserpy.layers.time_expressions import Timex3
from nafparserpy.parser import NafParser
from nafparserpy.layers.topics import *
from nafparserpy.layers.text import *
import os

text = 'colorless green ideas sleep furiously'
text2 = 'said Noam Chomsky'
out_file = 'tests/out/test.naf'
os.makedirs('tests/out', exist_ok=True)
naf = NafParser()


def test_attribution():
    statement = Statement('s1',
                          [StatementTarget.create(['w1'])],
                          [StatementSource.create(['w2'])],
                          [StatementCue.create(['w3'])])
    assert statement.target_spans() == [['w1']]
    assert statement.source_spans() == [['w2']]
    assert statement.cue_spans() == [['w3']]
    statement = Statement.object(statement.node())
    assert statement.target_spans() == [['w1']]
    assert statement.source_spans() == [['w2']]
    assert statement.cue_spans() == [['w3']]


def test_causal_relations():
    clink = CLink('a', 'b', 'c')
    node = clink.node()
    assert 'relType' not in node.attrib.keys()
    assert not clink.has('relType')
    clink = CLink.object(node)
    assert not clink.has('relType')

    clink = CLink('a', 'b', 'c', {'relType': 'some'})
    node = clink.node()
    assert 'relType' in node.attrib.keys()
    assert clink.has('relType')
    clink = CLink.object(node)
    assert clink.has('relType')


def test_naf_header():
    naf.add_naf_header(fileDesc_attrs={'filename': 'test.naf'})
    assert naf.has_layer('nafHeader')
    naf.write(out_file)
    assert naf.has_layer('fileDesc')
    assert naf.get('fileDesc').get('filename') == 'test.naf'
    assert not naf.has_layer('linguisticProcessors')
    naf.add_linguistic_processor('raw', 'rawLp', '0.1')
    naf.write(out_file)
    assert naf.has_layer('linguisticProcessors')
    lp1 = naf.getall('linguisticProcessors')[0].lps[0]

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
    assert not topic2.has('confidence')
    naf.add_layer_from_elements('topics', [topic1, topic2])
    assert naf.get('topics') == [topic1, topic2]
    naf.write(out_file)


def test_text_layer():
    wf1 = Wf('colorless', 'w1', str(0), str(9), attrs={'sent': str(1)})
    naf.add_layer_from_elements('text', [wf1])
    assert naf.get('text')[0].get('id') == 'w1'


def test_term_layer():
    t1 = Term.create('t1', ['w1'], {'lemma': 'in', 'pos': 'ADP'})
    naf.add_layer_from_elements('terms', [t1])
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


def test_opinions():
    opinion = Opinion('o1', OpinionExpression(Span.create(['w1'])))
    assert opinion.target is None
    assert opinion.expression.span.target_ids() == ['w1']
    assert not opinion.expression.has('polarity')
    opinion = Opinion.object(opinion.node())
    assert opinion.target is None
    assert opinion.expression.span.target_ids() == ['w1']
    assert not opinion.expression.has('polarity')


def test_elements():
    extref = ExternalRef('ref1', externalRefs=[ExternalRef('ref2'), ExternalRef('ref3')])
    assert extref.reference == 'ref1'
    subrefs = [e.reference for e in extref.externalRefs]
    assert subrefs == ['ref2', 'ref3']

    extref == ExternalRef(extref.node())
    assert extref.reference == 'ref1'
    subrefs = [e.reference for e in extref.externalRefs]
    assert subrefs == ['ref2', 'ref3']


def test_timex():
    timex = Timex3('t1', 'DATE', Span.create(['w1']), {'value': '2016'})
    naf.add_layer_from_elements('timeExpressions', [timex])
    assert naf.get('timeExpressions')[0].type == 'DATE'
    assert naf.get('timeExpressions')[0].span.target_ids() == ['w1']
    assert naf.get('timeExpressions')[0].get('value') == '2016'
