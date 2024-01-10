import urllib.parse
from typing import Optional

from pyoxigraph import NamedNode
from pyoxigraph_pydantic.base import BaseNode
from pydantic import computed_field

class Namespace(BaseNode):
    """
    Mirroring :class:`rdflib.Namespace` - convenience class for handling
    multiple terms from a namespace without needing the full URI every time!

    Examples:

        Simple usage:

        >>> ns = Namespace(uri='https://example.org')
        >>> ns.property
        NamedNode('https://example.org/property')

        For nodes that use strings not allowed by python in attribute names,
        or to use nodes that are already used as model fields, indexing works the same:

        >>> ns['Not-a-python-name']
        NamedNode('https://example.org/Not-a-python-name')
        >>> ns['node']
        NamedNode('https://example.org/node')

    Note:

        Since :class:`pyoxigraph.NamedNode` is marked as ``final`` and can't be
        subclassed, and since it's a Rust package with python bindings and probably shouldn't
        try and bypass that, we can't make this recursive -- ``Namespace.property.property2`` doesn't work
    """
    uri: str
    prefix: Optional[str] = None

    @computed_field
    @property
    def value(self) -> str:
        """Compatibiltiy with pyoxigraph semantics"""
        return self.str

    @property
    def node(self) -> NamedNode:
        """
        The :class:`.NamedNode` for the base namespace URI.

        NamedNode can't be subclassed since it's typed as ``final`` ,
        so this is our workaround
        """
        return NamedNode(self.uri)

    def __getattr__(self, item:str) -> NamedNode:
        uri = urllib.parse.urljoin(self.uri, item)
        node = NamedNode(uri)
        node._namespace = self.uri
        return node

    def __getitem__(self, item:str) -> NamedNode:
        if item.startswith('/'):
            item = item.lstrip('/')
        uri = urllib.parse.urljoin(self.uri, item)
        node = NamedNode(uri)
        node._namespace = self.uri
        return node


