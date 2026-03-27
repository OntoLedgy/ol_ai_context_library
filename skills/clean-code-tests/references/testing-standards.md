# Testing Standards

Quality rules, structure, and checklist for all tests.
Read alongside `testing-philosophy.md` and the relevant `languages/[language].md`.

---

## 1. Coverage Requirements

| Metric | Threshold |
|--------|-----------|
| Overall coverage | 80% minimum |
| Critical path (core business logic) | 95% minimum |
| Branch coverage | 75% minimum |
| New code | 90% minimum |

**Test distribution target:** 70% unit / 20% integration / 10% end-to-end.

Each module MUST cover:
- Happy path scenarios
- Error conditions and all exception types raised
- Edge cases and boundary conditions
- Input validation
- Resource cleanup

---

## 2. Directory Structure

```
tests/
├── unit_tests/           # Fast, no external deps — always run in CI
│   └── <module>/
├── integration_tests/    # Require external services — marked heavy/slow
├── e2e_tests/
├── fixtures/             # Shared test fixtures (imported by conftest)
│   └── <service>/
├── data/
│   ├── input/            # Static input files — small and representative
│   └── output/           # Expected outputs for comparison
└── conftest.[ext]        # Root fixture configuration
```

File naming mirrors source:
- Source: `src/module/component.[ext]`
- Test:   `tests/unit_tests/module/test_component.[ext]`

---

## 3. Naming Conventions

```
Class:  Test<ComponentName>
Method: test_<action>_<condition>_<expected_result>
```

**Good names:**
```
test_load_transactions_returns_list_when_valid_csv
test_load_transactions_raises_file_not_found_when_path_missing
test_load_transactions_returns_empty_list_when_csv_is_empty
test_connect_invalid_credentials_raises_auth_error
```

**Bad names:** `test_1`, `test_stuff`, `test_error`, `test_it_works`, `testLoad`

---

## 4. Arrange / Act / Assert (AAA)

Every test body follows AAA, with each phase separated by a blank line.
Every test has a docstring or comment describing what it verifies.

```
[Arrange]  — create inputs, configure mocks, set up scenario

[Act]      — call the thing under test, capture the result

[Assert]   — verify the outcome matches expectations
```

Rules:
- One *concept* per test — test one behaviour, not one line
- Multiple asserts are allowed when they all verify the same single behaviour
- No logic in tests — no loops, conditionals, or try/catch in test bodies
- Prefer named helpers over inline magic values

---

## 5. Assertions

```
# REQUIRED: specific, with failure context
assert result.status == "success", f"Expected success, got {result.status}"
assert len(items) == 3, f"Expected 3 items, got {len(items)}"

# FORBIDDEN: vague or meaningless
assert result        # any truthy value passes — detects nothing
assert True          # always passes — meaningless
```

---

## 6. Test Independence

- Each test MUST clean up its own resources — use setup/teardown or fixture yield
- No shared mutable state between tests
- Tests MUST pass in any order, in any subset
- Database tests MUST use transactions or per-test cleanup

---

## 7. Performance

| Category | Limit per test |
|----------|---------------|
| Unit test | < 1 second |
| Integration test | < 10 seconds |
| Full unit suite | < 5 minutes |

Tests that exceed these limits MUST be marked as heavy/slow and excluded from CI default runs.

---

## 8. Fixture Design

| Scope | Use for |
|-------|---------|
| Function (default) | Temporary folders, per-test objects, mutable state |
| Class | Shared setup across methods in one test class |
| Module | Read-only configuration shared across a file |
| Session | Expensive resources — DB connections, large file paths |

Rules:
- Every fixture has a docstring describing what it provides and its scope
- Common fixtures go in a shared conftest or fixtures directory
- Fixtures clean up after themselves (yield + teardown, not just return)
- Required categories: configuration, data/files, mock, database (integration only)

---

## 9. Mocking

| Rule | Detail |
|------|--------|
| External services MUST be mocked in unit tests | DB, API, filesystem, clock |
| Never mock the thing under test | Mock dependencies, not the subject |
| Mocks MUST match the real interface | Same method names, same argument shapes |
| Mock failures MUST be tested | Not just the happy path |
| Verify call interactions | Assert the mock was called with the expected arguments |

---

## 10. Error Path Testing

Every exception path in production code MUST have at least one test.
Verify both the exception type and the message content.

```
# Pattern — verify type AND message
raises <ExceptionType> matching "<message fragment>"
  when <condition>
```

Also test:
- Error recovery mechanisms
- Cleanup after errors (resources released even on failure)
- Retry logic where present

---

## 11. Parametrised Tests

Use parametrisation for multiple input scenarios of the same behaviour.
Each combination gets its own named test case. Do not use a loop.

```
Scenarios:
  ("hello", "HELLO")
  ("world", "WORLD")
  ("",      ""     )
→ generates three independently named, independently runnable tests
```

---

## 12. Async Tests

- Use the project's standard async test marker (language-specific — see language reference)
- Test timeout scenarios — do not assume async calls complete instantly
- Test cancellation handling where the production code supports it
- Do not use sleep/wait without a timeout guard

---

## 13. Test Markers and Categories

| Marker | Meaning |
|--------|---------|
| *(none)* | Lightweight unit test — no external deps, fast, runs in CI |
| `heavy` / `slow` | Requires external service or large download — local/staging only |
| `integration` | Component interaction test |
| `async` | Asynchronous test requiring special runner |

Integration tests additionally require:
- Test-specific configuration (not production config)
- Isolated test data (no cross-test bleed)
- Proper cleanup after each test

---

## 14. Anti-Patterns

| Anti-pattern | Why it's wrong |
|--------------|----------------|
| `assert True` or no assertion | Test always passes — detects nothing |
| `assert result` without specifics | Any truthy value passes |
| Testing the mock, not production code | Verifies the mock, not behaviour |
| Logic in tests (loops, conditionals) | Obscures intent; introduces test bugs |
| Hardcoded absolute paths | Breaks on other machines and CI |
| `sleep`/`wait` without timeout | Flaky; can hang CI indefinitely |
| Tests requiring specific execution order | Hidden coupling between tests |
| Multiple unrelated concepts in one test | Impossible to name; hard to diagnose |
| Commented-out tests | Delete them; re-add with a ticket if needed |
| Modifying production data in tests | Tests must be side-effect free |
| Mocking the thing under test | You are testing the mock, not the code |

---

## 15. Compliance Checklist

### All tests
- [ ] Name follows `test_<action>_<condition>_<result>` pattern
- [ ] Has docstring or description explaining what is being verified
- [ ] AAA structure with blank-line separation between phases
- [ ] Assertions are specific and include failure context
- [ ] Cleans up all resources
- [ ] Independent — passes in any order, in any subset
- [ ] Completes within performance limit

### Unit tests (additional)
- [ ] All external dependencies mocked
- [ ] The thing under test is NOT mocked
- [ ] Tests one concept per method
- [ ] No logic (loops, conditionals) in test body

### Integration tests (additional)
- [ ] Marked as integration / heavy
- [ ] Uses test-specific configuration, not production config
- [ ] Verifies component interactions across real boundaries
- [ ] Handles cleanup properly after each test

### Async tests (additional)
- [ ] Uses the correct async test marker for the language
- [ ] All async calls properly awaited
- [ ] Timeout scenarios covered
- [ ] Cancellation handling tested where applicable
