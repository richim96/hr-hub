<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import type { APIResponse } from '$lib/types';

	export let open = false;
	export let ticket: APIResponse | null = null;

	const dispatch = createEventDispatcher<{ close: void }>();

	function statusVariant(status: string) {
		if (status === 'completed') return 'completed';
		if (status === 'failed') return 'failed';
		return 'pending';
	}
</script>

<Modal {open} title="Ticket Details" maxWidth="xl" on:close={() => dispatch('close')}>
	{#if ticket}
		<div class="space-y-5">
			<!-- Header row -->
			<div class="flex items-center gap-3 flex-wrap">
				<Badge variant={statusVariant(ticket.status)}>{ticket.status}</Badge>
				<span class="text-sm font-mono text-gray-500">{ticket.request_id}</span>
				<span class="text-sm text-gray-400">{ticket.request_type}</span>
			</div>

			<!-- LLM result -->
			{#if ticket.llm_result}
				<div class="space-y-4">
					<div>
						<p class="text-sm font-semibold text-gray-700 mb-2">AI Analysis</p>
						<div class="flex flex-wrap gap-1 mb-3">
							{#each ticket.llm_result.topics as topic}
								<span class="px-2 py-0.5 bg-[#fdf4ef] text-[#9a3d1a] rounded-full text-xs">{topic}</span>
							{/each}
						</div>
						<div class="flex items-center gap-2 text-sm text-gray-600">
							<span>Confidence:</span>
							<div class="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden max-w-32">
								<div
									class="h-full bg-[#fdf4ef]0 rounded-full"
									style="width: {ticket.llm_result.confidence * 100}%"
								/>
							</div>
							<span class="font-medium">{Math.round(ticket.llm_result.confidence * 100)}%</span>
						</div>
					</div>

					{#if Object.keys(ticket.llm_result.extracted_info).length > 0}
						<div>
							<p class="text-sm font-medium text-gray-700 mb-2">Extracted Information</p>
							<div class="bg-gray-50 rounded-lg p-3 border border-gray-200 text-xs font-mono text-gray-700">
								{JSON.stringify(ticket.llm_result.extracted_info, null, 2)}
							</div>
						</div>
					{/if}

					<div>
						<p class="text-sm font-medium text-gray-700 mb-2">Draft Response</p>
						<div class="bg-gray-50 rounded-lg p-4 text-sm text-gray-700 whitespace-pre-wrap border border-gray-200">
							{ticket.llm_result.draft_response}
						</div>
					</div>
				</div>
			{/if}

			<!-- Actions taken -->
			<div>
				<p class="text-sm font-semibold text-gray-700 mb-2">Actions</p>
				<div class="space-y-2">
					{#each ticket.actions as action}
						<div class="flex items-start gap-2 p-3 rounded-lg border border-gray-100 bg-gray-50">
							<span class={`text-base ${action.success ? 'text-green-500' : 'text-red-500'}`}>
								{action.success ? '✓' : '✗'}
							</span>
							<div class="flex-1 min-w-0">
								<p class="text-sm font-medium text-gray-800">{action.action}</p>
								<p class="text-xs text-gray-500 mt-0.5">{action.details}</p>
							</div>
						</div>
					{:else}
						<p class="text-sm text-gray-400">No actions recorded.</p>
					{/each}
				</div>
			</div>
		</div>
	{/if}

	<svelte:fragment slot="footer">
		<Button variant="secondary" on:click={() => dispatch('close')}>Close</Button>
	</svelte:fragment>
</Modal>
