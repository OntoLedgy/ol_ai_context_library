# Mobile and Touch

Applies to **mobile web** and **React Native**. Web on desktop inherits the
WCAG 2.2 AA target-size rule (24×24 CSS px) but is not subject to most of this
reference.

The web-first rules in `component-standards.md`, `performance.md`, and
`pre-delivery.md` continue to apply. This file adds the mobile-specific
constraints they omit.

---

## Touch Target Sizes

| Platform | Minimum | Comfortable | Notes |
|----------|---------|-------------|-------|
| iOS | 44×44 pt | 48×48 pt | Apple HIG; applies to the *hit area*, not the *visual* element |
| Android | 48×48 dp | 56×56 dp | Material Design; same hit-area rule |
| Web (WCAG 2.2 SC 2.5.8) | 24×24 CSS px | 44×44 CSS px | Mobile web should still aim for the iOS/Android targets |

**Spacing between targets**: minimum 8 px / 8 dp gap. Adjacent tappable elements
without a gap cause mistaps regardless of individual size.

The hit area can extend beyond the visual element using padding or a
pseudo-element. A 24-px icon button is acceptable if its hit area is 44 px.

```css
/* Visual 24px icon, 44px hit area */
.icon-button {
  width: 24px;
  height: 24px;
  position: relative;
}
.icon-button::before {
  content: '';
  position: absolute;
  inset: -10px;       /* expands hit area to 44×44 */
}
```

```tsx
// React Native equivalent
<Pressable
  hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
  style={{ width: 24, height: 24 }}
>
  <Icon />
</Pressable>
```

---

## Safe Areas and Insets

Always reserve space for system UI. Do not place tappable elements inside the
status bar, home-indicator area, or under fixed navigation/tab bars.

**Web (mobile)**:

```css
.app-shell {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

/* Use min-h-dvh, not 100vh — accounts for dynamic browser chrome */
.full-height {
  min-height: 100dvh;
}
```

**React Native**:

```tsx
import { SafeAreaView } from 'react-native-safe-area-context';

<SafeAreaView edges={['top', 'bottom']} style={{ flex: 1 }}>
  {/* content */}
</SafeAreaView>
```

Required reservations:

- Status bar at top
- Notch / Dynamic Island (iPhone)
- Home indicator at bottom (iPhone X+)
- Three-button or gesture nav bar (Android)
- Fixed app headers and bottom tab bars

Lists must add bottom content insets so the last row is not hidden behind a
fixed bottom tab bar or system gesture area.

---

## Gesture Conflicts

Mobile platforms reserve specific edge regions for system gestures. Avoid
placing custom gestures in those regions.

| Platform | Reserved gesture | Region |
|----------|------------------|--------|
| iOS | Swipe-from-left → back navigation | Left edge, ~20 pt wide |
| iOS | Swipe-from-bottom → home / app switcher | Bottom edge, ~20 pt tall |
| Android | Swipe-from-left/right → back | Both side edges (gesture nav mode) |
| Android | Swipe-from-bottom → home / overview | Bottom edge |

Rules:

- Horizontal swipe gestures inside content (carousels, swipe-to-delete) must
  start their hit region at least 20 pt away from the screen edge
- Drawers that open from the edge should accept a tap-on-handle as well as
  swipe-from-edge, because edge swipe conflicts with system back
- Vertical scroll containers nested inside horizontal swipers cause mistaps —
  prefer either/or, not both, in the same region
- A movement threshold (≥ 8 dp) must be exceeded before a drag activates,
  so taps are not accidentally interpreted as drags

---

## Press Feedback

Every tappable element provides feedback within 80–150 ms — earlier than the
user's brain registers the action as having happened.

| Surface | Feedback |
|---------|----------|
| iOS | Subtle scale (0.96–0.98) + opacity (0.7) for icon buttons; system blue overlay for list rows |
| Android | Material ripple from the touch point |
| Web (mobile) | `:active` background or `transform: scale(0.97)` |

Feedback rules:

- Use `transform` and `opacity` only — never animate `width`, `height`, `margin`,
  or `padding` on press (causes layout shift)
- Pressed state must remain visible while the finger is down, even on fast taps
- Cancel the pressed state if the user drags off the element before releasing
- React Native: `Pressable` over `TouchableOpacity` (more control over states)

---

## Haptic Feedback

Use sparingly and only where it adds information.

| When | What |
|------|------|
| Confirming destructive action | iOS warning, Android `EFFECT_HEAVY_CLICK` |
| Successful submission | iOS success, Android `EFFECT_DOUBLE_CLICK` |
| Selection change in a picker | iOS selection, Android `EFFECT_TICK` |
| Error / form rejection | iOS error |

Forbidden: haptic on every button press, haptic on scroll, haptic on hover-equivalent.

Respect the system "Reduce Motion" / "System Haptics" toggle — fall back to
no haptic when disabled.

---

## Dynamic Type / System Text Scaling

Users can scale system text up to ~310% on iOS and ~200% on Android. Layouts
must not break.

- Never set fixed pixel `height` on text containers — let them grow
- Use platform-relative sizing: iOS Dynamic Type styles (Title, Body, Caption,
  …) and Material type roles (`displayLarge`, `bodyMedium`, …)
- Avoid `numberOfLines={1}` on user-content text; truncation at large scales
  hides information
- Test at largest accessibility size before sign-off
- Web: use `rem` for type sizes, never `px`, so user font-size preference applies

---

## Reduced Motion

`prefers-reduced-motion: reduce` (web) and `UIAccessibilityIsReduceMotionEnabled` /
`AccessibilityInfo.isReduceMotionEnabled()` (React Native) must be honoured.

When reduced motion is on:

- Disable parallax, large translations, and bounce effects
- Replace animated transitions with instant state changes or short fades (≤ 100 ms)
- Disable shared-element transitions
- Keep functional motion (loading spinners) but avoid decorative motion

```tsx
// React Native
import { AccessibilityInfo } from 'react-native';

const [reduceMotion, setReduceMotion] = useState(false);
useEffect(() => {
  AccessibilityInfo.isReduceMotionEnabled().then(setReduceMotion);
  const sub = AccessibilityInfo.addEventListener('reduceMotionChanged', setReduceMotion);
  return () => sub.remove();
}, []);
```

---

## Mobile Forms

- Use semantic input types so the OS surfaces the right keyboard:

  | Field | `inputMode` (web) | `keyboardType` (RN) |
  |-------|-------------------|---------------------|
  | Email | `email` | `email-address` |
  | Phone | `tel` | `phone-pad` |
  | Number (no decimals) | `numeric` | `number-pad` |
  | Number (decimals) | `decimal` | `decimal-pad` |
  | URL | `url` | `url` |
  | Search | `search` | `web-search` |

- Set `autoComplete` (web) / `textContentType` (iOS) / `autoComplete` (Android)
  for autofill and password-manager support
- Avoid blocking `onPaste` — users paste OTP codes, passwords, addresses
- Input height ≥ 44 pt on mobile
- One input per row on phones; never two-column forms below 600 px width
- Keyboard must not cover the focused input — scroll the form on focus
- "Done" / "Submit" / "Next" return-key labels reflect what the key actually does

---

## Navigation Patterns

| Pattern | When | Limit |
|---------|------|-------|
| Bottom tab bar | Top-level destinations | Max 5 items; iOS HIG / Material |
| Drawer (hamburger) | Secondary destinations | Avoid as primary nav on mobile-first apps; users miss it |
| Stack navigation | Hierarchical drilldown | Always provide a back affordance — system back alone is not enough |
| Modal | Self-contained tasks | Never use for primary navigation |

Rules:

- Highlight the current tab — icon + label, not just colour
- Do not mix tab bar + sidebar + bottom nav at the same hierarchy level
- Back behaviour is predictable: always returns to the previous screen with
  scroll position and state restored
- Deep linking works for every shareable screen
- After a route change, move focus to the main content (or the heading) for
  screen reader users

---

## Network and Offline

Mobile networks are intermittent. Plan for it.

- Show offline state explicitly when network is unavailable; do not silently fail
- Cache last-known-good data and show it with a "stale" indicator while refetching
- Submit actions must be retryable; queue them locally if offline
- Show request timeout feedback (≥ 10 s without response)
- Lazy-load images below the fold; respect `prefers-reduced-data` where set
- React Query: configure `staleTime`, `gcTime`, and `retry` per query class —
  don't accept defaults

---

## Vector Icons and Assets

- Use vector icons (SVG on web, `react-native-svg` or platform vector libraries
  on RN). Bitmap icons pixelate and ship multiple resolutions
- Apply consistent stroke width within a hierarchy level
- Provide `accessibilityLabel` (RN) or `aria-label` (web) on icon-only controls
- Brand assets at correct proportions; never stretch logos
- App icon and splash screen are platform-native, not webview-rendered

---

## React Native Specifics

- Prefer platform primitives: `Pressable`, `TextInput`, `FlatList`, `SectionList`
  over custom equivalents
- `FlatList` over `ScrollView` for any list with >10 items
  (`ScrollView` renders all children at mount; `FlatList` virtualises)
- Use `react-native-safe-area-context`, not the deprecated built-in `SafeAreaView`
- Platform-conditional UI via `Platform.OS` checks; do not render iOS-style
  controls on Android (and vice-versa)
- Accessibility props: `accessibilityRole`, `accessibilityLabel`,
  `accessibilityHint`, `accessibilityState`
- Test on a real device, not only the simulator — touch latency, haptics, and
  gesture handling differ
