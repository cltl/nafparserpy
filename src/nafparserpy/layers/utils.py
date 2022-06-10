from dataclasses import dataclass, field

from lxml import etree


class AttributeGetter:
    """Provides an attribute getter"""
    def get(self, attribute):
        """Get attribute from `attrs` field

        Parameters
        ----------
        attribute : str
            attribute name

        Raises
        ------
        KeyError: if the layer has no such attribute"""
        if self.has(attribute):
            return self.attrs[attribute]
        else:
            raise KeyError('Attribute {} is not present in layer:\n{}'.format(attribute, self))

    def has(self, attribute):
        """Test if attribute appears in `attrs` field"""
        return self.attrs is not None and attribute in self.attrs.keys()


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


@dataclass
class AttributeLayer(AttributeGetter):
    """A layer containing only attributes"""
    layer: str
    attrs: dict = field(default_factory=dict)
    """optional attributes (keys are subclass dependent)"""

    def node(self):
        """Create etree node from object"""
        return create_node(self.layer, None, [], self.attrs)

    @staticmethod
    def object(layer_name, node):
        """Create object from etree node"""
        return AttributeLayer(layer_name, node.attrib)

    def is_none(self):
        return not self.attrs


def create_node(layer, text, children, attributes):
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
        node attributes (whether compulsory or optional)
    """
    node = etree.Element(layer)
    if text is not None:
        node.text = etree.CDATA(text)
    for child in children:
        # create node for each child and append to node subelements
        node.append(child.node())
    for k, v in attributes.items():
        node.set(k, v)
    return node
