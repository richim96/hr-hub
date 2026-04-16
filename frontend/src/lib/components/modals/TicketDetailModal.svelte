<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Pencil, Trash2 } from 'lucide-svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import { editTicket } from '$lib/stores/tickets';
	import type { APIResponse } from '$lib/types';

	export let open = false;
	export let ticket: APIResponse | null = null;

	const dispatch = createEventDispatcher<{ close: void; deleted: string }>();

	let editing = false;
	let submitting = false;
	let confirmOpen = false;

	let subject = '';
	let text = '';

	$: if (ticket && open) {
		editing = false;
	}

	function startEdit() {
		if (!ticket) return;
		subject = ticket.subject ?? '';
		text = ticket.text ?? '';
		editing = true;
	}

	function cancelEdit() {
		editing = false;
	}

	async function handleSave() {
		if (!ticket) return;
		submitting = true;
		await editTicket(ticket.request_id, {
			subject: subject || null,
			text: text || null
		});
		submitting = false;
		editing = false;
	}

	async function handleDelete() {
		dispatch('deleted', ticket!.request_id);
		confirmOpen = false;
	}

	function statusVariant(status: string) {
		if (status === 'completed') return 'completed';
		if (status === 'failed') return 'failed';
		return 'pending';
	}

	function handleClose() {
		editing = false;
		dispatch('close');
	}
</script>

<Modal {open} maxWidth="xl" on:close={handleClose}>
	<svelte:fragment slot="title">
		{#if ticket}
			{ticket.subject ?? ticket.request_id}
			{#if !editing}
				<button
					class="p-1 rounded text-gray-400 hover:text-[#C05B28] hover:bg-[#fdf4ef] transition-colors"
					on:click={startEdit}
					aria-label="Edit ticket"
				>
					<Pencil size={14} />
				</button>
				<button
					class="p-1 rounded text-red-400 hover:text-red-600 hover:bg-red-50 transition-colors"
					on:click={() => (confirmOpen = true)}
					aria-label="Delete ticket"
				>
					<Trash2 size={14} />
				</button>
			{/if}
		{/if}
	</svelte:fragment>

	{#if ticket}
		{#if editing}
			<form class="space-y-4">
				<Input id="ticketSubject" label="Subject" bind:value={subject} required />
				<Textarea id="ticketText" label="Description" bind:value={text} rows={6} />
			</form>
		{:else}
			<div class="space-y-4">
				<!-- ID + status -->
				<div class="space-y-2">
					<div>
						<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">Ticket ID</p>
						<p class="text-sm font-mono text-gray-600">{ticket.request_id}</p>
					</div>
					<div>
						<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Status</p>
						<Badge variant={statusVariant(ticket.status)}>{ticket.status}</Badge>
					</div>
				</div>

				<!-- Subject -->
				<div class="pt-2 border-t border-gray-100">
					<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">Subject</p>
					<p class="text-base font-semibold text-gray-900">{ticket.subject ?? '—'}</p>
				</div>

				<!-- Description -->
				{#if ticket.text}
					<div>
						<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Description</p>
						<p class="text-sm text-gray-700 whitespace-pre-wrap">{ticket.text}</p>
					</div>
				{/if}

				<!-- Meta -->
				{#if ticket.submitted_by}
					<div class="pt-2 border-t border-gray-100">
						<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">Submitted By</p>
						<p class="text-sm text-gray-700">{ticket.submitted_by}</p>
					</div>
				{/if}

				<!-- LLM result -->
				{#if ticket.llm_result}
					<div class="space-y-3 pt-2 border-t border-gray-100">
						<p class="text-sm font-semibold text-gray-700">AI Analysis</p>
						<div class="flex flex-wrap gap-1">
							{#each ticket.llm_result.topics as topic}
								<span class="px-2 py-0.5 bg-[#fdf4ef] text-[#9a3d1a] rounded-full text-xs">{topic}</span>
							{/each}
						</div>
						<div class="flex items-center gap-2 text-sm text-gray-600">
							<span>Confidence:</span>
							<div class="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden max-w-32">
								<div class="h-full bg-[#C05B28] rounded-full" style="width: {ticket.llm_result.confidence * 100}%" />
							</div>
							<span class="font-medium">{Math.round(ticket.llm_result.confidence * 100)}%</span>
						</div>
						{#if ticket.llm_result.draft_response}
							<div>
								<p class="text-sm font-medium text-gray-700 mb-1">Draft Response</p>
								<div class="bg-gray-50 rounded-lg p-4 text-sm text-gray-700 whitespace-pre-wrap border border-gray-200">
									{ticket.llm_result.draft_response}
								</div>
							</div>
						{/if}
					</div>
				{/if}

				<!-- Actions -->
				<div class="pt-2 border-t border-gray-100">
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
	{/if}

	<svelte:fragment slot="footer">
		{#if editing}
			<Button variant="secondary" on:click={cancelEdit} disabled={submitting}>Cancel</Button>
			<Button variant="primary" on:click={handleSave} loading={submitting}>Save Changes</Button>
		{:else}
			<Button variant="secondary" on:click={handleClose}>Close</Button>
		{/if}
	</svelte:fragment>
</Modal>

<ConfirmModal
	open={confirmOpen}
	title="Delete Ticket"
	message="Delete ticket '{ticket?.subject ?? ticket?.request_id ?? ''}'? This cannot be undone."
	on:confirm={handleDelete}
	on:cancel={() => (confirmOpen = false)}
/>
