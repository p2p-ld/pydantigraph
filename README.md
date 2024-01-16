# pydantigraph
ORM data models, schemas, and vocabularies for pyoxigraph

- [ ] ORM-like read/write with pyoxigraph
  - [ ] Read - just model fields
  - [ ] Read - model fields + all triples with matching subject
  - [ ] Lazy read - read connected entities when accessed
  - [ ] Write
  - [ ] Update
  - [ ] Delete
  - [ ] Crawl - get triples n-steps out from current object leaves with filtering
- [x] Namespaces for using schema
  - [ ] Code generation from existing schema 
- [x] Fields and type annotations for declaring terms
  - [ ] Fields are properly checked by MyPy using the first type parameter
- [ ] Lists <-> blank node collections
- [ ] Pydantic validation
  - [ ] JSON-Schema
  - [ ] RDF serialization with rdflib
  - [ ] IRI (not URL) validator
  - [ ] Only fields that map onto RDF literals allowed

## See Also

- https://pypi.org/project/rdflib-orm/