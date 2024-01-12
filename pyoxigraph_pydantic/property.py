"""
Combine type checking with RDF-like property creation using Annotated type hints

ie we want

.. code-block:: python

    from typing import ClassVar
    from pyoxigraph import NamedNode
    from pyoxigraph_pydantic import RDFModel, Namespace
    FOAF = Namespace(iri='http://xmlns.com/foaf/0.1/', prefix='foaf')

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
import pdb
from abc import ABCMeta
from typing import Type, Any, Dict, Tuple, Callable, TypeVar, cast, Generic, TYPE_CHECKING, get_args
if TYPE_CHECKING:
    from pyoxigraph_pydantic import RDFModel
from types import GenericAlias

from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from pyoxigraph import NamedNode
from pyoxigraph_pydantic.types import Node

PropertyType = TypeVar('PropertyType', Type, GenericAlias, Node)
PropertyArgs = Tuple[PropertyType, NamedNode]


class PropertyMeta(ABCMeta):
    _all_types: Dict[Tuple[type, Tuple[Any, ...]], type] = {}
    __args__: PropertyArgs
    __type__: Type
    _parameterized: bool = False

    def __getitem__(cls, item: Tuple[PropertyType, NamedNode]) -> PropertyType:
        if getattr(cls, "_parameterized", False):
            raise RuntimeError(f"Type{cls} is already parameterized.")

        args = cls._check_item(item)
        result = cls._create_type(args)

        return result

    def _check_item(cls, item: PropertyArgs):
        if not isinstance(item, tuple):
            raise ValueError('Parameterization needs to be a tuple')
        if not len(item) == 2:
            raise ValueError(f'Incorrect number of arguments, need a type and a NamedNode')
        if not isinstance(item[0], (type, GenericAlias, NamedNode)):
            raise ValueError('The first argument must be a type or NamedNode!')
        if not isinstance(item[1], Node):
            try:
                item = (item[0], NamedNode(item[1]))
            except:
                raise ValueError('The second argument must be a NamedNode!')
        return item[0], item[1]

    def _create_type(
        cls, args: PropertyArgs
    ) -> type:
        key = (cls, args)
        if key not in cls._all_types:
            cls._all_types[key] = type(
                cls.__name__,
                (cls,),
                {"__args__": args, "_parameterized": True, '__type__': args[0], '__node__': args[1]},
            )
        return cls._all_types[key]

    def __str__(cls) -> str:
        type_, node = cls.__args__
        return (
            f"Property: type: {type_}, "
            f"node: {node}"
        )

    # def __instancecheck__(self, instance: Any):
    #     type_, node = self.__args__
    #     return isinstance(instance, type_)

    def __get_pydantic_core_schema__(
        cls,
        _source_type: 'Property',
        _handler: GetCoreSchemaHandler,

    ) -> core_schema.CoreSchema:
        type_, node = _source_type.__args__

        if type_ is NamedNode:
            type_handler = core_schema.str_schema()
        else:
            type_handler = _handler.generate_schema(type_)

        def url_from_namednode(node: NamedNode | Any) -> Any:
            if isinstance(node, NamedNode):
                return node.value
            else:
                return node

        def iri_from_property(arg: Any) -> Any:
            from pyoxigraph_pydantic import RDFModel
            if isinstance(arg, RDFModel):
                return arg.iri
            return arg

        def add_uri_to_json_schema(json_schema, handler):
            json_schema = handler(json_schema)
            json_schema.update({'iri': node.value})
            return json_schema

        json_handler = type_handler.copy()
        if 'metadata' not in json_handler:
            json_handler['metadata'] = {}
        json_handler['metadata']['pydantic_js_annotation_functions'] = [add_uri_to_json_schema]

        return core_schema.json_or_python_schema(
            json_schema = json_handler,
            python_schema = core_schema.chain_schema([
                core_schema.no_info_plain_validator_function(iri_from_property),
                type_handler,
                ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                url_from_namednode,
                when_used='json'
            )
        )




class Property(metaclass=PropertyMeta):
    __args__: PropertyArgs

    def __init__(self):
        raise RuntimeError(
            'Properties cannot be instantiated, use them like a subscriptable type like Property[type, NamedNode]')

