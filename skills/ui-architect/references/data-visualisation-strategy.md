# Data Visualisation Strategy

## Design Philosophy

Visualisation design begins with the **question the user needs to answer**, not the shape
of the data. A chart that maps to the data structure but doesn't answer the question is
architectural waste.

---

## Step 1: Match Chart Type to User Question

| User Question | Chart Type | Notes |
|---------------|-----------|-------|
| How does this change over time? | **Line chart** | Continuous trends; use area chart for cumulative values |
| How do these categories compare? | **Bar chart** | Vertical for < 8 categories; horizontal for long labels |
| What proportion of the whole? | **Pie / donut** | Maximum 5 slices; use bar chart if more categories |
| What is the relationship between two variables? | **Scatter plot** | Add trend line for correlation; add size encoding for a third variable |
| How is this distributed? | **Histogram** | Use beeswarm for small datasets (< 100 points) |
| Where are the patterns in dense data? | **Heatmap** | Time × category matrices; geographic density |
| What is the current status at a glance? | **KPI card / gauge** | Single metric only; colour encodes status |
| How does a real-time value change? | **Sparkline / live line chart** | Minimal decoration; prioritise render speed |
| How do multiple time series compare? | **Multi-series line chart** | Maximum 5–7 series before readability breaks |
| What is the breakdown of a total? | **Stacked bar** | Use with caution — harder to read than grouped bars |

---

## Step 2: Select the Chart Library

**One library per application** — mixing chart libraries produces visual inconsistency and
unnecessary bundle bloat. Choose once, document the rationale, enforce it.

### Library Comparison Matrix

| Library | Best For | Rendering | React Integration | Bundle Impact |
|---------|----------|----------|------------------|---------------|
| **Recharts** | Business dashboards, standard chart types | SVG | Native (React components) | Medium |
| **ECharts** | Large datasets (> 10K points), complex types | Canvas | Via wrapper | Large |
| **D3.js** | Fully bespoke, unique visualisations | SVG / Canvas | Manual integration | Small (core) |
| **Chart.js** | Simple charts, non-React contexts | Canvas | Via wrapper | Small |
| **Plotly.js** | Scientific, 3D, statistical visualisations | SVG / Canvas | Via wrapper | Large |

### Decision Rules

1. **Default**: **Recharts** — native React component model; covers 80% of business chart
   requirements; maintainable by any TypeScript engineer without specialist knowledge.
2. **Switch to ECharts when**: Dataset exceeds 10,000 data points, or SVG render performance
   degrades noticeably. Canvas rendering handles 10× more points than SVG.
3. **Use D3 when**: The visualisation is genuinely bespoke and cannot be composed from a
   standard library's chart types. Requires specialist knowledge — document this decision.
4. **Avoid Plotly unless**: The requirement is explicitly scientific, 3D, or statistical.
   Its bundle size is unjustified for standard business charts.

### Performance Limits by Rendering Mode

| Mode | Practical Interactive Limit | Action Above Limit |
|------|----------------------------|--------------------|
| SVG (Recharts default) | ~2,000 live data points | Switch to ECharts (Canvas) |
| Canvas (ECharts) | ~100,000 data points | Server-side aggregation + virtualisation |
| WebSocket throughput | ~30,000 points/sec (poor network) | Batch server-side before sending |

---

## Step 3: Real-Time Data Architecture

When data updates continuously (pipeline monitoring, live metrics, streaming results):

### Update Pipeline

```
Data Source → Server-Side Batching → WebSocket / SSE → Browser State → Chart Re-render
```

**Design these components explicitly** — do not leave real-time strategy to implementation.

### Batching Strategy

- Batch rapid updates on the server — **never forward every individual data point** to the browser
- Target: one update per 500–1000ms for dashboard displays; 100ms for critical metrics
- Use WebSocket for bidirectional communication; Server-Sent Events (SSE) for unidirectional
  streams from server to browser

### Browser-Side Architecture

- **Exponential backoff reconnection**: 1s → 2s → 4s → 8s → max 30s
- **Data retention limit**: browser holds maximum 1,000–5,000 live data points per chart
  (beyond this, trim the oldest points — specify the limit at design time)
- **Disable animations** during real-time updates — animations slow re-renders
- **Memoize chart components**: re-render only when the data reference actually changes

### Disconnection State Design

Specify what the UI displays when the real-time connection is lost:

| State | Recommended Treatment |
|-------|----------------------|
| Reconnecting (< 5s) | Subtle indicator; do not disrupt the user |
| Reconnecting (> 5s) | Clear status banner: "Reconnecting…" |
| Failed to reconnect | Error state with manual reconnect option; show last-known data with timestamp |

---

## Step 4: Colour and Accessibility

### Semantic Colour Conventions

- **Green / success**: positive values, completed states, above target
- **Red / danger**: negative values, error states, below threshold
- **Amber / warning**: degraded state, approaching threshold
- **Blue / neutral**: informational, selected, primary brand

### Accessibility Rules

- **WCAG AA contrast** (4.5:1) for all text rendered on chart backgrounds
- **Never rely on colour alone** — use shape, pattern, label, or icon as secondary encoding
- **Colour-blind-safe palette by default** — avoid red-green combinations without secondary encoding
- **Consistent palette**: the same category always uses the same colour across all charts in a dashboard

---

## Architecture Checklist for Visualisation Features

Before handing to `ui-engineer`, confirm all of these are specified:

| Concern | Question | Required Answer |
|---------|----------|----------------|
| Chart selection | Is the chart type driven by the user's question? | Yes — documented with rationale |
| Library choice | Is a single library specified for the application? | Yes — documented in tech stack |
| Real-time strategy | If real-time, is server-side batching designed? | Yes (or N/A if not real-time) |
| Performance target | Is a data point limit specified for live charts? | Yes (or N/A) |
| Accessibility | Is colour-blind safety addressed with secondary encoding? | Yes |
| Responsive design | Are chart container breakpoints specified? | Yes |
| Empty state | Is the "no data yet" state designed? | Yes |
| Loading state | Is the loading skeleton or spinner specified? | Yes |
