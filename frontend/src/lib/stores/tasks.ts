import { writable } from 'svelte/store';
import { listTasks, createTask, updateTask, deleteTask } from '$lib/api/tasks';
import { addToast } from './toast';
import type { ITTask, TaskStatus } from '$lib/types';

interface TaskFilters {
	search: string;
	status: TaskStatus | '';
	employeeEmail: string;
	assignee: string;
}

interface TaskStore {
	items: ITTask[];
	loading: boolean;
	error: string | null;
	filters: TaskFilters;
	page: number;
	pageSize: number;
	total: number;
}

const DEFAULT_FILTERS: TaskFilters = {
	search: '',
	status: '',
	employeeEmail: '',
	assignee: ''
};

export const taskStore = writable<TaskStore>({
	items: [],
	loading: false,
	error: null,
	filters: { ...DEFAULT_FILTERS },
	page: 1,
	pageSize: 25,
	total: 0
});

let debounceTimer: ReturnType<typeof setTimeout>;

export async function fetchTasks(employeeId?: string): Promise<void> {
	taskStore.update((s) => ({ ...s, loading: true, error: null }));
	try {
		const items = await listTasks(employeeId);
		taskStore.update((s) => ({ ...s, items, total: items.length, loading: false }));
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to load tasks';
		taskStore.update((s) => ({ ...s, loading: false, error: message, items: [] }));
	}
}

export function setTaskFilter(partial: Partial<TaskFilters>): void {
	taskStore.update((s) => ({
		...s,
		filters: { ...s.filters, ...partial },
		page: 1
	}));
	clearTimeout(debounceTimer);
	debounceTimer = setTimeout(() => fetchTasks(), 300);
}

export async function addTask(payload: Omit<ITTask, 'task_id'>): Promise<boolean> {
	try {
		await createTask(payload);
		addToast('success', 'Task created successfully.');
		await fetchTasks();
		return true;
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to create task');
		return false;
	}
}

export async function editTask(taskId: string, payload: Partial<ITTask>): Promise<boolean> {
	try {
		await updateTask(taskId, payload);
		addToast('success', 'Task updated.');
		await fetchTasks();
		return true;
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to update task');
		return false;
	}
}

export async function removeTask(taskId: string): Promise<boolean> {
	try {
		await deleteTask(taskId);
		addToast('success', 'Task deleted.');
		await fetchTasks();
		return true;
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to delete task');
		return false;
	}
}

export function filterTasks(items: ITTask[], filters: TaskFilters): ITTask[] {
	return items.filter((task) => {
		const matchesSearch =
			!filters.search || task.title.toLowerCase().includes(filters.search.toLowerCase());
		const matchesStatus = !filters.status || task.status === filters.status;
		const matchesEmployee =
			!filters.employeeEmail ||
			(task.employee_email ?? '').toLowerCase().includes(filters.employeeEmail.toLowerCase());
		const matchesAssignee =
			!filters.assignee ||
			(task.assignee ?? '').toLowerCase().includes(filters.assignee.toLowerCase());
		return matchesSearch && matchesStatus && matchesEmployee && matchesAssignee;
	});
}
