# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in the `frontend/` directory.

## Commands

This project uses [`yarn`](https://yarnpkg.com/) for dependency management.

```bash
yarn install          # install deps
yarn dev              # dev server on http://localhost:5173 (auto-reload)
yarn build            # production build
yarn preview          # preview production build
yarn check            # svelte-check (TypeScript + Svelte type errors)
yarn lint             # eslint
yarn test             # vitest unit tests
```

## Architecture

HR Hub Frontend is a SvelteKit single-page application that drives three operational dashboards (Employees, Tasks, Tickets) and a floating AI chat widget, all backed by the HR Hub FastAPI backend.

**Request flow:** Svelte component → store action → `lib/api/` service → FastAPI backend (base URL from `$env/static/public`)

All backend routes are prefixed `/hr-hub/api/v0.1`. The API base URL is configured via `PUBLIC_API_BASE_URL` in `.env`.

## Module rules

Detailed rules for each module live in `.claude/rules/`:

| Module | Rules file | Responsibility |
|--------|-----------|----------------|
| `src/lib/api/` | [rules/api.md](rules/api.md) | HTTP calls only — one file per domain, typed request/response |
| `src/lib/stores/` | [rules/stores.md](rules/stores.md) | Svelte writable stores; drive fetch, filter, pagination state |
| `src/lib/types/` | [rules/types.md](rules/types.md) | TypeScript interfaces mirroring backend DTOs — source of truth for payload shapes |
| `src/lib/components/` | [rules/components.md](rules/components.md) | UI components; `ui/` for primitives, domain folders for feature components |

## Environment variables

See `.env.example`:
- `PUBLIC_API_BASE_URL` — FastAPI base URL (default `http://localhost:8000`)

## Backend contract notes

- **Implemented endpoints** (safe to call):
  - `POST /hr-hub/api/v0.1/employee/new-hire` → `NewHireRequest` → `APIResponse`
- **Stubs** (returns `null` or 404 — handle gracefully):
  - `PATCH /hr-hub/api/v0.1/employee/change` → `EmployeeChangeRequest`
- **Not yet implemented** (show empty state or disable action):
  - Ticketing endpoints
  - Employee / Task / Ticket list (GET) endpoints
  - Chat / agent endpoint
- The `request_type` field is serialized as `"type"` in JSON (backend uses `serialization_alias="type"`).
- `employee_id` in `NewHireRequest.employee` must be frontend-generated (e.g., `emp_` + UUID).

## Current scaffolding notes

There is no authentication layer. All API calls go through without tokens. When the backend adds auth, add an `Authorization` header in `lib/api/client.ts`.
