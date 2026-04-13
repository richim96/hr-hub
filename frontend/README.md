# HR Hub — Frontend

SvelteKit single-page application for the HR Hub platform. Provides three operational dashboards (Employees, IT Tasks, Tickets) and a floating AI chat widget, all backed by the HR Hub FastAPI backend.

## Stack

| Layer | Technology |
|-------|-----------|
| Framework | [SvelteKit](https://kit.svelte.dev/) 2 + Svelte 4 |
| Language | TypeScript (strict) |
| Styling | [Tailwind CSS](https://tailwindcss.com/) 3 |
| Icons | [lucide-svelte](https://lucide.dev/) |
| HTTP | Native `fetch` via typed API client |
| State | Svelte writable stores |
| Package manager | yarn |

## Quick start

```bash
# from the frontend/ directory
yarn install
yarn dev          # http://localhost:5173
```

Requires the FastAPI backend to be running at `http://localhost:8000` (or the URL set in `.env`).

## Environment variables

Copy `.env.example` to `.env`:

```env
PUBLIC_API_BASE_URL=http://localhost:8000
```

## Project structure

```
src/
├── routes/
│   ├── +layout.svelte          # Shell: sidebar, header, toast, chat widget
│   ├── +page.svelte            # Redirects → /employees
│   ├── employees/+page.svelte  # Employees dashboard
│   ├── tasks/+page.svelte      # IT Tasks dashboard
│   └── tickets/+page.svelte    # People Tickets dashboard
└── lib/
    ├── api/
    │   ├── client.ts           # apiFetch base wrapper + ApiError
    │   ├── employees.ts        # Employee CRUD calls
    │   ├── tasks.ts            # IT Task CRUD calls
    │   ├── tickets.ts          # Ticket calls
    │   └── chat.ts             # LLM agent call
    ├── stores/
    │   ├── employees.ts        # Employee state + actions
    │   ├── tasks.ts            # Task state + actions
    │   ├── tickets.ts          # Ticket state + actions
    │   └── toast.ts            # Toast queue
    ├── types/
    │   └── index.ts            # TypeScript interfaces (mirrors backend DTOs)
    └── components/
        ├── ui/                 # Primitive components (Button, Badge, Modal, Input, …)
        ├── tables/             # EmployeesTable, TasksTable, TicketsTable
        ├── modals/             # NewHire, EmployeeDetail, NewTask, TaskDetail, NewTicket, TicketDetail
        ├── Sidebar.svelte
        ├── Header.svelte
        ├── ChatWidget.svelte   # Floating AI assistant
        └── Toast.svelte
```

## Commands

```bash
yarn dev            # dev server with HMR
yarn build          # production build
yarn preview        # preview production build locally
yarn check          # Svelte + TypeScript type check
yarn lint           # ESLint
yarn test           # Vitest unit tests
```

## Backend API contract

All requests go to `PUBLIC_API_BASE_URL/hr-hub/api/v0.1`.

| Status | Endpoint | Description |
|--------|----------|-------------|
| Ready | `POST /employee/new-hire` | Create employee + IT tasks |
| Stub | `PATCH /employee/change` | Update employee (returns null) |
| TODO | `GET /employee` | List employees |
| TODO | `GET /tasks` | List IT tasks |
| TODO | `POST /ticketing` | Submit people ticket |
| TODO | `POST /agent/query` | Chat / LLM query |

Dashboards that hit unimplemented endpoints display an inline empty state rather than crashing. The New Hire form (implemented) is fully functional.

### Payload notes

- `request_type` is sent as `"type"` in JSON (backend `serialization_alias="type"`).
- `employee_id` in `NewHireRequest.employee` is generated on the frontend as `emp_<uuid-prefix>`.
- `request_id` is generated as `req_<uuid>`.

## Features

### Employees dashboard (`/employees`)
- Sortable table: ID, name, department, manager, laptop, attrition risk %
- Search by name/email, filter by department and attrition risk range
- **New Hire** modal — full form (employee details, equipment, department/salary), POSTs to `/employee/new-hire`, shows `APIResponse` actions on success
- **Employee Detail** modal — view all fields + performance metrics; Edit mode sends `PATCH /employee/change`
- Pagination (50 rows/page)

### IT Tasks dashboard (`/tasks`)
- Sortable table: task ID, title, employee, assignee, status badge, due date
- Filter by status, employee ID, assignee; search by title
- **New Task** modal — create standalone task
- **Edit Task** modal — update title, description, assignee, due date, status; delete task
- Pagination

### Tickets dashboard (`/tickets`)
- Sortable table: request ID, status badge, LLM-extracted topics (pill list), confidence, action count
- Filter by status; search by ID or topic
- **New Ticket** modal — submit form → displays inline LLM result (topics, confidence bar, draft response, actions taken)
- **Ticket Detail** modal — full view of `APIResponse` incl. `LLMResult` and all actions

### Chat Widget
- Floating button (bottom-right, all pages)
- Passes current route as context with every message
- Graceful error when backend chat endpoint is not yet available
- Typing indicator (bouncing dots)

## Claude Code guidance

See [`.claude/CLAUDE.md`](.claude/CLAUDE.md) for module rules and backend contract notes used by Claude Code in this directory.
