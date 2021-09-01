from dataclasses import dataclass, field
from typing import List

from nafparserpy.layers.utils import IdrefGetter, create_node
from nafparserpy.layers.sublayers import Span, ExternalReferences


@dataclass
class Coref(IdrefGetter):
<<<<<<< HEAD
    """Coreference class

    Note that the implementation differs from the current DTD, and follows
    ```ELEMENT coref (span,externalReferences?)```
    rather than:
    ```ELEMENT coref (span|externalReferences)+```
    """
    id: str
    status: str
    span: Span      # the current DTD sees span as optional
    externalReferences: ExternalReferences = ExternalReferences([])   # the DTD is not clear about this
=======
    """Represents a coreference"""
    id: str
    status: str
    span: Span
    externalReferences: ExternalReferences = field(default_factory=ExternalReferences([]))
>>>>>>> wip
    type: str = None

    def node(self):
        attrs = {'id': self.id, 'status': self.status}
        if self.type is not None:
            attrs.update({'type': self.type})
        children = [self.span]
<<<<<<< HEAD
        if self.externalReferences.items:
            children.append(self.externalReferences)
=======
        if self.externalReferences is not None:
            children.append(self.externalReferences)

>>>>>>> wip
        return create_node('coref', None, children, attrs)

    @staticmethod
    def get_obj(node):
        return Coref(node.get('id'),
                     node.get('status'),
                     Span.get_obj(node.find('span')),
                     ExternalReferences(ExternalReferences.get_obj(node.find('externalReferences'))),
                     node.get('type'))


@dataclass
class Coreferences:
    items: List[Coref]

    def node(self):
        return create_node('coreferences', None, self.items, {})

    @staticmethod
    def get_obj(node):
        return [Coref.get_obj(n) for n in node]
