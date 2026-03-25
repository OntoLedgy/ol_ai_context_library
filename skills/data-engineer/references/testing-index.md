# Testing Standards Index

All testing standards are sourced from `prompts/coding/standards/testing/`. This index maps each concern to the authoritative document.

---

## Standard Documents

| Document | Covers |
|----------|--------|
| `testing/TESTING_GUIDELINES.md` | Testing philosophy, test types, structure, what to test |
| `testing/TEST_QUALITY_REQUIREMENTS.md` | Quality gates, coverage requirements, test naming, assertion patterns |
| `testing/unit_tests.md` | Unit test specifics — isolation, mocking, test doubles |

---

## Testing Principles (Quick Reference)

### What to Test

For every non-trivial function or class:

| Test Category | What It Covers |
|--------------|----------------|
| **Happy path** | Normal inputs produce expected outputs |
| **Error conditions** | Invalid inputs raise the right exceptions with useful messages |
| **Edge cases** | Empty collections, zero values, boundary values (min/max), None where relevant |
| **Input validation** | Rejected inputs are rejected cleanly, not silently ignored |

### Test Structure (Arrange-Act-Assert)

```python
def test_something_does_expected_thing():
    # Arrange — set up inputs and expected outputs
    input_value = ...
    expected_output = ...

    # Act — call the code under test
    result = function_under_test(input_value)

    # Assert — verify the result
    assert result == expected_output
```

### Test Naming

Tests names should read as specifications:
```
test_[function]_[scenario]_[expected_outcome]
```

Examples:
- `test_calculate_total_with_empty_list_returns_zero`
- `test_parse_date_with_invalid_format_raises_value_error`
- `test_create_entity_with_valid_inputs_returns_entity_with_correct_id`

### One Assertion Focus Per Test

Each test should verify one logical behaviour. Multiple `assert` statements are acceptable only if they all verify facets of the same single outcome.

Avoid: one test that checks happy path AND error condition AND edge case — split into three tests.

### Mocking Guidelines

- Mock at system boundaries only — external APIs, databases, file system
- Never mock the code under test itself
- Prefer real objects for domain logic; mocks introduce false confidence
- If you need to mock many things, the code under test is probably doing too much

---

## Test File Organisation

```
tests/
├── unit/
│   ├── test_[module_name].py       # mirrors source structure
│   └── ...
├── integration/
│   ├── test_[feature_name].py
│   └── ...
└── conftest.py                     # shared fixtures
```

---

## Quality Gates

Before declaring implementation complete:

```bash
pytest                  # all tests pass
pytest --cov=src        # check coverage (target: > 80% for new code)
mypy src/               # no type errors
ruff check src/         # no linting violations
```

Report failures; do not suppress or skip.

---

## Relationship to bclearer Testing

When working in the bclearer codebase, these general testing standards apply. The bclearer-specific tools (pytest, mypy, ruff) are already configured in `pyproject.toml`. No additional tooling setup is required.

For BIE domain code specifically, factory functions should be tested with a `NoOpBieIdRegisterer` to avoid real registry side effects in unit tests.
