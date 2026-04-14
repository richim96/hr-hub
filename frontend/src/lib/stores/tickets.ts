import { writable } from 'svelte/store';
import { listTickets, createTicket } from '$lib/api/tickets';
import { addToast } from './toast';
import type { APIResponse, ResponseStatus, TicketRequest } from '$lib/types';

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
	pageSize: 50,
	total: 0
});

let debounceTimer: ReturnType<typeof setTimeout>;

export async function fetchTickets(): Promise<void> {
	ticketStore.update((s) => ({ ...s, loading: true, error: null }));
	try {
		const items = await listTickets();
		ticketStore.update((s) => ({ ...s, items, total: items.length, loading: false }));
	} catch (err) {
		const message = err instanceof Error ? err.message : 'Failed to load tickets';
		ticketStore.update((s) => ({ ...s, loading: false, error: message, items: [] }));
	}
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
		await fetchTickets();
		return response;
	} catch (err) {
		addToast('error', err instanceof Error ? err.message : 'Failed to submit ticket');
		return null;
	}
}

export function filterTickets(items: APIResponse[], filters: TicketFilters): APIResponse[] {
	return items.filter((ticket) => {
		const matchesStatus = !filters.status || ticket.status === filters.status;
		const matchesSearch =
			!filters.search ||
			ticket.request_id.toLowerCase().includes(filters.search.toLowerCase()) ||
			(ticket.llm_result?.topics ?? []).some((t) =>
				t.toLowerCase().includes(filters.search.toLowerCase())
			);
		return matchesStatus && matchesSearch;
	});
}
