# Code Style Conventions

Follow these conventions exactly. They are consistent throughout the codebase.

## Line Continuations

Use backslash `\` continuations for assignments and returns:

```python
result = \
    some_function()

return \
    result
```

## Named Keyword Arguments

Always use named keyword arguments in function calls (no positional args after the first):

```python
BieIdCreationFacade.create_bie_id_for_single_object(
    input_object=input_object,
    bie_domain_type=bie_domain_type)
```

## Naming

- Verbose descriptive variable names — no abbreviations
- Classes: `PascalCase` with role suffix (`...Types`, `...Objects`, `...Wrappers`, `...Registries`)
- Functions: `snake_case` verbs (`create_...`, `register_...`, `get_...`)
- Files: `snake_case` matching class/function name

## Class Inheritance

Put the parent class on a separate indented line:

```python
class MyDomainEnums(
        BieEnums):
```

## Enum Members

Each member on its own block with `= \` continuation:

```python
BIE_SOME_TYPE = \
    auto()
```

## Imports

Use full package import paths with backslash continuation for long imports:

```python
from nf_common_base.b_source.services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import \
    BieIdCreationFacade
```

## Function Signatures

Parameters each on their own indented line, return type after `\`:

```python
def create_something(
        input_a: str,
        input_b: str) \
        -> BieIds:
```

## Lists

Multiline with items indented inside brackets:

```python
input_objects = \
    [
        item_a,
        item_b
    ]
```
