import pytest

from pydantic import BaseModel
from pyoxigraph import NamedNode
from pyoxigraph_pydantic import Property, RDFModel

def test_property_parameterization():
    with pytest.raises(ValueError):
        mytype = Property['hey', NamedNode('https://example.com')]

    with pytest.raises(ValueError):
        mytype = Property[str, 'hey']

    with pytest.raises(RuntimeError):
        mytype = Property()

    mytype = Property[str, NamedNode('https://example.com')]

def test_property_schema():
    """
    IRIs should stay in the model schema!
    :return:
    """
    class MyModel(BaseModel):
        myField: Property[str, NamedNode('https://example.com')]

    assert 'iri' in MyModel.model_json_schema()['properties']['myField'].keys()
    assert MyModel.model_json_schema()['properties']['myField']['iri'] == 'https://example.com'





