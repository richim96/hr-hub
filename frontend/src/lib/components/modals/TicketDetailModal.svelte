<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Pencil, Trash2, Sparkles } from 'lucide-svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import { editTicket, runClassification } from '$lib/stores/tickets';
	import type { Ticket, Status } from '$lib/types';

	export let open = false;
	export let ticket: Ticket | null = null;

	const dispatch = createEventDispatcher<{ close: void; deleted: string }>();

	let editing = false;
	let submitting = false;
	let classifying = false;
	let confirmOpen = false;

	let title = '';
	let text = '';

	$: if (ticket && open) { editing = false; }

	function startEdit() {
		if (!ticket) return;
		title = ticket.title;
		text = ticket.text;
		editing = true;
	}

	function cancelEdit() { editing = false; }

	async function handleSave() {
		if (!ticket) return;
		submitting = true;
		await editTicket(ticket.request_id, { title: title || null, text: text || null });
		submitting = false;
		editing = false;
	}

	async function handleClassify() {
		if (!ticket) return;
		classifying = true;
		const updated = await runClassification(ticket.request_id);
		if (updated) ticket = { ...ticket, llm_result: updated.llm_result };
		classifying = false;
	}

	async function handleDelete() {
		dispatch('deleted', ticket!.request_id);
		confirmOpen = false;
	}

	function statusVariant(status: Status) {
		if (status === 'Completed') return 'completed';
		if (status === 'Canceled') return 'failed';
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
			{ticket.title}
			{#if !editing}
				<button
					class="p-1 rounded-lg transition-colors text-gray-400 hover:text-[#C05B28]"
					style="background: var(--modal-subtle-bg); border: 1px solid var(--modal-section-border);"
					on:click={startEdit} aria-label="Edit ticket"
				>
					<Pencil size={14} />
				</button>
				<button
					class="p-1 rounded-lg transition-colors text-red-400 hover:text-red-600"
					style="background: var(--modal-subtle-bg); border: 1px solid var(--modal-section-border);"
					on:click={() => (confirmOpen = true)} aria-label="Delete ticket"
				>
					<Trash2 size={14} />
				</button>
			{/if}
		{/if}
	</svelte:fragment>

	{#if ticket}
		{#if editing}
			<form class="space-y-4">
				<Input id="ticketTitle" label="Title" bind:value={title} required />
				<Textarea id="ticketText" label="Description" bind:value={text} rows={6} />
			</form>
		{:else}
			<div class="space-y-4">
				<div class="rounded-2xl p-4" style="background: var(--modal-section-bg); border: 1px solid var(--modal-section-border);">
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
				</div>

				<div class="rounded-2xl p-4" style="background: var(--modal-section-bg); border: 1px solid var(--modal-section-border);">
					<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Description</p>
					<p class="text-sm text-gray-700 whitespace-pre-wrap">{ticket.text}</p>
				</div>

				<div class="rounded-2xl p-4" style="background: var(--modal-section-bg); border: 1px solid var(--modal-section-border);">
					<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">Submitted By</p>
					<p class="text-sm text-gray-700">{ticket.submitted_by}</p>
				</div>

				{#if ticket.llm_result}
					<div class="rounded-2xl p-4 space-y-3" style="background: var(--modal-section-bg); border: 1px solid var(--modal-section-border);">
						<p class="text-sm font-medium text-gray-700">AI Analysis</p>
						<div class="flex flex-wrap gap-1">
							{#each ticket.llm_result.topics as topic}
								<span class="px-2 py-0.5 rounded-full text-xs font-medium" style="background: rgba(192,91,40,0.12); color: #9a3d1a; border: 1px solid rgba(192,91,40,0.2);">{topic}</span>
							{/each}
						</div>
						{#if ticket.llm_result.confidence != null}
							<div class="flex items-center gap-2 text-sm text-gray-600">
								<span>Confidence:</span>
								<div class="flex-1 h-1.5 rounded-full overflow-hidden max-w-32" style="background: rgba(0,0,0,0.08);">
									<div class="h-full bg-[#C05B28] rounded-full" style="width: {ticket.llm_result.confidence * 100}%" />
								</div>
								<span class="font-medium">{Math.round(ticket.llm_result.confidence * 100)}%</span>
							</div>
						{/if}
						{#if ticket.llm_result.summary}
							<p class="text-sm text-gray-600 italic">{ticket.llm_result.summary}</p>
						{/if}
						{#if ticket.llm_result.draft_response}
							<div>
								<p class="text-sm font-medium text-gray-700 mb-1">Draft Response</p>
								<div class="rounded-xl p-3 text-sm text-gray-700 whitespace-pre-wrap" style="background: var(--modal-item-bg); border: 1px solid var(--modal-item-border);">
									{ticket.llm_result.draft_response}
								</div>
							</div>
						{/if}
					</div>
				{/if}

				<div class="rounded-2xl p-4 space-y-2" style="background: var(--modal-section-bg); border: 1px solid var(--modal-section-border);">
					<p class="text-sm font-medium text-gray-700 mb-2">Actions</p>
					{#each ticket.actions as action}
						<div class="flex items-start gap-2 p-3 rounded-xl" style="background: var(--modal-item-bg); border: 1px solid var(--modal-item-border);">
							<span class={`text-base ${action.success ? 'text-green-600' : 'text-red-500'}`}>
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
		{/if}
	{/if}

	<svelte:fragment slot="footer">
		{#if editing}
			<Button variant="secondary" on:click={cancelEdit} disabled={submitting}>Cancel</Button>
			<Button variant="primary" on:click={handleSave} loading={submitting}>Save Changes</Button>
		{:else}
			{#if ticket && !ticket.llm_result}
				<Button variant="secondary" on:click={handleClassify} loading={classifying}>
					<Sparkles size={14} />
					Classify
				</Button>
			{/if}
			<Button variant="secondary" on:click={handleClose}>Close</Button>
		{/if}
	</svelte:fragment>
</Modal>

<ConfirmModal
	open={confirmOpen}
	title="Delete Ticket"
	message="Delete ticket '{ticket?.title ?? ticket?.request_id ?? ''}'? This cannot be undone."
	on:confirm={handleDelete}
	on:cancel={() => (confirmOpen = false)}
/>
