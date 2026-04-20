# HR Hub — Frontend
SvelteKit single-page application for the HR Hub platform. Provides three operational dashboards (Employees, IT Tasks, Tickets) and a floating AI chat widget.
## Stack
| Layer | Technology |
|-------|-----------|
| Framework | [SvelteKit](https://kit.svelte.dev/) 2 + Svelte 4 |
| Language | TypeScript (strict) |
| Styling | [Tailwind CSS](https://tailwindcss.com/) 3 |
| Icons | Custom + [lucide-svelte](https://lucide.dev/) |
| HTTP | Native `fetch` via typed API client |
| Markdown | [marked](https://marked.js.org/) |
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
    │   ├── toast.ts            # Toast queue
    │   ├── cache.ts            # Request cache
    │   └── ui.ts               # UI state (sidebar, modals)
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

| Endpoint | Description |
|----------|-------------|
| `GET /employee` | List employees |
| `POST /employee/new-hire` | Create employee + IT tasks |
| `PATCH /employee/{id}` | Update employee |
| `GET /it-tasks` | List IT tasks |
| `POST /it-tasks` | Create IT task |
| `PATCH /it-tasks/{id}` | Update IT task |
| `DELETE /it-tasks/{id}` | Delete IT task |
| `GET /ticketing` | List tickets |
| `POST /ticketing` | Submit people ticket |
| `POST /agent/chat` | Chat / LLM query |

### Payload notes
- `employee_id` in `NewHireRequest.employee` is generated on the frontend as `emp_<uuid-prefix>`.
- `request_id` is generated as `req_<uuid>`.

## Features
### Employees dashboard (`/employees`)
- Sortable table: ID, name, department, manager, laptop, attrition risk %
- Search by name/email, filter by department and attrition risk range
- **New Hire** modal — full form (employee details, equipment, department/salary), POSTs to `/employee/new-hire`, shows `APIResponse` actions on success
- **Employee Detail** modal — view all fields + performance metrics; Edit mode sends `PATCH /employee/{id}`
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
- Typing indicator (bouncing dots)
