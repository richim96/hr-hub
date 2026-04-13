---
description: Rules for working in src/lib/stores/
---

# Stores Module Rules

Svelte stores hold all client-side state: fetched data, filter values, loading/error flags, and pagination cursors.

## File layout

| File | State |
|------|-------|
| `employees.ts` | Employee list, filters, selected employee, loading/error |
| `tasks.ts` | IT task list, filters, selected task, loading/error |
| `tickets.ts` | Ticket list, filters, selected ticket, loading/error |
| `toast.ts` | Toast notification queue |

## Store shape conventions

Each domain store exports:
- `<domain>Store` — writable store with `{ items, loading, error, filters, page, total }`
- `fetch<Domain>s()` — async function that calls the API and writes into the store
- `create<Domain>(data)` — calls POST, dispatches toast, calls `fetch<Domain>s()` on success
- `update<Domain>(id, data)` — calls PATCH/PUT, dispatches toast, refreshes on success
- `delete<Domain>(id)` — calls DELETE, dispatches toast, refreshes on success

## Error handling

- Wrap every API call in try/catch.
- On error, set `store.error` to the `ApiError.message` and dispatch an error toast.
- Never let an unhandled rejection bubble to the Svelte component.

## Filter state

- Filters are stored inside the domain store object (`store.filters`).
- Filter changes trigger a new fetch; debounce text inputs by 300 ms (use a `setTimeout` reset pattern).
- Pagination resets to page 1 on any filter change.

## Toast store

`toast.ts` exports `toasts` (writable array) and `addToast(type, message)`. Auto-dismiss after 4 s. Max 5 simultaneous toasts (oldest removed first).
