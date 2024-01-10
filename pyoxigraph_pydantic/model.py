from typing import Optional, ClassVar
from pydantic import BaseModel
from pyoxigraph import NamedNode

class RDFModel(BaseModel):
    uri: Optional[str] = None
    is_a: ClassVar[Optional[NamedNode]] = None
