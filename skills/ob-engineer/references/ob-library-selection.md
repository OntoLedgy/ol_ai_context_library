# OB Library Selection

## How to Determine the Active Variant

Read the codebase's dependency declarations (e.g. `requirements.txt`, `pyproject.toml`):

| Signal | Variant |
|--------|---------|
| Imports or depends on `nf_common` | **BORO** — codebase is in a bCLEARer project |
| Imports or depends on `bclearer_pdk`, `ai`, or `ui` | **Ontoledgy** — codebase is in the Ontoledgy repo |

When uncertain, ask the user which variant applies before proceeding.

---

## BORO — Platform Libraries

| Function | Library | Class / Function |
|----------|---------|-----------------|
| File operations | `nf_common` | `Files` |
| Folder operations | `nf_common` | `Folders` |
| General utilities | `nf_common` | Check the full catalogue before writing new utility code |

Dependency declaration: add `nf_common` to `requirements.txt` or `pyproject.toml`.

---

## Ontoledgy — Platform Libraries

| Function | Library | Class / Function |
|----------|---------|-----------------|
| Core PDK utilities | `bclearer_pdk` | Check the full catalogue before writing new utility code |
| AI capabilities | `ai` | Check the full catalogue before writing new AI-related code |
| UI components | `ui` | Check the full catalogue before writing new UI code |

Dependency declaration: add `bclearer_pdk`, `ai`, and/or `ui` as required.

---

## Rule

Always check the active variant's platform library catalogue **before** writing a new
utility function. Custom code is only justified when no platform function covers the need.

Both variants share the same BORO coding conventions (naming, layout, structure, error
handling). Only the platform library references differ.
