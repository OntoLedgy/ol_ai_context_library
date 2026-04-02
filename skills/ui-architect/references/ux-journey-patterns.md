# UX Journey Design Patterns

## What Is a UX Journey?

A UX journey is a named, multi-step user interaction that achieves a specific business
outcome. Journeys are architectural concerns — they define component boundaries, state
machine requirements, error handling strategies, and progress models.

## Journey Anatomy

Every journey must specify all of these:

| Element | Description |
|---------|-------------|
| **Entry point** | How the user starts: route, button, deep link, system trigger |
| **Steps** | Ordered sequence of actions, each with a single, clear goal |
| **Decision points** | Branches based on user input or system state |
| **Exit states** | Success (goal achieved), Abandon (user leaves), Error (unrecoverable failure) |
| **Progress state** | What has been completed; what remains; what the user can revisit |

**Design error paths first** — error states are harder than happy paths. Leaving them to
implementation leads to poor UX that is expensive to fix.

---

## Document Upload Journey

**Use when**: User uploads one or more files to trigger a downstream process.

### Component Architecture

```
DocumentUploader (organism)
├── DropZone (molecule)           drag-and-drop zone + "Browse files" button
├── FileList (molecule)           selected files with status indicators + remove controls
│   └── FileItem (molecule) × n  filename, size, status, per-file progress, error message
├── UploadProgress (atom)         overall progress bar (optional, for bulk uploads)
└── UploadSummary (molecule)      completion state: success / partial success / failed
```

### Step Design

| Step | User Goal | Key States | Error Cases |
|------|-----------|-----------|-------------|
| 1. Select | Choose files to upload | Empty, files selected, max count reached | Wrong type, file too large, duplicate |
| 2. Review | Confirm selection before upload | File list with remove option | — |
| 3. Upload | Submit files; monitor progress | Per-file: queued, uploading (% progress), complete, failed | Network failure, server rejection, timeout |
| 4. Result | See outcome; take next action | All success, partial success, all failed | Partial failure: which files, why, retry option |

### UX Rules
- Provide both drag-drop AND a "Browse files" button — both must be equally discoverable
- Show specific error messages: `"invoice.pdf exceeds 5 MB"` not `"Upload failed"`
- Support multi-file selection; never force one-at-a-time uploads
- Show per-file progress bars, not only an overall bar
- Allow removal of individual files from the list before upload begins
- After upload: distinguish between "file received" and "file processed"

### State Machine (design this explicitly)

```
idle → files_selected → uploading → complete
                      ↘           ↗ (all files) → success
                        failed_partial → (some files) → partial_success
                        failed_all → error
```

---

## Pipeline Kick-Off Journey (Wizard Pattern)

**Use when**: User configures and initiates a data processing pipeline. Best for
complex configuration that can be logically segmented into steps.

### When to Use a Wizard

Use a wizard when:
- The task is long and unfamiliar to most users
- Information entry is logically segmentable
- Subsequent steps depend on earlier answers
- The process is completed infrequently (not a daily workflow)

Do NOT use a wizard for: short forms (< 9 fields total), expert daily workflows, or
processes that benefit from seeing all fields simultaneously.

### Component Architecture

```
PipelineWizard (organism)
├── StepIndicator (molecule)       current step + total steps ("Step 2 of 4")
├── StepContainer (template)       renders the active step component
│   ├── PipelineConfigStep         parameters, run name, schedule options
│   ├── SourceSelectionStep        input data selection (file, dataset, query)
│   ├── ReviewStep                 read-only summary of all inputs (editable via links)
│   └── SubmitStep                 final confirmation; submit button; SLA estimate
├── WizardNavigation (molecule)    Back / Next / Submit with loading states
└── AbandonConfirmation (molecule) "Unsaved changes — are you sure?" on exit
```

### Wizard Design Rules

- Maximum **5–9 fields per step**; 1–2 minutes per step target
- Each step has **one clear, self-contained goal** — if a step is doing two things, split it
- Show clear progress: `"Step 2 of 4 — Select your data source"`
- Explain **why** information is needed — users abandon when they don't understand the value
- Always include a **review/summary step** before final submission
- Allow editing **any previous step** directly from the review step
- `Back` navigation **never loses** the current step's input
- `Next` validates the current step before advancing — show inline errors, not a toast

### Step States (design all of these)

| State | Description |
|-------|-------------|
| `not_started` | Step not yet reached |
| `active` | Currently being filled in |
| `valid` | Completed with valid inputs |
| `invalid` | Attempted and has validation errors |
| `loading` | Awaiting async validation or data fetch |

---

## Pipeline Monitoring Journey

**Use when**: User watches the progress of a running or recently completed pipeline.

### Component Architecture

```
PipelineDashboard (template)
├── StatusHeader (organism)        pipeline name, overall status badge, elapsed time
├── StageProgressTimeline (organism) per-stage status in sequence
│   └── StageCard (molecule) × n  stage name, status, duration, record count, log excerpt
├── MetricsPanel (organism)        key metrics: records in/out, error rate, throughput
└── LogStream (organism)           filterable, searchable log output
```

### Information Architecture
- **F-pattern layout**: most critical status in the top-left
- Priority order: Overall Status → Stage Breakdown → Metrics → Logs
- Real-time updates for in-progress pipelines; static snapshot for completed
- Error states are **visually prominent** — not hidden inside a log viewer

### Pipeline Status States (design all explicitly)

| State | Visual Treatment | User Actions |
|-------|-----------------|--------------|
| `queued` | Neutral / muted | Cancel |
| `running` | Animated progress indicator | Cancel |
| `completed` | Success (green) | View results |
| `failed` | Error (red, prominent) | View error detail, Retry |
| `cancelled` | Muted / grey | Re-run |
| `partial` | Warning (amber) | View partial results, Retry failed stages |

### Real-Time Update Architecture
See `references/data-visualisation-strategy.md` for the full real-time strategy.
Key constraints to specify at design time:
- Update frequency: how often does the UI poll/receive updates?
- Data retention: how many historical log lines / metric points does the browser hold?
- Reconnection strategy: what does the UI show if the WebSocket drops?

---

## Results Review Journey

**Use when**: User reviews the output of a completed pipeline or data process.

### Component Architecture

```
ResultsDashboard (template)
├── SummaryPanel (organism)         run metadata + key metrics at a glance
├── DataExplorer (organism)         filterable, sortable, paginated results table
├── VisualisationPanel (organism)   charts appropriate to data type (see data-visualisation-strategy.md)
└── ExportControls (molecule)       download (CSV/Excel/JSON) + share options
```

### Information Architecture Rules
- **Lead with the answer**: summary metrics before raw data
- Group related information with visual separators
- **Progressive disclosure**: summary → detail → raw data
- Filters appear above the content they affect, with short plain labels
- Top 3–4 metrics aligned with the user's **primary objective**, not what is easy to count
- Empty states are designed — "No results found" includes a reason and a recovery action

---

## General UX Journey Rules

1. **Design error paths alongside happy paths** — both are first-class requirements
2. **Every step has one goal** — split steps that are doing two things
3. **Progress is always visible** — users know where they are and how far they have to go
4. **Back never destroys input** — backward navigation preserves all state
5. **Abandonment is graceful** — explicit confirmation before losing progress; offer resume where feasible
6. **Accessibility is per-step** — keyboard navigation and screen reader behaviour are
   specified for each step, not for the journey as a whole
7. **Loading states are designed** — every async operation has a designed loading state;
   never leave the user staring at a frozen UI
