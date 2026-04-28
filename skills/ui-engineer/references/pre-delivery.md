# Pre-Delivery Checklist

Runs **after** the automated Quality Gates (`tsc`, `eslint`, `prettier`, `vitest`,
`playwright`, `storybook build`, `lighthouse`) pass.

Quality Gates verify that the code is **correct**. This checklist verifies that
the feature is **ready to ship** — visual quality, interaction feel, accessibility
in practice, and design-system fit. It is walked through manually (or against a
running preview) before declaring an implementation complete.

If any item fails, the implementation is not complete. Either fix it or capture
it as a follow-up issue with explicit user acknowledgement before handing back.

---

## 1. Visual Quality

- [ ] No emoji icons used as structural icons; SVG (Lucide / Heroicons / library set) only
- [ ] Icon family is consistent within the feature; stroke weight matches surrounding icons
- [ ] No glassmorphism, no gradient text on headings, no nested cards (see `ui-architect/references/aesthetic-quality.md`)
- [ ] Hierarchy carried by size + weight + spacing — not by colour alone
- [ ] Whitespace is intentional; not the default IDE auto-format leftovers
- [ ] No "AI-default" tells: purple-on-white gradient, generic centred hero, twelve identical cards in a grid

## 2. Library Compliance

- [ ] All atoms used from `ol_ui_library` where they exist; no re-implementations
- [ ] Any custom component justified in the design doc; not a duplicate of a library component
- [ ] Design tokens (colour, spacing, radius, shadow) used — no hard-coded hex / px values for tokenable properties
- [ ] If a new pattern was discovered during implementation, a library-extension issue is filed

## 3. Accessibility (WCAG 2.2 AA, visible verification)

- [ ] Tab through the feature using keyboard only — every interactive element is reachable
- [ ] Focus order matches the visual reading order
- [ ] `:focus-visible` ring is present on every focusable element (no `outline: none` without replacement)
- [ ] Sticky/fixed elements never obscure the focused element (WCAG 2.2 SC 2.4.11)
- [ ] Drag operations have a non-drag alternative (WCAG 2.2 SC 2.5.7)
- [ ] All target sizes ≥ 24×24 CSS px on web (WCAG 2.2 SC 2.5.8); ≥ 44×44 pt on iOS, ≥ 48×48 dp on Android
- [ ] Icon-only buttons have `aria-label`; decorative icons have `aria-hidden="true"`
- [ ] Form inputs have associated `<label>` elements; placeholder is never the only label
- [ ] Colour is never the sole carrier of meaning (status, validity, selection)
- [ ] Non-critical async updates announced via `aria-live="polite"`; errors via `role="alert"`
- [ ] Heading hierarchy is sequential (no jump from h1 to h3)
- [ ] Modal traps focus on open and restores focus to the trigger on close
- [ ] `prefers-reduced-motion` honoured by every animation
- [ ] Tested at 200% zoom and at the user's largest system font setting

## 4. Contrast (light AND dark themes)

- [ ] Body text contrast ≥ 4.5:1 in both themes
- [ ] Large text (≥18pt or ≥14pt bold) ≥ 3:1 in both themes
- [ ] Interactive UI components (buttons, inputs, focus rings) ≥ 3:1 in both themes
- [ ] Error / success / warning states ≥ 4.5:1 in both themes
- [ ] Dividers and borders distinguishable in both themes
- [ ] Disabled state visually clear (reduced opacity 0.38–0.5) without dropping below contrast where text is still readable
- [ ] Modal scrim 40–60% black; foreground content remains legible

## 5. Interaction & Feedback

- [ ] Every button gives pressed-state feedback within 80–150 ms
- [ ] Press feedback uses `transform` / `opacity` only — no layout shift on press
- [ ] Async actions show a loading state within 100 ms; skeleton appears if loading exceeds 300 ms
- [ ] Submit buttons disable during in-flight request; do not allow double-submit
- [ ] Destructive actions (delete, deactivate, overwrite) require explicit confirmation
- [ ] Destructive actions offer an undo path where reversibility is possible
- [ ] Toasts auto-dismiss in 3–5 s and are announced via `aria-live`
- [ ] Errors are shown beside the offending field, not only in a top banner
- [ ] First invalid field is auto-focused after a failed submit

## 6. Forms

- [ ] Required fields marked
- [ ] Validation runs on `blur`, not on every keystroke (except inline character counters)
- [ ] Helper text below complex inputs; error text below the field
- [ ] `autoComplete` and semantic `type` attributes set for browser autofill and mobile keyboards
- [ ] Password fields offer show/hide; no `onPaste` blocking
- [ ] Long forms (>1 screen) auto-save and confirm before discarding unsaved changes
- [ ] Multi-step forms show progress (step N of M) and allow backward navigation without state loss

## 7. Responsive & Layout

- [ ] Verified on small phone (375×667), large phone (414×896), tablet (768×1024), desktop (1440+)
- [ ] Tested in portrait AND landscape on at least one mobile size
- [ ] No horizontal scroll at any breakpoint (unless intentional carousel/table)
- [ ] Mobile body text ≥ 16px; line length 35–60ch on mobile, 60–75ch on desktop
- [ ] 4 / 8 px spacing rhythm maintained
- [ ] Fixed headers / bottom bars use `min-h-dvh` (not `100vh`); content not hidden behind them
- [ ] Safe-area insets respected on iOS / Android (notch, Dynamic Island, home indicator)
- [ ] Container queries used where layout depends on container size, not viewport

## 8. Performance (Core Web Vitals spot-check on a real preview)

- [ ] LCP ≤ 2.5 s on a throttled "Fast 3G" Lighthouse run
- [ ] INP ≤ 200 ms across the primary interactions
- [ ] CLS ≤ 0.1 — images and async content reserve space
- [ ] No request waterfalls visible in the network panel for the critical path
- [ ] Lists with 50+ items virtualised
- [ ] Images use WebP/AVIF with explicit `width` / `height`
- [ ] Critical fonts preloaded; non-critical fonts use `font-display: swap`

## 9. Data Visualisation (only if charts are present)

- [ ] Chart type matches the question being answered (trend → line, comparison → bar, proportion → bar/donut, distribution → histogram)
- [ ] No pie chart with >5 categories
- [ ] Data palette ≥ 3:1 against background; labels ≥ 4.5:1
- [ ] Colour is supplemented by a second encoding (pattern, label, shape) for colour-blind users
- [ ] Legend interactive (click to toggle series) where it adds value
- [ ] Tooltips reachable by keyboard
- [ ] Empty / error / loading states designed and verified
- [ ] Numbers locale-formatted with `Intl.NumberFormat`; tabular-nums in tables
- [ ] Tables have `aria-sort` on sortable columns
- [ ] Export option (CSV / PNG) provided for analyst-facing surfaces

## 10. Mobile / React Native (only if mobile target)

Walk through `references/mobile-and-touch.md` before signing off.

## 11. Tests & Stories

- [ ] Tests cover loading / error / empty / populated states (not just the happy path)
- [ ] Storybook stories exist for every variant of every new `ol_ui_library` component
- [ ] Playwright journey test covers the primary flow end-to-end

---

## Sign-off

The implementation is ready to hand back when:

- All Quality Gates pass (`tsc`, `eslint`, `prettier`, `vitest`, `playwright`, `storybook build`, `lighthouse`)
- This checklist has been walked through against a running preview
- Any unchecked item has an explicit follow-up issue with user acknowledgement

If any item is unchecked and not captured as a follow-up, the implementation
is not complete. Do not declare success.
