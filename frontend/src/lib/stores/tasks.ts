import { writable } from 'svelte/store';
import { listTasks, createTask, updateTask, deleteTask } from '$lib/api/tasks';
import { addToast } from './toast';
import { isWarm, readCache, writeCache, invalidateCache } from './cache';
import type { ITTask, Status } from '$lib/types';

interface TaskFilters {
	search: string;
	status: Status | '';
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
	pageSize: 100,
	total: 0
});

let debounceTimer: ReturnType<typeof setTimeout>;
let _fetchPromise: Promise<void> | null = null;

export async function fetchTasks(employeeId?: string): Promise<void> {
	// Warm: serve from localStorage (filter in-memory if employeeId given).
	if (isWarm('tasks')) {
		const cached = readCache<ITTask>('tasks');
		if (cached !== null) {
			const items = employeeId ? cached.filter((t) => t.employee_id === employeeId) : cached;
			taskStore.update((s) => ({ ...s, items, total: items.length, loading: false, error: null }));
			return;
		}
		// Cache key missing despite warm flag — fall through to re-fetch.
	}

	// If a cold-start fetch is already in-flight, wait for it instead of starting a second one.
	// Note: a concurrent caller with a different employeeId will get all tasks from cache once settled.
	if (_fetchPromise) return _fetchPromise;

	// Cold start: fetch the full unfiltered list from backend, populate cache.
	taskStore.update((s) => ({ ...s, loading: true, error: null }));
	_fetchPromise = (async () => {
		try {
			const all = await listTasks();
			writeCache('tasks', all);
			const items = employeeId ? all.filter((t) => t.employee_id === employeeId) : all;
			taskStore.update((s) => ({ ...s, items, total: items.length, loading: false }));
		} catch (err) {
			const message = err instanceof Error ? err.message : 'Failed to load tasks';
			taskStore.update((s) => ({ ...s, loading: false, error: message, items: [] }));
		} finally {
			_fetchPromise = null;
		}
	})();
	return _fetchPromise;
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

		invalidateCache('tasks');
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

		invalidateCache('tasks');
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

		invalidateCache('tasks');
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
