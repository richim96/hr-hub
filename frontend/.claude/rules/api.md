---
description: Rules for working in src/lib/api/
---

# API Module Rules

API service files make HTTP calls to the FastAPI backend. No business logic or UI state belongs here.

## File layout

| File | Domain |
|------|--------|
| `client.ts` | Base fetch wrapper — base URL, headers, error parsing |
| `employees.ts` | Employee endpoints (new hire, change, list) |
| `tasks.ts` | IT task endpoints (list, create, update, delete) |
| `tickets.ts` | Ticketing endpoints (list, create, update) |
| `chat.ts` | Chat/LLM agent endpoint |

## Conventions

- Every function returns `Promise<T>` where `T` is a type from `lib/types/`.
- All requests go through the `apiFetch` helper in `client.ts` — never call `fetch` directly in domain files.
- On non-2xx responses, `apiFetch` throws an `ApiError` with `status` and `message`. Callers (stores) catch it.
- Request bodies are typed as the matching `*Request` interface from `lib/types/`.
- The `request_type` field must be sent as `"type"` in JSON (matches the backend `serialization_alias`).
- Generate `request_id` values as `req_<crypto.randomUUID()>` in the calling store, not inside the API file.
- Do not import Svelte stores from API files — keep API layer free of UI state.

## Unimplemented endpoints

Functions for endpoints not yet on the backend must still be defined with the correct signature. They should call `apiFetch` normally; the store layer handles the resulting error and shows an appropriate empty state.
