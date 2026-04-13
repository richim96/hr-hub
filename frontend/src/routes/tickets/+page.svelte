<script lang="ts">
	import { onMount } from 'svelte';
	import { Plus, Search, SlidersHorizontal } from 'lucide-svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import TicketsTable from '$lib/components/tables/TicketsTable.svelte';
	import NewTicketModal from '$lib/components/modals/NewTicketModal.svelte';
	import TicketDetailModal from '$lib/components/modals/TicketDetailModal.svelte';
	import { ticketStore, fetchTickets, setTicketFilter, filterTickets } from '$lib/stores/tickets';
	import type { APIResponse, ResponseStatus } from '$lib/types';

	onMount(() => {
		fetchTickets();
	});

	let showNewTicket = false;
	let showTicketDetail = false;
	let selectedTicket: APIResponse | null = null;
	let showFilters = false;

	$: store = $ticketStore;
	$: filtered = filterTickets(store.items, store.filters);
	$: displayed = filtered.slice((store.page - 1) * store.pageSize, store.page * store.pageSize);
	$: totalPages = Math.max(1, Math.ceil(filtered.length / store.pageSize));

	const statusOptions: { value: ResponseStatus | ''; label: string }[] = [
		{ value: '', label: 'All statuses' },
		{ value: 'completed', label: 'Completed' },
		{ value: 'pending', label: 'Pending' },
		{ value: 'failed', label: 'Failed' }
	];

	function handleSearchInput(e: Event) {
		setTicketFilter({ search: (e.target as HTMLInputElement).value });
	}

	function handleStatusChange(e: Event) {
		setTicketFilter({ status: (e.target as HTMLSelectElement).value as ResponseStatus | '' });
	}

	function handleSubmitterInput(e: Event) {
		setTicketFilter({ submittedBy: (e.target as HTMLInputElement).value });
	}
</script>

<svelte:head>
	<title>Tickets — HR Hub</title>
</svelte:head>

<!-- Page header -->
<div class="flex items-center justify-between mb-6">
	<div>
		<h2 class="text-xl font-semibold text-gray-900">People Tickets</h2>
		<p class="text-sm text-gray-500 mt-0.5">
			{#if store.loading}Loading…{:else}{filtered.length} tickets{/if}
		</p>
	</div>
	<div class="flex gap-2">
		<Button variant="secondary" size="sm" on:click={() => (showFilters = !showFilters)}>
			<SlidersHorizontal size={15} />
			Filters
		</Button>
		<Button variant="primary" size="sm" on:click={() => (showNewTicket = true)}>
			<Plus size={15} />
			New Ticket
		</Button>
	</div>
</div>

<!-- Search + filter bar -->
<Card padding="sm" class="mb-4">
	<div class="flex flex-col gap-3">
		<div class="relative">
			<Search size={15} class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
			<input
				type="text"
				placeholder="Search by request ID or topic…"
				value={store.filters.search}
				on:input={handleSearchInput}
				class="w-full pl-9 pr-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C05B28]-500"
			/>
		</div>

		{#if showFilters}
			<div class="grid grid-cols-2 gap-3 pt-2 border-t border-gray-100">
				<Select
					id="ticketStatusFilter"
					label="Status"
					value={store.filters.status}
					options={statusOptions}
					on:change={handleStatusChange}
				/>
				<div class="flex flex-col gap-1">
					<label for="submitterFilter" class="text-sm font-medium text-gray-700">Submitted By</label>
					<input
						id="submitterFilter"
						type="text"
						placeholder="employee@company.com"
						value={store.filters.submittedBy}
						on:input={handleSubmitterInput}
						class="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C05B28]-500"
					/>
				</div>
			</div>
		{/if}
	</div>
</Card>

<!-- Table -->
<Card padding="none">
	<TicketsTable
		items={displayed}
		loading={store.loading}
		error={store.error}
		on:select={(e) => { selectedTicket = e.detail; showTicketDetail = true; }}
	/>

	{#if !store.loading && filtered.length > store.pageSize}
		<div class="flex items-center justify-between px-4 py-3 border-t border-gray-100 text-sm text-gray-600">
			<span>
				{(store.page - 1) * store.pageSize + 1}–{Math.min(
					store.page * store.pageSize,
					filtered.length
				)} of {filtered.length}
			</span>
			<div class="flex gap-2">
				<Button
					variant="ghost"
					size="sm"
					disabled={store.page <= 1}
					on:click={() => ticketStore.update((s) => ({ ...s, page: s.page - 1 }))}
				>
					Previous
				</Button>
				<Button
					variant="ghost"
					size="sm"
					disabled={store.page >= totalPages}
					on:click={() => ticketStore.update((s) => ({ ...s, page: s.page + 1 }))}
				>
					Next
				</Button>
			</div>
		</div>
	{/if}
</Card>

<!-- Modals -->
<NewTicketModal
	bind:open={showNewTicket}
	on:close={() => (showNewTicket = false)}
	on:submitted={(e) => {
		showNewTicket = false;
		selectedTicket = e.detail;
		showTicketDetail = true;
	}}
/>

<TicketDetailModal
	bind:open={showTicketDetail}
	ticket={selectedTicket}
	on:close={() => { showTicketDetail = false; selectedTicket = null; }}
/>
