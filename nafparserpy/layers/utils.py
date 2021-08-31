from dataclasses import dataclass, field

from lxml import etree


class AttributeGetter:
    """provides an attribute getter"""
    def get(self, attribute):
        return get_attribute(self, attribute)


class IdrefGetter:
    """provides a target ids getter for layers with a U{Span} field"""
    def target_ids(self):
        return get_span_target_ids(self)


def get_span_target_ids(layer):
    if layer.span is None:
        return []
    return [t.id for t in layer.span.targets]


@dataclass
class AttributeLayer(AttributeGetter):
    """a layer containing only attributes"""
    layer: str
    attrs: dict = field(default_factory=dict)

    def node(self):
        node = etree.Element(self.layer)
        set_attributes(self, node)
        return node

    @staticmethod
    def get_obj(layer_name, node):
        return AttributeLayer(layer_name, node.attrib)


def get_attribute(layer, key):
    if layer.attrs is not None and key in layer.attrs.keys():
        return layer.attrs[key]
    else:
        return None


def set_attributes(layer, node):
    if layer.attrs is not None:
        for k, v in layer.attrs.items():
            node.set(k, v)


def create_node(name, text, children, attributes):
    node = etree.Element(name)
    if text is not None:
        node.text = etree.CDATA(text)
    for child in children:
        node.append(child.node())
    for k, v in attributes.items():
        node.set(k, v)
    return node