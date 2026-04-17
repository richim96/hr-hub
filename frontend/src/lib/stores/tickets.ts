import { writable } from 'svelte/store';
import { listTickets, createTicket, updateTicket, deleteTicket, classifyTicket } from '$lib/api/tickets';
import { addToast } from './toast';
import { isWarm, readCache, writeCache, appendToCache, patchInCache, removeFromCache } from './cache';
import type { Ticket, Status, TicketRequest, UpdateTicketRequest } from '$lib/types';

interface TicketFilters {
	search: string;
	status: Status | '';
	submittedBy: string;
}

interface TicketStore {
	items: Ticket[];
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
		const cached = readCache<Ticket>('tickets');
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

export async function submitTicket(payload: TicketRequest): Promise<Ticket | null> {
	try {
		const ticket = await createTicket(payload);
		addToast('success', 'Ticket submitted successfully.');

		appendToCache('tickets', ticket);
		ticketStore.update((s) => ({
			...s,
			items: [ticket, ...s.items],
			total: s.total + 1
		}));
		return ticket;
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to submit ticket');
		return null;
	}
}

export async function editTicket(requestId: string, payload: UpdateTicketRequest): Promise<void> {
	try {
		const ticket = await updateTicket(requestId, payload);
		addToast('success', 'Ticket updated.');

		patchInCache<Ticket>('tickets', 'request_id', requestId, {
			title: ticket.title,
			text: ticket.text
		});
		ticketStore.update((s) => ({
			...s,
			items: s.items.map((t) =>
				t.request_id === requestId
					? { ...t, title: ticket.title, text: ticket.text }
					: t
			)
		}));
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to update ticket');
	}
}

export async function removeTicket(requestId: string): Promise<void> {
	try {
		await deleteTicket(requestId);
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

export async function runClassification(requestId: string): Promise<Ticket | null> {
	try {
		const ticket = await classifyTicket(requestId);
		addToast('success', 'Ticket classified.');

		patchInCache<Ticket>('tickets', 'request_id', requestId, { llm_result: ticket.llm_result });
		ticketStore.update((s) => ({
			...s,
			items: s.items.map((t) => (t.request_id === requestId ? { ...t, llm_result: ticket.llm_result } : t))
		}));
		return ticket;
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Classification failed');
		return null;
	}
}

export function filterTickets(items: Ticket[], filters: TicketFilters): Ticket[] {
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
