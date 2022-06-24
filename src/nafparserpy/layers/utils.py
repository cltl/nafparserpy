from lxml import etree


class IdrefGetter:
    """Provides a target ids getter for layers with a `span` field"""
    def target_ids(self):
        """Return list of target ids covered by the layer's span"""
        if self.span is None:
            return []
        return [t.id for t in self.span.targets]


class ExternalReferenceHolder:
    """Provides add/get method for external references"""
    def add_external_ref(self, external_ref):
        self.external_references.items.append(external_ref)

    def get_external_refs(self):
        return [x.reference for x in self.external_references.items]


def create_node(layer, text=None, children=[], attributes={}, optional_attrs={}):
    """Create an etree Element node from the text, children and attributes of NAF objects

    Parameters
    ----------
    layer : str
        layer name
    text : str
        text of node
    children : list
        list of NAF objects to add as subelements in the node
    attributes : dict
        compulsory node attributes
    optional_attrs : dict
        optional node attributes
    """
    node = etree.Element(layer)
    if text is not None:
        node.text = etree.CDATA(text)
    for child in children:
        # create node for each child and append to node subelements
        node.append(child.node())
    for n, a in attributes.items():
        node.set(n, a)
    for n, a in optional_attrs.items():
        if a is not None:
            node.set(n, a)
    return node
