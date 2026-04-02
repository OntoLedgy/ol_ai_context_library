# UX Journey Implementation Patterns

## Document Upload: Implementation

### File Selection Component

```typescript
interface DropZoneProps {
  readonly acceptedTypes: string[];   // e.g. ['.pdf', '.csv', 'application/json']
  readonly maxFileSizeBytes: number;
  readonly maxFileCount?: number;
  readonly onFilesSelected: (files: File[]) => void;
  readonly disabled?: boolean;
}

function DropZone({ acceptedTypes, maxFileSizeBytes, onFilesSelected, disabled }: DropZoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    setIsDragOver(false);
    const files = Array.from(event.dataTransfer.files);
    onFilesSelected(files);
  }, [onFilesSelected]);

  return (
    <div
      role="button"
      aria-label="Drop files here or click to browse"
      tabIndex={0}
      className={`${styles.dropZone} ${isDragOver ? styles.dragOver : ''}`}
      onDrop={handleDrop}
      onDragOver={e => { e.preventDefault(); setIsDragOver(true); }}
      onDragLeave={() => setIsDragOver(false)}
      onClick={() => inputRef.current?.click()}
      onKeyDown={e => e.key === 'Enter' && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        multiple
        accept={acceptedTypes.join(',')}
        className={styles.hiddenInput}
        onChange={e => onFilesSelected(Array.from(e.target.files ?? []))}
        aria-hidden="true"
        tabIndex={-1}
      />
      <UploadIcon aria-hidden="true" />
      <p>Drop files here or <span className={styles.browseLink}>browse</span></p>
      <p className={styles.hint}>
        Accepted: {acceptedTypes.join(', ')} · Max {formatBytes(maxFileSizeBytes)} per file
      </p>
    </div>
  );
}
```

### File Validation Hook

```typescript
interface FileValidationOptions {
  readonly acceptedTypes: string[];
  readonly maxFileSizeBytes: number;
  readonly maxFileCount?: number;
}

interface ValidatedFile {
  readonly file: File;
  readonly error: string | null;
}

function validateFiles(files: File[], options: FileValidationOptions): ValidatedFile[] {
  return files.map(file => ({
    file,
    error: getFileError(file, options),
  }));
}

function getFileError(file: File, options: FileValidationOptions): string | null {
  if (!isAcceptedType(file, options.acceptedTypes)) {
    return `${file.name}: file type not accepted`;
  }
  if (file.size > options.maxFileSizeBytes) {
    return `${file.name}: exceeds ${formatBytes(options.maxFileSizeBytes)} limit`;
  }
  return null;
}
```

### Upload State Machine

Use a discriminated union to model upload state — never a bag of boolean flags:

```typescript
type UploadState =
  | { status: 'idle' }
  | { status: 'validating' }
  | { status: 'ready'; files: ValidatedFile[] }
  | { status: 'uploading'; progress: Record<string, number> }
  | { status: 'complete'; results: UploadResult[] }
  | { status: 'partial'; results: UploadResult[] }
  | { status: 'failed'; error: string };
```

---

## Wizard / Multi-Step Form: Implementation

### Wizard State Management

```typescript
interface WizardState<TData> {
  readonly currentStep: number;
  readonly totalSteps: number;
  readonly data: Partial<TData>;
  readonly stepValidity: Record<number, boolean>;
}

function useWizard<TData>(totalSteps: number) {
  const [state, setState] = useState<WizardState<TData>>({
    currentStep: 0,
    totalSteps,
    data: {},
    stepValidity: {},
  });

  const goToNext = useCallback(() => {
    setState(prev => ({
      ...prev,
      currentStep: Math.min(prev.currentStep + 1, prev.totalSteps - 1),
    }));
  }, []);

  const goToPrevious = useCallback(() => {
    setState(prev => ({
      ...prev,
      currentStep: Math.max(prev.currentStep - 1, 0),
    }));
  }, []);

  const updateStepData = useCallback((stepData: Partial<TData>) => {
    setState(prev => ({ ...prev, data: { ...prev.data, ...stepData } }));
  }, []);

  const markStepValid = useCallback((step: number, valid: boolean) => {
    setState(prev => ({
      ...prev,
      stepValidity: { ...prev.stepValidity, [step]: valid },
    }));
  }, []);

  return { state, goToNext, goToPrevious, updateStepData, markStepValid } as const;
}
```

### Step Indicator Component

```typescript
interface StepIndicatorProps {
  readonly currentStep: number;
  readonly totalSteps: number;
  readonly stepLabels: string[];
}

function StepIndicator({ currentStep, totalSteps, stepLabels }: StepIndicatorProps) {
  return (
    <nav aria-label="Progress">
      <ol className={styles.steps}>
        {stepLabels.map((label, index) => (
          <li
            key={label}
            className={styles.step}
            aria-current={index === currentStep ? 'step' : undefined}
          >
            <span className={getStepClass(index, currentStep)} aria-hidden="true">
              {index + 1}
            </span>
            <span className={styles.stepLabel}>{label}</span>
          </li>
        ))}
      </ol>
      <p className={styles.srOnly}>
        Step {currentStep + 1} of {totalSteps}: {stepLabels[currentStep]}
      </p>
    </nav>
  );
}
```

### Form Validation (react-hook-form)

```typescript
// Per-step validation using react-hook-form
function PipelineConfigStep({ onComplete }: { onComplete: (data: ConfigData) => void }) {
  const { register, handleSubmit, formState: { errors } } = useForm<ConfigData>({
    mode: 'onBlur',  // Validate on blur for better UX than onChange
  });

  return (
    <form onSubmit={handleSubmit(onComplete)} noValidate>
      <FormField
        label="Pipeline name"
        error={errors.name?.message}
        required
      >
        <Input
          {...register('name', {
            required: 'Pipeline name is required',
            maxLength: { value: 100, message: 'Name must be 100 characters or fewer' },
          })}
          aria-describedby={errors.name ? 'name-error' : undefined}
        />
      </FormField>
      <WizardNavigation canProceed={!Object.keys(errors).length} />
    </form>
  );
}
```

---

## Pipeline Monitoring Dashboard: Implementation

### Status Polling Hook

```typescript
function usePipelineStatus(pipelineId: string) {
  return useQuery({
    queryKey: ['pipeline', pipelineId, 'status'],
    queryFn: () => fetchPipelineStatus(pipelineId),
    refetchInterval: query => {
      // Poll only while pipeline is running; stop when terminal state reached
      const status = query.state.data?.status;
      if (status === 'running' || status === 'queued') return 2000;
      return false;
    },
    staleTime: 0,
  });
}
```

### Real-Time Log Stream Hook

```typescript
function usePipelineLogStream(pipelineId: string, maxLines = 1000) {
  const [lines, setLines] = useState<LogLine[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(`/api/pipelines/${pipelineId}/logs`);
    wsRef.current = ws;

    ws.onmessage = event => {
      const newLine: LogLine = JSON.parse(event.data as string);
      setLines(prev => {
        const updated = [...prev, newLine];
        // Trim to max to prevent memory growth
        return updated.length > maxLines ? updated.slice(-maxLines) : updated;
      });
    };

    return () => ws.close();
  }, [pipelineId, maxLines]);

  return lines;
}
```

### Stage Progress Timeline

```typescript
function StageProgressTimeline({ stages }: { stages: PipelineStage[] }) {
  return (
    <ol className={styles.timeline} aria-label="Pipeline stages">
      {stages.map(stage => (
        <li key={stage.id} className={styles.stageItem}>
          <StageCard
            name={stage.name}
            status={stage.status}
            durationMs={stage.durationMs}
            recordCount={stage.recordCount}
          />
        </li>
      ))}
    </ol>
  );
}
```

---

## Results Dashboard: Implementation

### Filterable Data Table

```typescript
function useResultsFilter<T>(data: T[], filterFn: (item: T, query: string) => boolean) {
  const [query, setQuery] = useState('');

  const filteredData = useMemo(
    () => (query ? data.filter(item => filterFn(item, query)) : data),
    [data, query, filterFn],
  );

  return { filteredData, query, setQuery } as const;
}
```

### Empty State Pattern

Always design the empty state:

```typescript
function ResultsTable({ results }: { results: ProcessingResult[] }) {
  if (results.length === 0) {
    return (
      <EmptyState
        icon={<NoResultsIcon aria-hidden="true" />}
        title="No results found"
        description="The pipeline completed but produced no output records."
        action={<Button onClick={handleRetry}>Re-run pipeline</Button>}
      />
    );
  }
  return <DataTable data={results} />;
}
```

### Progressive Disclosure Pattern

Show summary first; reveal detail on demand:

```typescript
function ResultsSummary({ summary, onViewDetails }: ResultsSummaryProps) {
  return (
    <section aria-label="Processing summary">
      <MetricCard label="Records processed" value={summary.totalRecords} />
      <MetricCard label="Errors" value={summary.errorCount} intent={summary.errorCount > 0 ? 'danger' : 'success'} />
      <MetricCard label="Processing time" value={formatDuration(summary.durationMs)} />
      <Button variant="secondary" onClick={onViewDetails}>
        View detailed results
      </Button>
    </section>
  );
}
```

---

## Accessibility Rules for Journey Components

| Pattern | Implementation |
|---------|---------------|
| Wizard progress | `<nav aria-label="Progress">` with `aria-current="step"` on active step |
| File upload area | `role="button"`, `tabIndex={0}`, keyboard handler for `Enter` and `Space` |
| Status updates | `aria-live="polite"` region for non-critical updates; `aria-live="assertive"` for errors |
| Loading states | `aria-busy="true"` on the container; loading text for screen readers |
| Form errors | `aria-describedby` linking input to its error message; `role="alert"` on error summary |
| Dynamic content | Focus management on route/step change — move focus to the new heading |
