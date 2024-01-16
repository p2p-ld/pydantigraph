import pdb
import inspect
from typing import Optional, ClassVar, Any, TYPE_CHECKING, get_args, Type
if TYPE_CHECKING:
    from pydantigraph import Property
from pydantic import BaseModel
from pyoxigraph import NamedNode, Store, Quad, Literal, DefaultGraph
from pydantigraph.const import IS_A

class RDFModel(BaseModel):
    iri: Optional[str] = None
    is_a: ClassVar[Optional[NamedNode]] = None

    def to_quads(self, graph: Optional[NamedNode] = None) -> list[Quad]:
        if graph is None:
            graph = DefaultGraph()


        subject = NamedNode(self.iri)
        quads = []
        if isinstance(self.is_a, NamedNode):
            quads.append(Quad(subject, IS_A, self.is_a, graph))

        for k, field in self.model_fields.items():
            value = getattr(self, k)
            if value is None or k in ('iri',):
                continue
            if not isinstance(value, NamedNode):
                if isinstance(value, RDFModel):
                    quads.extend(value.to_quads(graph))
                    value = NamedNode(value.iri)
                else:
                    value = Literal(value)

            prop_uri = get_property(field.annotation).__args__[1]
            quads.append(
                Quad(
                    subject, prop_uri, value, graph
                )
            )
        return quads


    def add(self, store: Store, graph: Optional[NamedNode] = None):
        quads = self.to_quads(graph)
        store.extend(quads)







def get_property(annotation: Any) -> Type['Property']:
    """
    Get a property from a potentially nested annotation
    """
    from pydantigraph import Property
    if inspect.isclass(annotation) and issubclass(annotation, Property):
        return annotation
    if get_args(annotation):
        for arg in get_args(annotation):
            if inspect.isclass(arg) and issubclass(arg, Property):
                return arg

    raise NotImplementedError(
        'This is just a lazy placeholder, more work to be done to make sure this works')
