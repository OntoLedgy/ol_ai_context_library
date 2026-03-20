You are operating in **{{ mode }}** mode.

{% if mode == "implement" %}
Target domain path: `{{ target_path }}`

Approved ontology model:
{{ ontology_model }}

Read all existing files under the target path, then follow the Implementation Workflow from your instructions. Implement all four artifacts (enum, identity vectors, factories, object classes) in the leaf-first construction order from the ontology model. Write unit tests for each factory. Run pytest and mypy when done.
{% endif %}

{% if mode == "migrate" %}
Target domain path: `{{ target_path }}`

Domain: {{ domain_description }}

Read all files under the target path. Identify all `BieDomainObjects` subclasses that still use the old pattern (`_create_vector()`, `BieIdCreationFacade` in `__init__`, or direct infrastructure registry calls). For each one:
1. Create the `*IdentityVectorPlaces` NamedTuple and `*IdentityVector` class in the appropriate `bie_identity_vectors/` sub-package
2. Create a `create_*()` factory function in a sibling `factories/` sub-package
3. Refactor the domain object class to accept `bie_base_identity: BieBaseIdentities` and remove all identity/registration logic from `__init__`
4. Update all call sites to use the factory instead of direct construction

Run the full test suite to confirm nothing is broken.
{% endif %}

{% if mode == "review" %}
Target domain path: `{{ target_path }}`

Read all files under the target path, then apply the conformance rules from your instructions. For each domain object class found:
- Check whether it conforms to the three-tier construction pattern
- Identify any old-pattern violations (`_create_vector()`, `BieIdCreationFacade` in `__init__`, direct registry access)
- Report findings as a table: object class | violation | severity | recommended fix

End with a verdict: CONFORMANT / PARTIAL / NON-CONFORMANT.
{% endif %}
