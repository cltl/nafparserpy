from nafparserpy.layers.utils import create_node
from nafparserpy.parser import NafParser


def test_add_etree_element():
    naf = NafParser.load('tests/data/coreference.naf')
    wfs = naf.get('text')
    naf2 = NafParser(filename='coreference_copy.naf')
    text_node = create_node('text')
    for wf in wfs:
        text_node.append(wf.node())
    naf2.add_layer('text', text_node, is_etree_element=True)
    assert len(wfs) == len(naf2.get('text'))
