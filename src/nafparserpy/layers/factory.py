from nafparserpy.layers.attribution import Attribution
from nafparserpy.layers.causal_relations import CausalRelations
from nafparserpy.layers.chunks import Chunks
from nafparserpy.layers.constituency import Constituency
from nafparserpy.layers.coreferences import Coreferences
from nafparserpy.layers.deps import Deps
from nafparserpy.layers.entities import Entities
from nafparserpy.layers.factualities import Factualities
from nafparserpy.layers.locations_dates import Locations, Dates
from nafparserpy.layers.markables import Markables
from nafparserpy.layers.multiwords import Multiwords
from nafparserpy.layers.naf_header import NafHeader, FileDesc, Public, LinguisticProcessors, LP
from nafparserpy.layers.opinions import Opinions
from nafparserpy.layers.raw import Raw
from nafparserpy.layers.srl import Srl
from nafparserpy.layers.temporal_relations import TemporalRelations
from nafparserpy.layers.terms import Terms
from nafparserpy.layers.text import Text
from nafparserpy.layers.time_expressions import TimeExpressions
from nafparserpy.layers.topics import Topics
from nafparserpy.layers.tunits import Tunits

create_from_node = {
    'nafHeader': lambda n: NafHeader.object(n),
    'fileDesc': lambda n: FileDesc.object(n),
    'public': lambda n: Public.object(n),
    'linguisticProcessors': lambda n: LinguisticProcessors.object(n),
    'lp': lambda n: LP.object(n),
    'raw': lambda n: Raw.object(n),
    'topics': lambda n: Topics.object(n),
    'text': lambda n: Text.object(n),
    'terms': lambda n: Terms.object(n),
    'chunks': lambda n: Chunks.object(n),
    'multiwords': lambda n: Multiwords.object(n),
    'deps': lambda n: Deps.object(n),
    'constituency': lambda n: Constituency.object(n),
    'coreferences': lambda n: Coreferences.object(n),
    'srl': lambda n: Srl.object(n),
    'opinions': lambda n: Opinions.object(n),
    'timeExpressions': lambda n: TimeExpressions.object(n),
    'tunits': lambda n: Tunits.object(n),
    'locations': lambda n: Locations.object(n),
    'dates': lambda n: Dates.object(n),
    'temporalRelations': lambda n: TemporalRelations.object(n),
    'entities': lambda n: Entities.object(n),
    'causalRelations': lambda n: CausalRelations.object(n),
    'markables': lambda n: Markables.object(n),
    'attribution': lambda n: Attribution.object(n),
    'factualities': lambda n: Factualities.object(n)
}
"""mapping of layer name to class object creation method"""

create_from_elements = {
    'topics': lambda elts: Topics(elts),
    'text': lambda elts: Text(elts),
    'terms': lambda elts: Terms(elts),
    'chunks': lambda elts: Chunks(elts),
    'multiwords': lambda elts: Multiwords(elts),
    'deps': lambda elts: Deps(elts),
    'constituency': lambda elts: Constituency(elts),
    'coreferences': lambda elts: Coreferences(elts),
    'srl': lambda elts: Srl(elts),
    'opinions': lambda elts: Opinions(elts),
    'timeExpressions': lambda elts: TimeExpressions(elts),
    'tunits': lambda elts: Tunits(elts),
    'entities': lambda elts: Entities(elts),
    'causalRelations': lambda elts: CausalRelations(elts),
    'markables': lambda elts: Markables(elts),
    'attribution': lambda elts: Attribution(elts),
    'factualities': lambda elts: Factualities(elts)
}
"""mapping of layer name to class constructor for container classes"""
