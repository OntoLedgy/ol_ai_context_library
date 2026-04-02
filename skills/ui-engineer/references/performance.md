# Frontend Performance

Performance is a design constraint, not an afterthought. The three measurable targets that
define a "fast" experience are the Core Web Vitals. Everything else in this file exists to
hit them.

---

## Core Web Vitals — Hard Targets

Google evaluates these at the **75th percentile** across all page visits.

| Metric | What it measures | Good | Needs work | Poor |
|--------|-----------------|------|-----------|------|
| **LCP** — Largest Contentful Paint | Loading performance | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **INP** — Interaction to Next Paint | Responsiveness | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS** — Cumulative Layout Shift | Visual stability | ≤ 0.1 | ≤ 0.25 | > 0.25 |

These are not aspirational — they are pass/fail gates before a feature ships.

### Measuring in the Browser

```typescript
// Observe LCP in development
const observer = new PerformanceObserver(list => {
  const entries = list.getEntries();
  const lcp = entries[entries.length - 1];
  console.log('LCP:', lcp.startTime, 'ms');
});
observer.observe({ type: 'largest-contentful-paint', buffered: true });
```

Use the `web-vitals` library for real-user monitoring in production:
```typescript
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(console.log);
onINP(console.log);
onCLS(console.log);
```

---

## LCP — Loading Performance

**Target: ≤ 2.5s**

| Rule | Implementation |
|------|---------------|
| Server response < 800ms | Measure TTFB; cache at CDN edge |
| Preload the LCP element | `<link rel="preload" as="image">` for hero images |
| Inline above-fold CSS | No render-blocking stylesheet for critical styles |
| No render-blocking JS on the critical path | `defer` or `async` on non-critical scripts |
| Compress images correctly | WebP/AVIF; correct `sizes` attribute on `<img>` |
| Self-host critical fonts | Avoids third-party DNS lookup on the critical path |

```tsx
// Correct: explicit dimensions prevent layout reflow; priority loads immediately
<Image
  src="/hero.webp"
  width={1200}
  height={600}
  priority          // Next.js: preloads this image
  alt="Dashboard overview"
/>
```

---

## INP — Interaction Responsiveness

**Target: ≤ 200ms** (event handler completes and browser paints within 200ms)

### Break Long Tasks

Any JS task that runs > 50ms blocks the main thread and degrades INP. Break long tasks:

```typescript
// Bad: synchronous heavy work blocks input handling
function processResults(data: RawResult[]) {
  return data.map(item => expensiveTransform(item));  // 300ms of synchronous work
}

// Good: yield to the browser between chunks
async function processResultsAsync(data: RawResult[]) {
  const chunkSize = 100;
  const results: ProcessedResult[] = [];
  for (let i = 0; i < data.length; i += chunkSize) {
    const chunk = data.slice(i, i + chunkSize);
    results.push(...chunk.map(expensiveTransform));
    await new Promise(resolve => setTimeout(resolve, 0));  // Yield
  }
  return results;
}
```

### Provide Immediate Visual Feedback

Users perceive < 100ms as instant. For operations that take longer, show feedback immediately:

```typescript
function SubmitButton({ onSubmit }: SubmitButtonProps) {
  const [isPending, setIsPending] = useState(false);

  const handleClick = async () => {
    setIsPending(true);           // Immediate feedback within the same event
    await onSubmit();
    setIsPending(false);
  };

  return <Button loading={isPending} onClick={handleClick}>Submit</Button>;
}
```

### Defer Non-Critical Work

```typescript
// Non-critical analytics work deferred until browser is idle
requestIdleCallback(() => {
  trackPageView({ page: location.pathname });
});

// Visual updates deferred to next frame
requestAnimationFrame(() => {
  element.classList.add('highlighted');
});
```

---

## CLS — Visual Stability

**Target: ≤ 0.1** (elements should not shift unexpectedly after initial paint)

| Rule | Implementation |
|------|---------------|
| Always set explicit image dimensions | `width` + `height` or `aspect-ratio` in CSS |
| Reserve space for async content | Skeleton loaders matching the final layout size |
| Avoid inserting content above existing content | Insert dynamic content at the bottom or in reserved space |
| Animate with `transform` only | `transform: translateY()` not `margin-top` — transforms don't cause layout |
| Use `font-display: optional` for non-critical fonts | Prevents FOUT-triggered layout shift |

```css
/* Reserve space for an image before it loads */
.hero-image {
  aspect-ratio: 16 / 9;
  width: 100%;
  background: var(--color-neutral-100);  /* Placeholder colour */
}
```

---

## React Performance: Eliminating Waterfalls

A waterfall happens when requests are made sequentially when they could be parallel.
This is the single highest-impact React performance issue.

### Parallel Data Fetching

```typescript
// Bad: sequential — request 2 waits for request 1 to complete
function PipelineDashboard({ pipelineId }: { pipelineId: string }) {
  const { data: pipeline } = useQuery(pipelineQuery(pipelineId));
  const { data: stages } = useQuery(stagesQuery(pipelineId));  // Waits for pipeline
  const { data: metrics } = useQuery(metricsQuery(pipelineId)); // Waits for stages
}

// Good: parallel — all three requests fire simultaneously
function PipelineDashboard({ pipelineId }: { pipelineId: string }) {
  const results = useQueries({
    queries: [
      pipelineQuery(pipelineId),
      stagesQuery(pipelineId),
      metricsQuery(pipelineId),
    ],
  });
  const [pipeline, stages, metrics] = results;
}
```

### Prefetch on Hover

```typescript
const queryClient = useQueryClient();

function PipelineListItem({ pipeline }: { pipeline: PipelineSummary }) {
  const prefetch = useCallback(() => {
    queryClient.prefetchQuery({
      queryKey: ['pipeline', pipeline.id],
      queryFn: () => fetchPipeline(pipeline.id),
      staleTime: 10_000,
    });
  }, [pipeline.id]);

  return (
    <li onMouseEnter={prefetch} onFocus={prefetch}>
      <Link to={`/pipelines/${pipeline.id}`}>{pipeline.name}</Link>
    </li>
  );
}
```

---

## Bundle Size Optimisation

### Code Splitting

```typescript
// Lazy-load routes — each route is a separate chunk
const PipelineDashboard = lazy(() => import('./pages/pipeline/PipelineDashboard'));
const ResultsReview = lazy(() => import('./pages/results/ResultsReview'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/pipelines/:id" element={<PipelineDashboard />} />
        <Route path="/results/:id" element={<ResultsReview />} />
      </Routes>
    </Suspense>
  );
}
```

### Lazy-Load Heavy Libraries

```typescript
// Bad: ECharts loaded on every page even when not needed
import ReactECharts from 'echarts-for-react';

// Good: loaded only when the chart component mounts
const ReactECharts = lazy(() => import('echarts-for-react'));
```

### Bundle Analysis

Run after each significant dependency addition:
```bash
npx vite-bundle-visualizer   # Vite projects
npx @next/bundle-analyzer    # Next.js projects
```

**Red flags to investigate**:
- A single chunk > 200 KB (gzipped)
- The same dependency appearing in multiple chunks (should be shared)
- Development-only packages (e.g. `@storybook/*`) in the production bundle

---

## Re-render Memoisation

Memoisation has a cost — apply it only where profiling confirms a problem.

### When to Use `React.memo`

```typescript
// Only memo components that: re-render frequently AND are expensive to render
const StageCard = React.memo(function StageCard({ stage }: StageCardProps) {
  // Expensive render: lots of DOM nodes or complex calculations
  return <div>...</div>;
});

// No memo needed: cheap render, infrequent updates
function StatusBadge({ status }: StatusBadgeProps) {
  return <span className={styles[status]}>{status}</span>;
}
```

### `useMemo` for Expensive Derivations

```typescript
// Good: expensive filter/sort runs only when data or query changes
const filteredResults = useMemo(
  () => results.filter(r => r.label.includes(searchQuery)).sort(byDate),
  [results, searchQuery],
);

// Bad: useMemo for trivial derivations adds overhead without benefit
const label = useMemo(() => `${firstName} ${lastName}`, [firstName, lastName]);
// Just write: const label = `${firstName} ${lastName}`;
```

### State Colocation Prevents Unnecessary Re-renders

```typescript
// Bad: search state at page level re-renders the whole page on each keystroke
function ResultsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  return (
    <>
      <ExpensiveHeader />                    {/* Re-renders on every keystroke */}
      <SearchBox value={searchQuery} onChange={setSearchQuery} />
      <ResultsTable query={searchQuery} />
    </>
  );
}

// Good: search state co-located with what needs it
function ResultsSection() {
  const [searchQuery, setSearchQuery] = useState('');
  return (
    <>
      <SearchBox value={searchQuery} onChange={setSearchQuery} />
      <ResultsTable query={searchQuery} />
    </>
  );
}
```

---

## List Virtualisation

**Rule**: Virtualise any list or table with > 50 rows. Rendering all rows to the DOM is O(n)
in render cost and causes significant scroll jank above ~200 rows.

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualResultsTable({ results }: { results: ProcessingResult[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: results.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48,    // Estimated row height in px
    overscan: 5,               // Rows to render outside the visible area
  });

  return (
    <div ref={parentRef} className={styles.tableContainer}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              transform: `translateY(${virtualRow.start}px)`,
              height: `${virtualRow.size}px`,
            }}
          >
            <ResultRow result={results[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Image and Font Optimisation

### Images

```tsx
// Always specify width + height (prevents CLS)
// Use next/image or equivalent for automatic format negotiation (WebP/AVIF)
<Image
  src="/chart-thumbnail.png"
  width={400}
  height={225}
  loading="lazy"              // Below-fold images: lazy load
  alt="Pipeline run results"
/>

// Above-fold hero: eager + preload
<Image src="/hero.webp" width={1200} height={600} priority alt="..." />
```

### Fonts

```css
/* Self-host fonts to eliminate third-party DNS lookup */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-variable.woff2') format('woff2');
  font-display: swap;     /* Show fallback immediately; swap when loaded */
  font-weight: 100 900;   /* Variable font covers all weights in one file */
}
```

```html
<!-- Preload the primary font file in <head> -->
<link rel="preload" href="/fonts/inter-variable.woff2" as="font" type="font/woff2" crossorigin>
```

---

## Performance Checklist (Pre-ship)

| Check | Tool | Target |
|-------|------|--------|
| LCP | Lighthouse / `web-vitals` | ≤ 2.5s |
| INP | Lighthouse / `web-vitals` | ≤ 200ms |
| CLS | Lighthouse / `web-vitals` | ≤ 0.1 |
| No long tasks on critical path | Chrome DevTools Performance tab | No task > 50ms |
| Bundle size | `vite-bundle-visualizer` | No chunk > 200 KB gzipped |
| No waterfall requests | Chrome DevTools Network tab | Requests fire in parallel |
| Lists virtualised | Code review | > 50 rows → virtualised |
| Images have explicit dimensions | Lighthouse | Zero CLS from images |
