# Data Visualisation Implementation

## Library Conventions

Use the library specified in the approved `ui-architect` design. The default for new
projects is **Recharts**. See the architect's `data-visualisation-strategy.md` for
the selection rationale and the library decision.

---

## Recharts Patterns (Default)

### Base Chart Wrapper

Wrap every chart in a responsive container and extract chart logic to a custom hook:

```typescript
interface LineChartProps {
  readonly data: TimeSeriesPoint[];
  readonly xAxisKey: string;
  readonly yAxisKey: string;
  readonly label: string;
  readonly height?: number;
}

function TimeSeriesLineChart({ data, xAxisKey, yAxisKey, label, height = 300 }: LineChartProps) {
  return (
    <figure aria-label={label} role="img">
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-neutral-200)" />
          <XAxis dataKey={xAxisKey} tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey={yAxisKey}
            stroke="var(--color-brand-primary)"
            dot={false}           // Remove dots for large datasets
            isAnimationActive={false}  // Disable for real-time data
          />
        </LineChart>
      </ResponsiveContainer>
      <figcaption className={styles.srOnly}>{label}</figcaption>
    </figure>
  );
}
```

### Chart Type Implementations

**Bar Chart (categorical comparison)**:
```typescript
function CategoryBarChart({ data, categoryKey, valueKey, label }: BarChartProps) {
  return (
    <figure aria-label={label} role="img">
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={categoryKey} />
          <YAxis />
          <Tooltip />
          <Bar dataKey={valueKey} fill="var(--color-brand-primary)" />
        </BarChart>
      </ResponsiveContainer>
      <figcaption className={styles.srOnly}>{label}</figcaption>
    </figure>
  );
}
```

**KPI Card (single metric)**:
```typescript
interface KpiCardProps {
  readonly label: string;
  readonly value: string | number;
  readonly trend?: 'up' | 'down' | 'neutral';
  readonly intent?: 'success' | 'danger' | 'warning' | 'neutral';
}

function KpiCard({ label, value, trend, intent = 'neutral' }: KpiCardProps) {
  return (
    <article className={`${styles.kpiCard} ${styles[intent]}`} aria-label={`${label}: ${value}`}>
      <span className={styles.label}>{label}</span>
      <span className={styles.value}>{value}</span>
      {trend && <TrendIndicator direction={trend} aria-hidden="true" />}
    </article>
  );
}
```

---

## Real-Time Chart Implementation

### Data Buffer Hook

Manage the rolling window of live data in a hook — keep it out of the component:

```typescript
interface RealTimeBufferOptions {
  readonly maxPoints: number;
  readonly wsUrl: string;
  readonly parseMessage: (event: MessageEvent) => DataPoint;
}

function useRealTimeBuffer({ maxPoints, wsUrl, parseMessage }: RealTimeBufferOptions) {
  const [buffer, setBuffer] = useState<DataPoint[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectDelayRef = useRef(1000);

  const connect = useCallback(() => {
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnectionStatus('connected');
      reconnectDelayRef.current = 1000;  // Reset backoff on successful connection
    };

    ws.onmessage = event => {
      const point = parseMessage(event);
      setBuffer(prev => {
        const updated = [...prev, point];
        return updated.length > maxPoints ? updated.slice(-maxPoints) : updated;
      });
    };

    ws.onclose = () => {
      setConnectionStatus('disconnected');
      // Exponential backoff reconnection
      setTimeout(() => {
        reconnectDelayRef.current = Math.min(reconnectDelayRef.current * 2, 30000);
        connect();
      }, reconnectDelayRef.current);
    };
  }, [wsUrl, maxPoints, parseMessage]);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  return { buffer, connectionStatus } as const;
}
```

### Real-Time Line Chart

```typescript
function LiveMetricChart({ wsUrl, label }: LiveMetricChartProps) {
  const { buffer, connectionStatus } = useRealTimeBuffer({
    maxPoints: 500,
    wsUrl,
    parseMessage: event => JSON.parse(event.data as string) as DataPoint,
  });

  // Memoize — only re-render when buffer reference changes
  const chartData = useMemo(() => buffer, [buffer]);

  return (
    <div className={styles.liveChartWrapper}>
      <ConnectionStatusBadge status={connectionStatus} />
      <TimeSeriesLineChart
        data={chartData}
        xAxisKey="timestamp"
        yAxisKey="value"
        label={label}
      />
    </div>
  );
}
```

---

## ECharts Patterns (Large Datasets)

Use ECharts when dataset exceeds 2,000 live points or SVG performance degrades:

```typescript
import ReactECharts from 'echarts-for-react';

function LargeDatasetChart({ data, label }: LargeDatasetChartProps) {
  const option = useMemo(() => ({
    xAxis: { type: 'category', data: data.map(d => d.timestamp) },
    yAxis: { type: 'value' },
    series: [{
      data: data.map(d => d.value),
      type: 'line',
      smooth: true,
      symbol: 'none',  // No dots — critical for performance at scale
      animation: false, // Disable animation for large/real-time data
    }],
    tooltip: { trigger: 'axis' },
  }), [data]);

  return (
    <figure aria-label={label} role="img">
      <ReactECharts option={option} style={{ height: 300 }} />
      <figcaption className={styles.srOnly}>{label}</figcaption>
    </figure>
  );
}
```

---

## Accessibility for Charts

Every chart must be accessible. A chart that is only a visual element is not sufficient:

```typescript
// Pattern: figure + figcaption + data table fallback
function AccessibleChart({ data, label, chartElement }: AccessibleChartProps) {
  const [showTable, setShowTable] = useState(false);

  return (
    <figure role="img" aria-label={label}>
      {chartElement}
      <figcaption>
        <button
          className={styles.dataTableToggle}
          onClick={() => setShowTable(prev => !prev)}
          aria-expanded={showTable}
          aria-controls="chart-data-table"
        >
          {showTable ? 'Hide data table' : 'Show data as table'}
        </button>
        {showTable && (
          <table id="chart-data-table">
            {/* Render data in tabular form for screen readers */}
          </table>
        )}
      </figcaption>
    </figure>
  );
}
```

Rules:
- Every chart has `role="img"` and `aria-label` describing what it shows
- Every chart has a `<figcaption>` (can be `sr-only` if the title is visually clear)
- Complex charts (multi-series, interactive) offer a data table view
- Colour is never the only encoding — use labels, patterns, or shapes as secondary encoding
- Interactive chart elements (tooltips, zoom) are keyboard accessible

---

## Empty and Loading States

Design these before implementing the chart:

```typescript
function ChartPanel({ isLoading, error, data, label }: ChartPanelProps) {
  if (isLoading) {
    return <ChartSkeleton height={300} aria-label={`Loading ${label}`} />;
  }
  if (error) {
    return (
      <ChartError
        message="Could not load chart data"
        onRetry={handleRetry}
        aria-label={`Error loading ${label}`}
      />
    );
  }
  if (data.length === 0) {
    return (
      <ChartEmpty
        message="No data available for this period"
        aria-label={`No data for ${label}`}
      />
    );
  }
  return <TimeSeriesLineChart data={data} label={label} />;
}
```

---

## Performance Rules

| Rule | Reason |
|------|--------|
| `isAnimationActive={false}` for real-time data | Animations block re-renders at high update frequency |
| `symbol="none"` for line charts with > 100 points | Individual dots are expensive to render at scale |
| `useMemo` for chart data derivation | Prevents unnecessary re-computation on unrelated state changes |
| `React.memo` on chart components | Prevents re-render when parent state changes but chart data has not |
| Single `ResponsiveContainer` per chart | Multiple responsive containers in one render are expensive |
| Virtualise tables with > 1,000 rows | Use `@tanstack/react-virtual` — rendering all rows at once is O(n) render cost |
