import pytest

from typing import Optional
from pyoxigraph import NamedNode, Store
from pyoxigraph_pydantic import RDFModel, Namespace, Property

def test_base_model_write():
    FOAF = Namespace(iri='http://xmlns.com/foaf/0.1/')

    class MyModel(RDFModel):
        is_a = FOAF.Person
        name: Property[str, FOAF.name]
        friend: Optional[Property[NamedNode, FOAF.knows]] = None


    friend = MyModel(iri="tmp:#Friend", name="my friend!")
    me = MyModel(iri="tmp:#Me", name="my friend", friend=friend)
    me.friend = friend

    store = Store()
    me.add(store)

    # TODO: finish this and make it actually test the values lmao

