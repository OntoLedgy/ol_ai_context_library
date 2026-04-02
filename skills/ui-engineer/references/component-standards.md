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
