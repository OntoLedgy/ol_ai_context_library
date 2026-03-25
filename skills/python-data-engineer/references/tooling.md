# Python Tooling

---

## Standard Toolchain

| Tool | Purpose | Config |
|------|---------|--------|
| `ruff` | Linting + formatting (replaces flake8, isort, black) | `pyproject.toml [tool.ruff]` |
| `mypy` | Static type checking | `pyproject.toml [tool.mypy]` |
| `pytest` | Test runner | `pyproject.toml [tool.pytest.ini_options]` |
| `pytest-cov` | Coverage reporting | `pyproject.toml [tool.coverage]` |

---

## pyproject.toml (standard sections)

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM"]
# E/F: pycodestyle/pyflakes  I: isort  N: pep8-naming
# UP: pyupgrade  B: flake8-bugbear  SIM: simplify

[tool.mypy]
strict = true
python_version = "3.11"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]

[tool.coverage.report]
fail_under = 80
```

---

## Quality Gates (run in CI and before commit)

```bash
ruff check src/          # lint — flag violations
ruff format --check src/ # format check (no changes)
mypy src/                # type check
pytest                   # all tests pass
pytest --cov=src --cov-report=term-missing   # coverage
```

Auto-fix locally:
```bash
ruff check --fix src/    # fix auto-fixable lint issues
ruff format src/         # format in place
```

---

## Test Structure

```
tests/
├── conftest.py              # shared fixtures
├── unit/
│   └── test_[module].py    # mirrors src/ structure
└── integration/
    └── test_[feature].py
```

Run a specific test:
```bash
pytest tests/unit/test_transaction_service.py -v
pytest -k "test_process_batch"
```

---

## Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

pip install -e ".[dev]"     # install with dev dependencies
```

Or with `uv` (faster):
```bash
uv venv && uv pip install -e ".[dev]"
```
