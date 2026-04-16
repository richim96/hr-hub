import { writable } from 'svelte/store';
import { listTickets, createTicket, updateTicket, deleteTicket } from '$lib/api/tickets';
import { addToast } from './toast';
import { isWarm, readCache, writeCache, appendToCache, patchInCache, removeFromCache } from './cache';
import type { APIResponse, ResponseStatus, TicketRequest, UpdateTicketRequest } from '$lib/types';

interface TicketFilters {
	search: string;
	status: ResponseStatus | '';
	submittedBy: string;
}

interface TicketStore {
	items: APIResponse[];
	loading: boolean;
	error: string | null;
	filters: TicketFilters;
	page: number;
	pageSize: number;
	total: number;
}

const DEFAULT_FILTERS: TicketFilters = {
	search: '',
	status: '',
	submittedBy: ''
};

export const ticketStore = writable<TicketStore>({
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

export async function fetchTickets(): Promise<void> {
	// Warm: serve from localStorage, skip network.
	if (isWarm('tickets')) {
		const cached = readCache<APIResponse>('tickets');
		if (cached !== null) {
			ticketStore.update((s) => ({ ...s, items: cached, total: cached.length, loading: false, error: null }));
			return;
		}
		// Cache key missing despite warm flag — fall through to re-fetch.
	}

	// If a cold-start fetch is already in-flight, wait for it instead of starting a second one.
	if (_fetchPromise) return _fetchPromise;

	// Cold start: fetch from backend, populate cache.
	ticketStore.update((s) => ({ ...s, loading: true, error: null }));
	_fetchPromise = (async () => {
		try {
			const items = await listTickets();
			writeCache('tickets', items);
			ticketStore.update((s) => ({ ...s, items, total: items.length, loading: false }));
		} catch (err) {
			const message = err instanceof Error ? err.message : 'Failed to load tickets';
			ticketStore.update((s) => ({ ...s, loading: false, error: message, items: [] }));
		} finally {
			_fetchPromise = null;
		}
	})();
	return _fetchPromise;
}

export function setTicketFilter(partial: Partial<TicketFilters>): void {
	ticketStore.update((s) => ({
		...s,
		filters: { ...s.filters, ...partial },
		page: 1
	}));
	clearTimeout(debounceTimer);
	debounceTimer = setTimeout(fetchTickets, 300);
}

export async function submitTicket(payload: TicketRequest): Promise<APIResponse | null> {
	try {
		const response = await createTicket(payload);
		if (response.status === 'failed') {
			addToast('error', 'Ticket submission failed.');
			return null;
		}
		addToast('success', 'Ticket submitted successfully.');

		appendToCache('tickets', response);
		ticketStore.update((s) => ({
			...s,
			items: [response, ...s.items],
			total: s.total + 1
		}));
		return response;
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to submit ticket');
		return null;
	}
}

export async function editTicket(requestId: string, payload: UpdateTicketRequest): Promise<void> {
	try {
		const response = await updateTicket(requestId, payload);
		if (response.status === 'failed') {
			addToast('error', 'Failed to update ticket.');
			return;
		}
		addToast('success', 'Ticket updated.');

		patchInCache<APIResponse>('tickets', 'request_id', requestId, {
			subject: response.subject,
			text: response.text
		});
		ticketStore.update((s) => ({
			...s,
			items: s.items.map((t) =>
				t.request_id === requestId
					? { ...t, subject: response.subject, text: response.text }
					: t
			)
		}));
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to update ticket');
	}
}

export async function removeTicket(requestId: string): Promise<void> {
	try {
		const response = await deleteTicket(requestId);
		if (response.status === 'failed') {
			addToast('error', 'Failed to delete ticket.');
			return;
		}
		addToast('success', 'Ticket deleted.');

		removeFromCache('tickets', 'request_id', requestId);
		ticketStore.update((s) => ({
			...s,
			items: s.items.filter((t) => t.request_id !== requestId),
			total: s.total - 1
		}));
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to delete ticket');
	}
}

export function filterTickets(items: APIResponse[], filters: TicketFilters): APIResponse[] {
	return items.filter((ticket) => {
		const matchesStatus = !filters.status || ticket.status === filters.status;
		const matchesSearch =
			!filters.search ||
			(ticket.llm_result?.topics ?? []).some((t) =>
				t.toLowerCase().includes(filters.search.toLowerCase())
			);
		return matchesStatus && matchesSearch;
	});
}
