/**
 * Ticketing API service.
 *
 * Implemented backend endpoints:
 *   GET    /hr-hub/api/v0.1/ticketing             ✅ newest first
 *   POST   /hr-hub/api/v0.1/ticketing             ✅
 *   DELETE /hr-hub/api/v0.1/ticketing/{id}        ✅
 */

import { apiFetch } from './client';
import type { Ticket, TicketRequest, UpdateTicketRequest } from '$lib/types';

const PREFIX = '/hr-hub/api/v0.1/ticketing';

/** Submit a new people-team ticket. */
export async function createTicket(payload: TicketRequest): Promise<Ticket> {
	return apiFetch<Ticket>(PREFIX, {
		method: 'POST',
		json: payload
	});
}

/** List all tickets, newest first. */
export async function listTickets(): Promise<Ticket[]> {
	return apiFetch<Ticket[]>(PREFIX);
}

/** Get a single ticket by request_id. */
export async function getTicket(requestId: string): Promise<Ticket> {
	return apiFetch<Ticket>(`${PREFIX}/${requestId}`);
}

/** Partially update a ticket's title and/or text. */
export async function updateTicket(requestId: string, payload: UpdateTicketRequest): Promise<Ticket> {
	return apiFetch<Ticket>(`${PREFIX}/${requestId}`, { method: 'PATCH', json: payload });
}

/** Hard-delete a ticket by request_id. */
export async function deleteTicket(requestId: string): Promise<void> {
	return apiFetch<void>(`${PREFIX}/${requestId}`, { method: 'DELETE' });
}
