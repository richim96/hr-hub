/**
 * IT Tasks API service.
 *
 * NOTE: No task endpoints are implemented on the backend yet.
 * These functions are defined with the correct signatures and will work
 * once the backend adds the endpoints.
 */

import { apiFetch } from './client';
import type { ITTask } from '$lib/types';

const PREFIX = '/hr-hub/api/v0.1/tasks';

export async function listTasks(employeeId?: string): Promise<ITTask[]> {
	const query = employeeId ? `?employee_id=${encodeURIComponent(employeeId)}` : '';
	return apiFetch<ITTask[]>(`${PREFIX}${query}`);
}

export async function getTask(taskId: string): Promise<ITTask> {
	return apiFetch<ITTask>(`${PREFIX}/${taskId}`);
}

export async function createTask(payload: Omit<ITTask, 'task_id'>): Promise<ITTask> {
	return apiFetch<ITTask>(PREFIX, {
		method: 'POST',
		json: payload
	});
}

export async function updateTask(taskId: string, payload: Partial<ITTask>): Promise<ITTask> {
	return apiFetch<ITTask>(`${PREFIX}/${taskId}`, {
		method: 'PATCH',
		json: payload
	});
}

export async function deleteTask(taskId: string): Promise<void> {
	return apiFetch<void>(`${PREFIX}/${taskId}`, { method: 'DELETE' });
}
