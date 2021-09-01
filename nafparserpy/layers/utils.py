from dataclasses import dataclass, field

from lxml import etree


class AttributeGetter:
    """Provides an attribute getter"""
    def get(self, attribute):
        """Get attribute from `attrs` field"""
        return get_attribute(self, attribute)


def get_attribute(layer, key: str):
    """Return attribute value, or None if there is no such attribute.

    :param layer: the layer object carrying the attribute
    :param key: attribute name
    """
    if layer.attrs is not None and key in layer.attrs.keys():
        return layer.attrs[key]
    else:
        return None


class IdrefGetter:
    """Provides a target ids getter for layers with a `span` field"""
    def target_ids(self):
        """Returns list of target ids covered by the layer's span"""
        return get_span_target_ids(self)


def get_span_target_ids(layer):
    """Return the list of target ids covered by the span of a layer.

    Defaults to empty list, also if span is missing.
    :param layer: the layer object"""
    if layer.span is None:
        return []
    return [t.id for t in layer.span.targets]


@dataclass
class AttributeLayer(AttributeGetter):
    """A layer containing only attributes"""
    layer: str
    attrs: dict = field(default_factory=dict)

    def node(self):
        return create_node(self.layer, None, [], self.attrs)

    @staticmethod
    def get_obj(layer_name, node):
        return AttributeLayer(layer_name, node.attrib)


def create_node(layer, text, children, attributes):
    """Create an etree Element node from NAF objects

    :param layer:layer name
    :param text: text of node
    :param children: list of NAF objects to add as subelements in the node
    :param attributes: node attributes (whether compulsory or optional)
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
