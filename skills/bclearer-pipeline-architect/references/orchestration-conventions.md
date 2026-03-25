# Orchestration Conventions

> **Status: Skeleton** — populate with bclearer-specific orchestration conventions as they are confirmed from the codebase. Base orchestration services are in `software-architect/references/technology-stack.md`.

---

## Pipeline Entry Points

bclearer pipelines are launched via `b_app_runner_service`. The runner is the sole entry point — it creates the Universe, calls stage orchestrators in order, and handles top-level error reporting.

```python
# Conventional entry point structure (to be confirmed from codebase)
runner = SomePipelineRunner(config=...)
runner.run()
```

---

## Orchestrator Responsibility

The pipeline orchestrator:
- Creates the Universe
- Calls each stage in order, passing the Universe
- Does not contain business logic
- Does not call interop services directly (delegates to stage adapters)

Each stage is a separate class or module with a single `run(universe)` method (or equivalent).

---

## Universe Lifecycle

```
Runner.__init__       → create Universe
Runner.run()
  ├── Stage1.run(universe)    → populate with raw data
  ├── Stage2.run(universe)    → populate with domain objects
  ├── Stage3.run(universe)    → enrich domain objects
  └── Stage4.run(universe)    → export from universe
Runner teardown       → serialise or dispose Universe
```

---

## Conventions to Document (TODO)

- [ ] Standard runner class structure (`b_app_runner_service` API)
- [ ] Universe creation and initialisation pattern for new pipeline types
- [ ] Configuration passing convention (config file, env vars, constructor params)
- [ ] Logging integration per stage (`logging_service` hooks)
- [ ] Snapshot universe vs. standard universe — when to use each
- [ ] Multi-pipeline orchestration (pipelines that call other pipelines)
- [ ] Testing a pipeline runner (how to inject test doubles for stage I/O)
