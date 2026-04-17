<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Skeleton from '$lib/components/ui/Skeleton.svelte';
	import type { Ticket, Status } from '$lib/types';

	export let items: Ticket[] = [];
	export let loading = false;
	export let error: string | null = null;
	export let maxHeight = 'calc(100vh - 20rem)';

	const dispatch = createEventDispatcher<{ select: Ticket }>();

	function statusVariant(status: Status) {
		if (status === 'Completed') return 'completed';
		if (status === 'Canceled') return 'failed';
		return 'pending';
	}


</script>

<div class="overflow-auto" style="max-height: {maxHeight}">
	<table class="w-full text-sm">
		<thead class="sticky top-0 z-10 bg-gray-50">
			<tr class="border-b border-gray-200">
				<th class="px-4 py-2 text-left font-medium text-gray-600">Submitted By</th>
				<th class="px-4 py-2 text-left font-medium text-gray-600">Title</th>
				<th class="px-4 py-2 text-left font-medium text-gray-600">Status</th>
				<th class="px-4 py-2 text-left font-medium text-gray-600">Topics</th>
				<th class="px-4 py-2 text-left font-medium text-gray-600">Actions</th>
				<th class="px-4 py-2 text-left font-medium text-gray-600">Ticket ID</th>
			</tr>
		</thead>
		<tbody>
			{#if loading}
				<tr><td colspan="6" class="px-4 py-6"><Skeleton rows={6} cols={5} /></td></tr>
			{:else if error}
				<tr>
					<td colspan="6" class="px-4 py-12 text-center text-gray-500">
						<p class="text-red-500 font-medium">{error}</p>
						<p class="text-sm mt-1 text-gray-400">Ticketing endpoint is not yet available on the backend.</p>
					</td>
				</tr>
			{:else if items.length === 0}
				<tr>
					<td colspan="6" class="px-4 py-12 text-center text-gray-500">
						<p class="font-medium">No tickets yet</p>
						<p class="text-xs mt-1">Submit a ticket to see it here.</p>
					</td>
				</tr>
			{:else}
				{#each items as ticket}
					<tr
						class="border-b border-gray-100 hover:bg-[#fdf4ef]/30 cursor-pointer transition-colors"
						on:click={() => dispatch('select', ticket)}
					>
						<td class="px-4 py-3 text-xs text-gray-600">{ticket.submitted_by ?? '—'}</td>
						<td class="px-4 py-3 font-medium text-gray-900">{ticket.title}</td>
						<td class="px-4 py-2">
							<Badge variant={statusVariant(ticket.status)}>{ticket.status}</Badge>
						</td>
						<td class="px-4 py-2">
							{#if ticket.llm_result?.topics?.length}
								<div class="flex flex-wrap gap-1">
									{#each ticket.llm_result.topics as topic}
										<span class="px-1.5 py-0.5 bg-[#fdf4ef] text-[#9a3d1a] rounded text-xs">{topic}</span>
									{/each}
								</div>
							{:else}
								<span class="text-gray-400 text-xs">—</span>
							{/if}
						</td>
						<td class="px-4 py-3 text-xs text-gray-500">
							{ticket.actions.length} action{ticket.actions.length !== 1 ? 's' : ''}
						</td>
						<td class="px-4 py-3 font-mono text-xs text-gray-400">{ticket.request_id}</td>
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
</div>
