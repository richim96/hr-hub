import { writable } from 'svelte/store';
import { createEmployee, deleteEmployee, listEmployees, updateEmployee } from '$lib/api/employees';
import { scoreAll } from '$lib/api/prediction';
import { addToast } from './toast';
import { isWarm, readCache, writeCache, invalidateCache } from './cache';
import type { Department, FullEmployee, NewHireRequest, UpdateEmployeeRequest } from '$lib/types';

interface EmployeeFilters {
	search: string;
	department: Department | '';
	attritionRiskMin: number;
	attritionRiskMax: number;
}

interface EmployeeStore {
	items: FullEmployee[];
	loading: boolean;
	error: string | null;
	filters: EmployeeFilters;
	page: number;
	pageSize: number;
	total: number;
}

const DEFAULT_FILTERS: EmployeeFilters = {
	search: '',
	department: '',
	attritionRiskMin: 0,
	attritionRiskMax: 1
};

export const employeeStore = writable<EmployeeStore>({
	items: [],
	loading: false,
	error: null,
	filters: { ...DEFAULT_FILTERS },
	page: 1,
	pageSize: 100,
	total: 0
});

let debounceTimer: ReturnType<typeof setTimeout>;
// Deduplicates concurrent cold-start calls (e.g. layout + page onMount fire together).
let _fetchPromise: Promise<void> | null = null;

export async function fetchEmployees(): Promise<void> {
	// Warm: serve from localStorage, skip network.
	if (isWarm('employees')) {
		const cached = readCache<FullEmployee>('employees');
		if (cached !== null) {
			employeeStore.update((s) => ({ ...s, items: cached, total: cached.length, loading: false, error: null }));
			return;
		}
		// Cache key missing despite warm flag (e.g. localStorage cleared) — fall through to re-fetch.
	}

	// If a cold-start fetch is already in-flight, wait for it instead of starting a second one.
	if (_fetchPromise) return _fetchPromise;

	employeeStore.update((s) => ({ ...s, loading: true, error: null }));
	_fetchPromise = (async () => {
		try {
			const items = await listEmployees();
			writeCache('employees', items); // also marks domain warm via _mem
			employeeStore.update((s) => ({ ...s, items, total: items.length, loading: false }));
		} catch (err) {
			const message = err instanceof Error ? err.message : 'Failed to load employees';
			employeeStore.update((s) => ({ ...s, loading: false, error: message, items: [] }));
		} finally {
			_fetchPromise = null;
		}
	})();
	return _fetchPromise;
}

export function setEmployeeFilter(partial: Partial<EmployeeFilters>): void {
	employeeStore.update((s) => ({
		...s,
		filters: { ...s.filters, ...partial },
		page: 1
	}));
	clearTimeout(debounceTimer);
	debounceTimer = setTimeout(fetchEmployees, 300);
}

export async function hireEmployee(payload: NewHireRequest): Promise<boolean> {
	try {
		const response = await createEmployee(payload);
		if (response.status === 'Canceled') {
			addToast('error', `New hire failed: ${response.actions.find((a) => !a.success)?.details ?? 'unknown error'}`);
			return false;
		}
		addToast('success', `Employee ${payload.employee.first_name} ${payload.employee.last_name} onboarded successfully.`);

		invalidateCache('employees');
		await fetchEmployees();
		return true;
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to create employee';
		addToast('error', message);
		return false;
	}
}

export async function changeEmployee(employeeId: string, payload: UpdateEmployeeRequest): Promise<boolean> {
	try {
		await updateEmployee(employeeId, payload);
		addToast('success', 'Employee updated successfully.');

		invalidateCache('employees');
		await fetchEmployees();
		return true;
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to update employee';
		addToast('error', message);
		return false;
	}
}

export async function removeEmployee(employeeId: string): Promise<boolean> {
	try {
		await deleteEmployee(employeeId);
		addToast('success', 'Employee deleted successfully.');

		invalidateCache('employees');
		await fetchEmployees();
		return true;
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to delete employee';
		addToast('error', message);
		return false;
	}
}

/** Batch-score all employees and refresh the list from the backend. */
export async function refreshRiskScores(): Promise<boolean> {
	try {
		const requestId = `req_${crypto.randomUUID()}`;
		const response = await scoreAll({ request_id: requestId, request_type: 'prediction' });
		if (response.status === 'Canceled') {
			addToast('error', `Batch scoring failed: ${response.actions.find((a) => !a.success)?.details ?? 'model unavailable'}`);
			return false;
		}
		const detail = response.actions.find((a) => a.success)?.details ?? 'Risk scores refreshed.';
		addToast('success', detail);

		// Scores changed server-side: re-fetch and overwrite the cache.
		const items = await listEmployees();
		writeCache('employees', items);
		employeeStore.update((s) => ({ ...s, items, total: items.length }));
		return true;
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to refresh risk scores';
		addToast('error', message);
		return false;
	}
}

/** Client-side filtering applied on top of fetched items. */
export function filterEmployees(items: FullEmployee[], filters: EmployeeFilters): FullEmployee[] {
	return items.filter((emp) => {
		const searchLower = filters.search.toLowerCase();
		const matchesSearch =
			!filters.search ||
			`${emp.first_name} ${emp.last_name}`.toLowerCase().includes(searchLower) ||
			emp.email.toLowerCase().includes(searchLower);

		const matchesDept = !filters.department || emp.department === filters.department;

		const risk = emp.attrition_risk ?? 0;
		const matchesRisk = risk >= filters.attritionRiskMin && risk <= filters.attritionRiskMax;

		return matchesSearch && matchesDept && matchesRisk;
	});
}
