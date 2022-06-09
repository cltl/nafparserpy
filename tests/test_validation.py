from nafparserpy.parser import NafParser


def test_validation():
    naf = NafParser.load('tests/data/lpdep.naf', validate_against_dtd=True)
    assert naf
