# Aesthetic Quality Standards

This reference applies primarily during **Library Maintenance Mode** — designing new
`ol_ui_library` components, reviewing component visual quality, or auditing existing
components for generic "AI-produced" aesthetics.

---

## The Quality Test

Before finalising any component design, apply this test:

> *"If you showed this to someone and said 'AI made this,' would they believe you immediately?"*

If yes — the design needs rework. Components should feel **intentionally crafted**, not
generated from a template. This is not about complexity; it is about intent.

---

## Anti-patterns to Reject ("AI Slop")

These patterns are signals of generic, low-quality AI output. Reject them in design reviews
and in `ol_ui_library` contributions:

| Anti-pattern | Why it fails | Alternative |
|-------------|-------------|-------------|
| **Glassmorphism** (frosted glass everywhere) | Overused since 2021; no semantic meaning | Solid surfaces with purposeful depth via shadow tokens |
| **Rounded rectangle cards with drop shadows** as the only layout unit | Creates visual monotony; everything looks the same | Mix layout types: inset panels, ruled sections, full-bleed bands |
| **Nested cards** (card inside card inside card) | Creates visual clutter; unclear hierarchy | Use spacing and typography to create hierarchy without boxing |
| **Gradient text on headings** | Reduces legibility; cliché | Use colour contrast and weight instead |
| **Hero metric layout** (giant number, tiny label below) | No hierarchy when everything uses the same pattern | Differentiate with size scale, intent colours, and grouping |
| **Cyan on dark** or **neon accent on dark** | Overused in "developer dashboards" | Build a full palette from brand identity; avoid defaults |
| **Symmetric centred layouts** for everything | Static, predictable; feels templated | Vary alignment; use asymmetry intentionally in hero regions |
| **Repetitive card grids** (12 identical cards) | No visual rhythm; user cannot scan | Vary card sizes; group by importance; use list and table views for dense data |
| **Redundant information** (icon + label + tooltip all saying the same thing) | Noise without signal | Use label OR icon; reserve tooltips for non-obvious actions |

---

## Typography

Typography is the fastest way to make an interface feel distinctive or generic.

### Rules

| Rule | Detail |
|------|--------|
| **Use a distinctive typeface** | Avoid defaulting to Inter or system-ui; choose a face that carries the product's personality |
| **Clear hierarchy** | At minimum three distinct sizes with weight differentiation; headings must not look like body text |
| **Avoid font overload** | Maximum two typefaces per interface: one display/heading, one body/UI |
| **`text-wrap: balance` on headings** | Prevents awkward single-word orphan lines; browser-native in 2025+ |
| **`tabular-nums` for data** | All number columns use `font-variant-numeric: tabular-nums` so digits align |
| **Typographic quotes** | Use `"…"` and `'…'` (curly), not `"..."` and `'...'` (straight ASCII) |
| **Non-breaking spaces** | Use `&nbsp;` between numbers and units (`5 MB`, `3 items`) and in brand names |
| **Line length** | 60–75 characters per line for body text; shorter for UI labels |

### Forbidden

```css
/* Forbidden: gradient text — reduces legibility */
.heading {
  background: linear-gradient(to right, #06b6d4, #8b5cf6);
  -webkit-background-clip: text;
  color: transparent;
}

/* Forbidden: Inter as default with no personality */
font-family: 'Inter', system-ui, sans-serif; /* acceptable only if Inter is the brand choice */
```

---

## Colour

### Build a Cohesive Palette

A cohesive palette has:
- **One brand colour** — used sparingly, carries maximum visual weight
- **Tinted neutrals** — not pure `#f5f5f5` grey; slightly tinted toward the brand hue
- **Semantic colours** — success, error, warning, info — derived from the palette, not defaults
- **Maximum 5–6 distinct hues** in use at any one time

### Modern CSS: OKLCH

Use OKLCH for colour definitions in `ol_ui_library` tokens. OKLCH is **perceptually uniform**
— changing the lightness value produces predictable results; hues stay vivid at all lightness levels.

```css
/* Avoid: HSL — not perceptually uniform; saturation behaves differently per hue */
:root {
  --color-brand-primary: hsl(220, 90%, 50%);
}

/* Prefer: OKLCH — predictable lightness, consistent chroma across hues */
:root {
  --color-brand-primary: oklch(55% 0.22 250);    /* L: 0–100%, C: chroma, H: hue */
  --color-brand-light:   oklch(92% 0.05 250);    /* Same hue, high lightness */
  --color-brand-dark:    oklch(35% 0.22 250);    /* Same hue, low lightness */
}
```

### Tint Neutrals Toward Brand

```css
/* Generic: pure grey — feels disconnected from brand */
--color-surface: oklch(97% 0 0);

/* Better: tinted neutral — surface feels part of the same palette */
--color-surface: oklch(97% 0.01 250);   /* Barely perceptible blue tint matching brand hue */
```

### Rules

- Never pure black (`#000000`) — use near-black tinted toward the brand hue
- Never pure white (`#ffffff`) — use near-white tinted toward the brand hue
- Colour alone never encodes information (WCAG requirement; see accessibility section)
- WCAG AA contrast minimum (4.5:1) on all text; 3:1 on large text and UI components

---

## Layout and Visual Rhythm

Generic interfaces apply the same spacing and layout treatment to everything. Distinctive
interfaces vary treatment to create **hierarchy and rhythm**.

### Rules

| Rule | Detail |
|------|--------|
| **Vary spatial rhythm** | Mix tight and loose spacing to signal grouping and importance |
| **Embrace asymmetry** | Centred layouts feel static; left-weighted or asymmetric layouts feel dynamic |
| **Use full-bleed bands** | Not everything should be in a card; full-width colour bands create strong section breaks |
| **Limit card depth** | Maximum 1 level of card nesting; replace the second level with spacing and dividers |
| **Grid variation** | Not every grid should be 3 or 4 equal columns; vary column widths to create visual interest |

### Avoid Templated Page Structures

```
// Templated (generic):          // Distinctive:
[Hero]                           [Full-bleed asymmetric hero]
[3-column card grid]             [Wide primary card + 2 secondary]
[3-column card grid]             [Ruled list with typographic hierarchy]
[3-column card grid]             [Metrics band with varied sizing]
[Footer]                         [Footer]
```

---

## Motion and Animation

Motion communicates state change. It is not decoration.

### Rules

| Rule | Detail |
|------|--------|
| **Animate only `transform` and `opacity`** | These run on the compositor thread; do not trigger layout or paint |
| **Never `transition: all`** | Animates every property including ones that cause layout reflow |
| **Exponential easing** | `cubic-bezier(0.4, 0, 0.2, 1)` (Material Design standard) for most transitions |
| **Short durations** | UI feedback: 100–150ms; element entry: 200–300ms; page transitions: 300–400ms |
| **Make animations interruptible** | User should be able to trigger the reverse transition before the first completes |
| **`prefers-reduced-motion`** | All animations must be disabled or significantly reduced when this media query is set |

```css
/* Correct: only transform and opacity; respects reduced motion */
.card {
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1),
              opacity   200ms cubic-bezier(0.4, 0, 0.2, 1);
}
.card:hover {
  transform: translateY(-2px);
}

/* Forbidden: transition all, animates layout properties */
.card {
  transition: all 0.3s ease;
}
.card:hover {
  margin-top: -4px;     /* Triggers layout — causes CLS */
}

/* Required: reduced motion override */
@media (prefers-reduced-motion: reduce) {
  .card { transition: none; }
}
```

---

## Modern CSS Techniques

### Container Queries (preferred over media queries for components)

Components should adapt to their **container size**, not the viewport size. A card does not
know if it is in a sidebar or a main column; its container does.

```css
/* Adapt to container, not viewport */
.chart-panel {
  container-type: inline-size;
}

@container (min-width: 600px) {
  .chart-panel__legend {
    display: flex;
    flex-direction: row;   /* Horizontal legend when panel is wide enough */
  }
}

@container (max-width: 599px) {
  .chart-panel__legend {
    display: none;         /* Hide legend on narrow containers */
  }
}
```

### `text-wrap: balance`

```css
/* Prevent orphaned words on headings */
h1, h2, h3 {
  text-wrap: balance;
}
```

### `font-variant-numeric: tabular-nums`

```css
/* All number columns in tables and dashboards */
.metric-value,
td.numeric {
  font-variant-numeric: tabular-nums;
}
```

---

## Aesthetic Quality Review Checklist

Use during Library Maintenance Mode component reviews:

| Check | Pass Condition |
|-------|---------------|
| AI slop test | Would not be immediately identified as AI-generated |
| No glassmorphism | Not present, or justified with a specific rationale |
| No nested cards | Maximum 1 level of card nesting |
| No gradient text | Headings use colour and weight for hierarchy, not gradients |
| Typography distinctiveness | Not defaulting to Inter/system-ui without brand rationale |
| `text-wrap: balance` on headings | Applied in CSS |
| `tabular-nums` on numeric data | Applied in CSS |
| OKLCH colour tokens | New token values use OKLCH |
| Tinted neutrals | Neutrals have a slight hue tint, not pure grey |
| `transform`/`opacity` only animations | No `margin`, `height`, `width`, `top` in transitions |
| `prefers-reduced-motion` | All animated components override when set |
| Container queries | Components use container queries over viewport media queries |
