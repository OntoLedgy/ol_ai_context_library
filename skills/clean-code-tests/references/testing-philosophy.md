# Testing Philosophy

Core principles that apply to all languages and test types.

---

## F.I.R.S.T.

Every test must satisfy all five properties:

| Principle | Rule |
|-----------|------|
| **Fast** | Unit tests run in < 1 second each; full unit suite in < 5 minutes |
| **Independent** | Tests do not depend on each other; pass in any order, in any subset |
| **Repeatable** | Same result in every environment — local, CI, offline |
| **Self-Validating** | Boolean pass/fail; no manual log inspection required |
| **Timely** | Written alongside production code, not as an afterthought |

---

## Test Code Is Production Code

Test code requires the same care, design, and maintenance as production code.

- Dirty tests → harder to change production code → tests get abandoned → code rots
- Clean tests → confidence to refactor → production code stays healthy

**The dirtier the tests, the dirtier the code becomes.**

---

## The Three Laws of TDD

1. Do not write production code until you have a failing unit test
2. Do not write more of a unit test than is sufficient to fail (not compiling is failing)
3. Do not write more production code than is sufficient to pass the failing test

These laws produce a tight red/green/refactor cycle — roughly thirty seconds long.

---

## One Concept per Test

The rule is not strictly "one assert per test" — it is **one concept per test**.

A test that checks a single behaviour may need multiple assertions to express it
fully. That is acceptable. What is not acceptable is a test that exercises two
unrelated scenarios in the same function — that makes failures ambiguous and names
impossible to write.

```
# Bad — two unrelated concepts
test_add_months_handles_month_boundary_and_leap_year

# Good — one concept each
test_add_months_wraps_to_next_month_when_source_is_31st
test_add_months_clips_to_february_28_in_non_leap_year
```

---

## Readability Above All

What makes a clean test? **Readability, readability, readability.**

Tests are documentation. A reader should be able to understand what the production
code does — and what it guarantees — by reading the test names and bodies alone,
without reading the implementation.

### Build-Operate-Check

Tests follow a simple three-phase pattern:

1. **Build** — create test data and set up the scenario
2. **Operate** — execute the thing under test
3. **Check** — verify the results

This maps directly to Arrange / Act / Assert. Separate each phase with a blank line.

### Domain-Specific Test Language

Build helpers that make the scenario obvious:

```python
# Instead of
user = User(name="Alice", role="admin", active=True, created=datetime.now())
service = AuthService(db=FakeDb([user]))
result = service.check_permission(user.id, "write_report")
assert result is True

# Prefer
user = make_active_admin(name="Alice")
assert can_write_reports(user)
```

Helpers like `make_active_admin()` and `can_write_reports()` read like a specification,
not like infrastructure wiring.

---

## Tests Enable Change

Tests are what keep production code flexible, maintainable, and reusable.

- Without tests, every change is a potential bug
- With tests, you can change code without fear
- If you let the tests rot, the code will rot too
