import pytest

from pyoxigraph_pydantic import Namespace
from pyoxigraph import NamedNode

def test_namespace_terms():
    """
    We should be able to recursively refer to terms using a Namespace object
    :return:
    """
    target1 = NamedNode('https://example.com/myProperty')
    target2 = NamedNode('https://example.com/my-Non-Python-Property')
    target3 = NamedNode('https://example.com/node')
    target4 = NamedNode('https://example.com/subpath/subProperty')

    ns1 = Namespace(uri='https://example.com')
    ns2 = Namespace(uri='https://example.com/')
    ns3 = Namespace(uri='https://example.com/subpath')

    assert ns1.myProperty == target1
    assert ns1['my-Non-Python-Property'] == target2
    assert ns1['node'] == target3

    assert ns2.myProperty == target1
    assert ns2['my-Non-Python-Property'] == target2
    assert ns2['node'] == target3

    assert ns3.subProperty == target4

