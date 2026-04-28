# Component Standards: SOLID Principles for React

## Single Responsibility Principle

**Rule**: One component renders one thing. Do not mix data fetching, business logic, and
rendering in the same component.

**Before** (violates SRP):
```typescript
// UserProfile does too many things
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(data => { setUser(data); setLoading(false); });
  }, [userId]);

  const handleDeactivate = async () => {
    await fetch(`/api/users/${userId}/deactivate`, { method: 'POST' });
    setUser(prev => prev ? { ...prev, active: false } : null);
  };

  if (loading) return <Spinner />;
  return <div>...</div>;
}
```

**After** (SRP applied):
```typescript
// Logic in a hook
function useUserProfile(userId: string) {
  const { data: user, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
  const { mutate: deactivate } = useMutation({
    mutationFn: () => deactivateUser(userId),
  });
  return { user, isLoading, deactivate };
}

// Component only renders
function UserProfile({ userId }: { userId: string }) {
  const { user, isLoading, deactivate } = useUserProfile(userId);
  if (isLoading) return <Spinner />;
  return <UserProfileView user={user} onDeactivate={deactivate} />;
}
```

---

## Open/Closed Principle

**Rule**: Components are open for extension through props/composition; closed for internal
modification to add new behaviour.

**Before** (violates OCP — conditionals for every new variant):
```typescript
function Button({ label, type }: { label: string; type: 'primary' | 'danger' | 'ghost' }) {
  const className = type === 'primary' ? 'btn-primary'
    : type === 'danger' ? 'btn-danger'
    : 'btn-ghost';
  // Adding a new type requires modifying this component
  return <button className={className}>{label}</button>;
}
```

**After** (OCP — extend via props without modifying internals):
```typescript
interface ButtonProps {
  readonly children: React.ReactNode;
  readonly intent?: 'primary' | 'secondary' | 'danger' | 'ghost';
  readonly size?: 'sm' | 'md' | 'lg';
  readonly disabled?: boolean;
  readonly onClick?: () => void;
}

function Button({ children, intent = 'primary', size = 'md', ...props }: ButtonProps) {
  return (
    <button
      className={styles[`${intent}-${size}`]}
      {...props}
    >
      {children}
    </button>
  );
}
// New variant: add to the style map, not to the component
```

---

## Interface Segregation Principle

**Rule**: No component accepts props it does not use. When a component is used in multiple
unrelated contexts, split its props interface.

**Before** (violates ISP — many optional props the component may not use):
```typescript
interface TableProps {
  data: Row[];
  onEdit?: (row: Row) => void;       // Only needed in edit mode
  onDelete?: (row: Row) => void;     // Only needed in admin mode
  onExport?: () => void;             // Only needed with export feature
  showPagination?: boolean;          // Always needed
  pageSize?: number;                 // Always needed
}
```

**After** (ISP — compose specific interfaces):
```typescript
interface BaseTableProps {
  readonly data: Row[];
  readonly pageSize?: number;
}

interface EditableTableProps extends BaseTableProps {
  readonly onEdit: (row: Row) => void;
  readonly onDelete: (row: Row) => void;
}

interface ExportableTableProps extends BaseTableProps {
  readonly onExport: () => void;
}
```

---

## Dependency Inversion Principle

**Rule**: Components depend on prop abstractions (callback functions, typed data interfaces),
not concrete domain services. Never import a domain service directly into a component.

**Before** (violates DIP — component knows about pipeline service):
```typescript
import { pipelineService } from '../../services/pipelineService';

function PipelineStatusCard({ pipelineId }: { pipelineId: string }) {
  const [status, setStatus] = useState<PipelineStatus | null>(null);
  useEffect(() => {
    pipelineService.getStatus(pipelineId).then(setStatus);
  }, [pipelineId]);
  return <div>{status?.label}</div>;
}
```

**After** (DIP — component depends only on its props contract):
```typescript
interface PipelineStatusCardProps {
  readonly status: PipelineStatus;
  readonly label: string;
  readonly onRetry?: () => void;
}

function PipelineStatusCard({ status, label, onRetry }: PipelineStatusCardProps) {
  return <div>{label}</div>;
}
// Data fetching is the container/hook's concern, not the component's
```

---

## Component File Co-location

Keep related files together. A component's supporting files live alongside it:

```
DocumentUploader/
  DocumentUploader.tsx          Component
  DocumentUploader.test.tsx     React Testing Library tests
  DocumentUploader.stories.tsx  Storybook stories
  DocumentUploader.module.css   CSS Modules styles
  useDocumentUpload.ts          Co-located hook (if only used by this component)
  documentUploader.constants.ts Constants (copy strings, limits, config values)
  index.ts                      Public export: export { DocumentUploader }
```

**Rule**: If a hook or constant is used by only one component, co-locate it. If used by
two or more, move it to a shared location.

---

## Props Interface Rules

```typescript
// All props readonly — components do not mutate their inputs
interface DocumentUploaderProps {
  readonly acceptedTypes: string[];         // What file types are allowed
  readonly maxFileSizeBytes: number;        // Hard limit per file
  readonly maxFileCount?: number;           // Optional: limit number of files
  readonly onFilesSelected: (files: File[]) => void;  // Callback, not imperative
  readonly onUploadComplete?: (results: UploadResult[]) => void;
  readonly isUploading?: boolean;           // Controlled loading state
  readonly disabled?: boolean;
}
```

Rules:
- All props `readonly`
- Optional props use `?` — never use `undefined` as a default value explicitly
- Callback props follow `on` + noun convention
- No `any` in props — use specific types or generics
- No prop drilling beyond 2 levels — pass via Context or lift state

---

## Custom Hook Rules

```typescript
// Hook encapsulates logic; returns only what the component needs
function useDocumentUpload(options: UseDocumentUploadOptions) {
  const { maxFileSizeBytes, acceptedTypes, onComplete } = options;

  const [files, setFiles] = useState<FileWithStatus[]>([]);
  const [uploadState, setUploadState] = useState<UploadState>('idle');

  const handleFilesAdded = useCallback((newFiles: File[]) => {
    const validated = validateFiles(newFiles, { maxFileSizeBytes, acceptedTypes });
    setFiles(prev => [...prev, ...validated]);
  }, [maxFileSizeBytes, acceptedTypes]);

  const handleUpload = useCallback(async () => {
    setUploadState('uploading');
    // ... upload logic
  }, [files, onComplete]);

  return {
    files,
    uploadState,
    handleFilesAdded,
    handleUpload,
    removeFile: (index: number) => setFiles(prev => prev.filter((_, i) => i !== index)),
  } as const;
}
```

Rules:
- Always starts with `use`
- Returns a `const` object (prevents accidental mutation of the return value)
- No JSX inside hooks
- Side effects go in `useEffect` with proper dependency arrays
- `useCallback` on handlers that are passed to child components

---

## Forbidden Patterns

| Pattern | Why Forbidden | Alternative |
|---------|--------------|-------------|
| Domain service imports in components | Couples UI to business logic | Inject via props or custom hook |
| `any` in props or state | Loses type safety | Use `unknown` and narrow, or specific types |
| Inline styles (style={{ }}) | Hard to theme, hard to override | CSS Modules or design tokens |
| `!important` in CSS | Defeats cascade | Increase selector specificity correctly |
| `useEffect` for data derivation | Causes extra renders | Use `useMemo` for derived values |
| `index` as React `key` | Causes incorrect reconciliation on reorder | Use stable entity IDs |
| Nested ternaries in JSX | Unreadable | Extract to a named variable or helper function |
| `outline: none` without replacement | Destroys keyboard accessibility | Replace with `:focus-visible` ring using design tokens |
| `transition: all` | Animates layout properties; causes CLS and jank | List only `transform` and `opacity` explicitly |
| `user-scalable=no` in viewport meta | Blocks zoom for low-vision users | Never set; let users zoom |
| `<div onClick={...}>` | Not keyboard accessible; not announced by screen readers | Use `<button>` or `<a>` with correct role |
| Hardcoded date formats | Locale-incompatible | Use `Intl.DateTimeFormat` with explicit locale |

---

## Interaction Timing Budget

Concrete numbers for every animated or asynchronous response. These are
ceilings — feel free to be faster, but never exceed.

| Event | Target | Why |
|-------|--------|-----|
| Pressed-state feedback (button, list row, tab) | 80–150 ms | Below 80 ms feels twitchy; above 150 ms feels broken |
| Micro-interaction (hover, focus, toggle) | 150–300 ms | Long enough to perceive; short enough not to delay |
| Complex transition (panel slide, route change) | ≤ 400 ms | Beyond this, the user thinks the app has stalled |
| Loading indicator first appearance | ≤ 100 ms after action | Users register "nothing happened" at ~100 ms |
| Skeleton / spinner first appearance | ≤ 300 ms after action | Below 300 ms, instant feels better than spinner |
| Optimistic UI rollback on failure | ≤ 1 s | Long enough to detect failure, short enough to feel responsive |
| Toast auto-dismiss | 3–5 s | Long enough to read; short enough to not nag |
| Tooltip show delay | 400–600 ms | Prevents accidental tooltip storms when the cursor passes over |
| Tooltip hide delay | 100–200 ms | Forgiving when the cursor briefly leaves and returns |
| Frame budget | ≤ 16 ms per frame (60 fps) | Anything above causes visible jank |
| INP (Interaction to Next Paint) | ≤ 200 ms | Core Web Vital; must hold across primary interactions |
| Exit animation duration | 60–70% of entrance | Asymmetric timing feels natural; equal feels laboured |
| List-item stagger | 30–50 ms per item | Below 30 ms is invisible; above 50 ms feels slow |
| Modal scrim fade-in | 150–250 ms | Establishes context without being a "production" |

### Rules That Apply Across All Timings

- Use `ease-out` (decelerate) for entering elements
- Use `ease-in` (accelerate) for exiting elements
- Animate `transform` and `opacity` only — never layout properties
- Make animations interruptible (cancellable mid-flight when the user acts)
- Never block input during an animation
- Modals animate **from the trigger element**, not from a global anchor
- Forward and backward navigation use the same direction, mirrored
- A modal scrim sits at 40–60% black so foreground content remains legible

---

## Interaction Anti-patterns

These are the behavioural counterpart to the visual anti-patterns in
`ui-architect/references/aesthetic-quality.md`. Reject them in review.

| Anti-pattern | Why it fails | Alternative |
|--------------|-------------|-------------|
| **Focus order ≠ visual order** | Keyboard and screen-reader users get a different journey than sighted users | Author DOM in reading order; use `order` only for purely visual columns; never use positive `tabindex` |
| **Modal as primary navigation** | Modals are for self-contained tasks; using them as nav breaks back/forward, deep links, and screen readers | Real route + page transition |
| **Mixing tab bar + sidebar + bottom nav at the same hierarchy** | Users cannot tell which is "primary"; selection state contradicts itself | Pick one primary surface per hierarchy level |
| **Layout-shifting press state** (`padding`, `margin`, `width` change on `:active`) | Causes CLS; nearby elements jump under the finger | Animate `transform` and `opacity` only |
| **Gesture conflict in same region** (horizontal swipe inside vertical scroll, custom edge swipe over system back) | One gesture wins by accident; users learn neither works reliably | Pick one direction per region; reserve edge regions for system gestures |
| **`<div onClick>`** | Not focusable, not announced, not keyboard-activatable | `<button>` for actions, `<a>` for navigation |
| **Hover-only affordance** | Touch users cannot discover the action; keyboard users cannot trigger it | Make the action visible at rest, or expose via long-press / explicit menu |
| **Toast as the only error channel** | Toast disappears; user cannot recover the message | Toast for transient confirmation only; persistent error inline near the trigger |
| **Auto-advancing carousels** | Steals attention; fights screen readers; rarely read | User-driven advance, or auto-advance with prominent pause control + `prefers-reduced-motion` honoured |
| **Form validation on every keystroke** | Errors appear before the user finishes typing — punishing, not helpful | Validate on `blur`; allow inline character counters and async availability checks |
| **Disabled submit until form is "valid"** | User cannot tell *why* it is disabled; gives no error path | Allow submit; surface field-level errors on attempt; auto-focus the first invalid field |
| **Submit buttons that double-fire** | Network race conditions; duplicate records | Disable + show loading on submit; idempotency key on the request |
| **Page jump on route change without focus management** | Screen-reader users stay on the old element | Move focus to main content or page heading after navigation |
| **Touch target < 24×24 CSS px on web** (or < 44×44 pt iOS / 48×48 dp Android) | Mistaps; fails WCAG 2.2 SC 2.5.8 | Expand hit area via padding or pseudo-element without changing visual size |
| **Drag-only interactions with no alternative** | Fails WCAG 2.2 SC 2.5.7; impossible for users with motor limitations | Provide a non-drag alternative (buttons, menu) for every drag action |
| **Scroll-hijacking** (custom wheel handlers, locked scroll regions) | Breaks momentum scrolling, screen-reader scrolling, browser find-in-page | Trust the platform scroll; only intercept for proven UX wins (parallax narrative, lightbox) |
| **Sticky elements covering the focused control** | Fails WCAG 2.2 SC 2.4.11 | Use `scroll-margin-top` / `scroll-padding-top` so focused elements stay visible |
| **Ambiguous loading state** (button looks identical loading vs idle) | User clicks again → duplicate submission | Spinner inside the button + disabled + label change ("Saving…") |
| **`outline: none` without replacement** | Destroys keyboard accessibility | Replace with `:focus-visible` ring using the design-token shadow |

---

## Implementation Micro-rules

Specific rules derived from Vercel web-interface-guidelines and addyosmani/web-quality-skills.
These are quick wins that prevent the most common accessibility, performance, and UX bugs.

### Focus and Keyboard

```css
/* Always use :focus-visible — only shows ring for keyboard, not mouse */
.button:focus-visible {
  outline: 2px solid var(--shadow-focus);
  outline-offset: 2px;
}

/* Never do this — removes focus ring for keyboard users */
.button:focus { outline: none; }
```

```tsx
// Icon-only buttons always need aria-label
<button aria-label="Close dialog" onClick={onClose}>
  <CloseIcon aria-hidden="true" />
</button>
```

### Forms

```tsx
// Inputs need autocomplete + name for password managers and autofill
<input
  type="email"
  name="email"
  autoComplete="email"
  aria-label="Email address"
/>

// Always associate label with input — never rely on placeholder alone
<label htmlFor="pipeline-name">Pipeline name</label>
<input id="pipeline-name" type="text" />

// Never block paste — users paste passwords, OTP codes, and data
// Remove: onPaste={e => e.preventDefault()}

// On form submit with errors: focus the first error field
function handleSubmit(e: React.FormEvent) {
  e.preventDefault();
  const firstError = formRef.current?.querySelector('[aria-invalid="true"]');
  (firstError as HTMLElement)?.focus();
}
```

### Animation

```css
/* Only animate transform and opacity — compositor-thread only */
.panel {
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1),
              opacity   150ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Never animate layout properties */
/* BAD: .panel { transition: height 200ms; } */
/* BAD: .panel { transition: margin 200ms; } */

/* Always respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  .panel { transition: none; }
}
```

### Typography

```css
/* Balance heading line breaks — prevents orphaned words */
h1, h2, h3 { text-wrap: balance; }

/* Align number columns in tables and dashboards */
.metric-value, td.numeric { font-variant-numeric: tabular-nums; }
```

### Navigation and URL State

```tsx
// Deep-linkable state belongs in the URL, not in useState
// Use <Link> for navigation — never <div onClick={() => navigate(...)}>

// Bad: state in React, not URL — not shareable, not bookmarkable
const [activeTab, setActiveTab] = useState('overview');

// Good: state in URL — shareable, bookmarkable, browser-back works
const [searchParams, setSearchParams] = useSearchParams();
const activeTab = searchParams.get('tab') ?? 'overview';
```

### Destructive Actions

```tsx
// Always confirm before irreversible operations
function DeletePipelineButton({ onConfirm }: { onConfirm: () => void }) {
  const [showConfirm, setShowConfirm] = useState(false);
  return (
    <>
      <Button intent="danger" onClick={() => setShowConfirm(true)}>
        Delete pipeline
      </Button>
      {showConfirm && (
        <ConfirmationModal
          title="Delete pipeline?"
          description="This action cannot be undone."
          confirmLabel="Delete"
          onConfirm={onConfirm}
          onCancel={() => setShowConfirm(false)}
        />
      )}
    </>
  );
}
```

### Dynamic Content

```tsx
// Announce non-critical async updates to screen readers
<div aria-live="polite" aria-atomic="true">
  {uploadStatus && <p>{uploadStatus}</p>}
</div>

// Announce errors immediately
<div role="alert">
  {error && <p>{error.message}</p>}
</div>
```

---

## Compound Component Pattern

Use when a component family needs flexible internal composition without a proliferation of
boolean props. Replaces: `<Tabs activeTab="x" showBorder hideIcons verticalLayout />`.

```typescript
// Context holds shared state
interface TabsContextValue {
  readonly activeTab: string;
  readonly setActiveTab: (id: string) => void;
}
const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Must be used inside <Tabs>');
  return ctx;
}

// Root component owns the state
function Tabs({ defaultTab, children }: { defaultTab: string; children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className={styles.tabs}>{children}</div>
    </TabsContext.Provider>
  );
}

// Sub-components consume the context
function TabList({ children }: { children: React.ReactNode }) {
  return <div role="tablist" className={styles.tabList}>{children}</div>;
}

function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
      className={`${styles.tab} ${activeTab === id ? styles.active : ''}`}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab } = useTabsContext();
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
}

// Attach sub-components to root for ergonomic usage
Tabs.List  = TabList;
Tabs.Tab   = Tab;
Tabs.Panel = TabPanel;

// Consumer usage — composition, no boolean props
<Tabs defaultTab="overview">
  <Tabs.List>
    <Tabs.Tab id="overview">Overview</Tabs.Tab>
    <Tabs.Tab id="stages">Stages</Tabs.Tab>
    <Tabs.Tab id="logs">Logs</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel id="overview"><OverviewContent /></Tabs.Panel>
  <Tabs.Panel id="stages"><StagesContent /></Tabs.Panel>
  <Tabs.Panel id="logs"><LogsContent /></Tabs.Panel>
</Tabs>
```

**When to use compound components**: Navigation (Tabs, Accordion, Menu), form field
families, multi-step containers. **When not to**: Simple standalone components — compound
pattern adds ceremony that is not justified for a single component.

---

## React 19 Patterns

### `use()` Hook for Promises

```typescript
// React 19: unwrap a promise inside a component (must be wrapped in Suspense)
import { use } from 'react';

function PipelineDetails({ pipelinePromise }: { pipelinePromise: Promise<Pipeline> }) {
  const pipeline = use(pipelinePromise);  // Suspends until resolved
  return <div>{pipeline.name}</div>;
}

// Parent wraps with Suspense
<Suspense fallback={<PipelineSkeleton />}>
  <PipelineDetails pipelinePromise={fetchPipeline(id)} />
</Suspense>
```

### Form Actions (React 19)

```typescript
// React 19: useActionState replaces manual isPending + error state for form submissions
import { useActionState } from 'react';

async function submitPipelineAction(
  previousState: ActionState,
  formData: FormData,
): Promise<ActionState> {
  const name = formData.get('name') as string;
  try {
    await createPipeline({ name });
    return { status: 'success' };
  } catch (error) {
    return { status: 'error', message: 'Failed to create pipeline' };
  }
}

function CreatePipelineForm() {
  const [state, action, isPending] = useActionState(submitPipelineAction, { status: 'idle' });
  return (
    <form action={action}>
      <input name="name" type="text" required />
      {state.status === 'error' && <p role="alert">{state.message}</p>}
      <Button type="submit" loading={isPending}>Create</Button>
    </form>
  );
}
```

### `useOptimistic` for Instant Feedback

```typescript
// Optimistically update UI before server confirms
import { useOptimistic } from 'react';

function PipelineList({ pipelines, onDelete }: PipelineListProps) {
  const [optimisticPipelines, removeOptimistically] = useOptimistic(
    pipelines,
    (current, idToRemove: string) => current.filter(p => p.id !== idToRemove),
  );

  const handleDelete = async (id: string) => {
    removeOptimistically(id);   // Instant UI update
    await deletePipeline(id);   // Server call — UI already reflects the change
  };

  return (
    <ul>
      {optimisticPipelines.map(p => (
        <PipelineItem key={p.id} pipeline={p} onDelete={handleDelete} />
      ))}
    </ul>
  );
}
```
