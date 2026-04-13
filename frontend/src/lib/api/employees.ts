/**
 * Employee API service.
 *
 * Implemented backend endpoints:
 *   POST /hr-hub/api/v0.1/employee/new-hire   ✅
 *   PATCH /hr-hub/api/v0.1/employee/change    ⚠️  stub (returns null)
 *
 * Not yet implemented (handle 404/error gracefully in stores):
 *   GET  /hr-hub/api/v0.1/employee            ❌
 *   GET  /hr-hub/api/v0.1/employee/:id        ❌
 */

import { apiFetch } from './client';
import type { APIResponse, EmployeeChangeRequest, FullEmployee, NewHireRequest } from '$lib/types';

const PREFIX = '/hr-hub/api/v0.1/employee';

/** Create a new employee via the onboarding workflow. */
export async function createEmployee(payload: NewHireRequest): Promise<APIResponse> {
	return apiFetch<APIResponse>(`${PREFIX}/new-hire`, {
		method: 'POST',
		json: payload
	});
}

/**
 * Update employee fields.
 * NOTE: Backend stub — currently returns null. The store handles this gracefully.
 */
export async function updateEmployee(payload: EmployeeChangeRequest): Promise<APIResponse> {
	return apiFetch<APIResponse>(`${PREFIX}/change`, {
		method: 'PATCH',
		json: payload
	});
}

/**
 * List all employees.
 * NOTE: Endpoint not yet implemented on the backend. Returns empty array until available.
 */
export async function listEmployees(): Promise<FullEmployee[]> {
	return apiFetch<FullEmployee[]>(`${PREFIX}`);
}

/**
 * Get a single employee by ID.
 * NOTE: Endpoint not yet implemented on the backend.
 */
export async function getEmployee(employeeId: string): Promise<FullEmployee> {
	return apiFetch<FullEmployee>(`${PREFIX}/${employeeId}`);
}
