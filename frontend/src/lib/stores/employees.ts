import { writable, get } from 'svelte/store';
import { createEmployee, listEmployees, updateEmployee } from '$lib/api/employees';
import { addToast } from './toast';
import type { Department, EmployeeChangeRequest, FullEmployee, NewHireRequest } from '$lib/types';

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
	pageSize: 50,
	total: 0
});

let debounceTimer: ReturnType<typeof setTimeout>;

export async function fetchEmployees(): Promise<void> {
	employeeStore.update((s) => ({ ...s, loading: true, error: null }));
	try {
		const items = await listEmployees();
		employeeStore.update((s) => ({ ...s, items, total: items.length, loading: false }));
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to load employees';
		employeeStore.update((s) => ({ ...s, loading: false, error: message, items: [] }));
	}
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
		if (response.status === 'failed') {
			addToast('error', `New hire failed: ${response.actions.find((a) => !a.success)?.details ?? 'unknown error'}`);
			return false;
		}
		addToast('success', `Employee ${payload.employee.first_name} ${payload.employee.last_name} onboarded successfully.`);
		await fetchEmployees();
		return true;
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to create employee';
		addToast('error', message);
		return false;
	}
}

export async function changeEmployee(payload: EmployeeChangeRequest): Promise<boolean> {
	try {
		await updateEmployee(payload);
		addToast('success', 'Employee updated successfully.');
		await fetchEmployees();
		return true;
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to update employee';
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
