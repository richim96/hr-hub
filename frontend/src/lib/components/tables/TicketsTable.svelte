<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Eye, ChevronUp, ChevronDown } from 'lucide-svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Skeleton from '$lib/components/ui/Skeleton.svelte';
	import type { APIResponse, ResponseStatus } from '$lib/types';

	export let items: APIResponse[] = [];
	export let loading = false;
	export let error: string | null = null;

	const dispatch = createEventDispatcher<{ select: APIResponse }>();

	let sortKey: 'request_id' | 'status' = 'request_id';
	let sortDir: 'asc' | 'desc' = 'desc';

	$: sorted = [...items].sort((a, b) => {
		const av = a[sortKey] ?? '';
		const bv = b[sortKey] ?? '';
		const cmp = String(av).localeCompare(String(bv));
		return sortDir === 'asc' ? cmp : -cmp;
	});

	function statusVariant(status: ResponseStatus) {
		if (status === 'completed') return 'completed';
		if (status === 'failed') return 'failed';
		return 'pending';
	}

	function confidencePct(c: number | undefined) {
		if (c == null) return '—';
		return `${Math.round(c * 100)}%`;
	}
</script>

<div class="overflow-x-auto">
	<table class="w-full text-sm">
		<thead>
			<tr class="border-b border-gray-200 bg-gray-50">
				<th class="px-4 py-3 text-left font-medium text-gray-600">Request ID</th>
				<th class="px-4 py-3 text-left font-medium text-gray-600">Status</th>
				<th class="px-4 py-3 text-left font-medium text-gray-600">Topics (LLM)</th>
				<th class="px-4 py-3 text-left font-medium text-gray-600">Confidence</th>
				<th class="px-4 py-3 text-left font-medium text-gray-600">Actions</th>
				<th class="w-10" />
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
			{:else if sorted.length === 0}
				<tr>
					<td colspan="6" class="px-4 py-12 text-center text-gray-500">
						<p class="font-medium">No tickets yet</p>
						<p class="text-xs mt-1">Submit a ticket to see it here.</p>
					</td>
				</tr>
			{:else}
				{#each sorted as ticket}
					<tr
						class="border-b border-gray-100 hover:bg-[#fdf4ef]/30 cursor-pointer transition-colors"
						on:click={() => dispatch('select', ticket)}
					>
						<td class="px-4 py-3 font-mono text-xs text-gray-600">{ticket.request_id}</td>
						<td class="px-4 py-3">
							<Badge variant={statusVariant(ticket.status)}>{ticket.status}</Badge>
						</td>
						<td class="px-4 py-3">
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
						<td class="px-4 py-3 text-gray-700">
							{confidencePct(ticket.llm_result?.confidence)}
						</td>
						<td class="px-4 py-3 text-xs text-gray-500">
							{ticket.actions.length} action{ticket.actions.length !== 1 ? 's' : ''}
						</td>
						<td class="px-4 py-3">
							<button
								class="p-1.5 rounded text-gray-400 hover:text-[#C05B28] hover:bg-[#fdf4ef] transition-colors"
								on:click|stopPropagation={() => dispatch('select', ticket)}
								aria-label="View ticket"
							>
								<Eye size={15} />
							</button>
						</td>
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
</div>
