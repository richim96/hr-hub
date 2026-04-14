---
description: Rules for working in src/lib/components/
---

# Components Module Rules

Components are organized into two layers: primitive UI components in `ui/` and feature-specific components in domain folders.

## Directory structure

```
src/lib/components/
├── ui/                    # Primitive / design-system components (shadcn-style)
│   ├── Button.svelte
│   ├── Badge.svelte
│   ├── Card.svelte
│   ├── Input.svelte
│   ├── Select.svelte
│   ├── Textarea.svelte
│   ├── Modal.svelte
│   └── Skeleton.svelte
├── tables/                # Domain table components
│   ├── EmployeesTable.svelte
│   ├── TasksTable.svelte
│   └── TicketsTable.svelte
├── modals/                # CRUD modals
│   ├── NewHireModal.svelte
│   ├── EmployeeDetailModal.svelte
│   ├── NewTaskModal.svelte
│   ├── TaskDetailModal.svelte
│   ├── NewTicketModal.svelte
│   └── TicketDetailModal.svelte
├── Sidebar.svelte
├── Header.svelte
├── ChatWidget.svelte
└── Toast.svelte
```

## Conventions

- All `ui/` components accept standard HTML attributes via Svelte's `$$restProps` pattern and forward them to the root element.
- Use Tailwind utility classes only — no inline `style` attributes.
- Status badges use consistent color tokens: `pending` → amber, `completed` → green, `failed`/`Canceled` → red.
- Modal components receive an `open` boolean prop and emit a `close` event. They do not own their open state.
- Table components receive `items`, `loading`, and `error` props. They are display-only — actions emit events up to the page.
- Form submissions call store actions, not API functions directly.
- Skeleton loading states match the shape of the real content (same number of rows/columns).

## Responsive breakpoints

- Mobile (`< 768px`): Sidebar hidden, shown via hamburger toggle in Header.
- Tablet (`768px – 1279px`): Sidebar collapsed to icon-only.
- Desktop (`≥ 1280px`): Full sidebar visible.
