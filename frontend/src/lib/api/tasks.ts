/**
 * IT Tasks API service.
 *
 * Implemented backend endpoints:
 *   GET    /hr-hub/api/v0.1/it-tasks               ✅ optional ?employee_id filter
 *   GET    /hr-hub/api/v0.1/it-tasks/:id           ✅
 *   POST   /hr-hub/api/v0.1/it-tasks               ✅
 *   PATCH  /hr-hub/api/v0.1/it-tasks/:id           ✅
 *   DELETE /hr-hub/api/v0.1/it-tasks/:id           ✅
 */

import { apiFetch } from './client';
import type { ITTask } from '$lib/types';

const PREFIX = '/hr-hub/api/v0.1/it-tasks';

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
