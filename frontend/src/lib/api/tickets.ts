/**
 * Ticketing API service.
 *
 * NOTE: Ticketing endpoints are marked TODO on the backend.
 * These functions are defined with the correct signatures and will work
 * once the backend adds the endpoints under /hr-hub/api/v0.1/ticketing.
 */

import { apiFetch } from './client';
import type { APIResponse, TicketRequest } from '$lib/types';

const PREFIX = '/hr-hub/api/v0.1/ticketing';

/** Submit a new people-team ticket. Expects APIResponse in return. */
export async function createTicket(payload: TicketRequest): Promise<APIResponse> {
	return apiFetch<APIResponse>(PREFIX, {
		method: 'POST',
		json: payload
	});
}

/** List all tickets. Not yet implemented on the backend. */
export async function listTickets(): Promise<APIResponse[]> {
	return apiFetch<APIResponse[]>(PREFIX);
}

/** Get a single ticket by request_id. Not yet implemented on the backend. */
export async function getTicket(requestId: string): Promise<APIResponse> {
	return apiFetch<APIResponse>(`${PREFIX}/${requestId}`);
}
