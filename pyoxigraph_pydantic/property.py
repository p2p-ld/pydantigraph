"""
Combine type checking with RDF-like property creation using Annotated type hints

ie we want

.. code-block:: python

    from typing import ClassVar
    from pyoxigraph import NamedNode
    from pyoxigraph_pydantic import RDFModel, Namespace
    FOAF = Namespace(uri='http://xmlns.com/foaf/0.1/', prefix='foaf')

    class MyModel(RDFModel):
        is_a: ClassVar[NamedNode] = FOAF.Person
        name: Property[str, FOAF.name]
        knows: Property[list[FOAF.name], FOAF.knows]
        myProp: int

    data = MyModel(
        myName = "Rumbly",
        knows = ["Santi", "Pichu"],
        myProp = 10
    )

To be serialized like:

.. code-block:: turtle

    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    [] a foaf:Person ;
        foaf:name "Rumbly" ;
        foaf:knows [
            foaf:name "Santi" ] ;
        foaf:knows [
            foaf:name "Pichu" ] ;
        _:myProp 10 .


"""