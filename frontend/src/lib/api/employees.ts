/**
 * Employee API service.
 *
 *   GET    /hr-hub/api/v0.1/employee            ✅ current employees only (attrition=False)
 *   GET    /hr-hub/api/v0.1/employee/:id        ✅ single current employee
 *   POST   /hr-hub/api/v0.1/employee/new-hire   ✅
 *   PATCH  /hr-hub/api/v0.1/employee/:id        ✅ partial update (any field)
 *   DELETE /hr-hub/api/v0.1/employee/:id        ✅ hard delete
 */

import { apiFetch } from './client';
import type { APIResponse, FullEmployee, NewHireRequest, UpdateEmployeeRequest } from '$lib/types';

const PREFIX = '/hr-hub/api/v0.1/employee';

/** Create a new employee via the onboarding workflow. */
export async function createEmployee(payload: NewHireRequest): Promise<APIResponse> {
	return apiFetch<APIResponse>(`${PREFIX}/new-hire`, {
		method: 'POST',
		json: payload
	});
}

/** Partially update an employee's identity, equipment, or employment info. */
export async function updateEmployee(employeeId: string, payload: UpdateEmployeeRequest): Promise<APIResponse> {
	return apiFetch<APIResponse>(`${PREFIX}/${employeeId}`, {
		method: 'PATCH',
		json: payload
	});
}

/** Hard-delete an employee and all their related records. */
export async function deleteEmployee(employeeId: string): Promise<APIResponse> {
	return apiFetch<APIResponse>(`${PREFIX}/${employeeId}`, {
		method: 'DELETE'
	});
}

/** List all current employees (attrition=False). */
export async function listEmployees(): Promise<FullEmployee[]> {
	return apiFetch<FullEmployee[]>(`${PREFIX}`);
}

/** Get a single employee by ID. */
export async function getEmployee(employeeId: string): Promise<FullEmployee> {
	return apiFetch<FullEmployee>(`${PREFIX}/${employeeId}`);
}
