<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { submitTicket } from '$lib/stores/tickets';
	import type { APIResponse, TicketRequest } from '$lib/types';

	export let open = false;

	const dispatch = createEventDispatcher<{ close: void; submitted: APIResponse }>();

	let submittedBy = '';
	let subject = '';
	let text = '';
	let submitting = false;
	let result: APIResponse | null = null;
	let errors: Record<string, string> = {};

	function validate() {
		errors = {};
		if (!submittedBy.trim() || !submittedBy.includes('@')) errors.submittedBy = 'Valid email required';
		if (!subject.trim()) errors.subject = 'Required';
		if (!text.trim()) errors.text = 'Required';
		return Object.keys(errors).length === 0;
	}

	async function handleSubmit() {
		if (!validate()) return;
		submitting = true;

		const payload: TicketRequest = {
			request_id: `req_${crypto.randomUUID()}`,
			request_type: 'people_ticket',
			submitted_by: submittedBy,
			subject,
			text
		};

		result = await submitTicket(payload);
		submitting = false;
		if (result) dispatch('submitted', result);
	}

	function handleClose() {
		submittedBy = subject = text = '';
		errors = {};
		result = null;
		dispatch('close');
	}
</script>

<Modal {open} title="Submit a Ticket" maxWidth="xl" on:close={handleClose}>
	{#if result}
		<!-- Success view -->
		<div class="space-y-5">
			<div class="flex items-center gap-3">
				<Badge variant={result.status === 'completed' ? 'completed' : 'failed'}>
					{result.status}
				</Badge>
				<span class="text-sm text-gray-500 font-mono">{result.request_id}</span>
			</div>

			{#if result.llm_result}
				<div class="space-y-3">
					<div>
						<p class="text-sm font-medium text-gray-700 mb-1">Detected Topics</p>
						<div class="flex flex-wrap gap-1">
							{#each result.llm_result.topics as topic}
								<span class="px-2 py-0.5 bg-[#fdf4ef] text-[#9a3d1a] rounded-full text-xs">{topic}</span>
							{/each}
						</div>
					</div>

					<div>
						<p class="text-sm font-medium text-gray-700 mb-1">
							Confidence: {Math.round(result.llm_result.confidence * 100)}%
						</p>
						<div class="h-1.5 bg-gray-200 rounded-full overflow-hidden">
							<div
								class="h-full bg-[#fdf4ef]0 rounded-full"
								style="width: {result.llm_result.confidence * 100}%"
							/>
						</div>
					</div>

					<div>
						<p class="text-sm font-medium text-gray-700 mb-1">Draft Response</p>
						<div class="bg-gray-50 rounded-lg p-4 text-sm text-gray-700 whitespace-pre-wrap border border-gray-200">
							{result.llm_result.draft_response}
						</div>
					</div>
				</div>
			{/if}

			<div class="space-y-2">
				<p class="text-sm font-medium text-gray-700">Actions Taken</p>
				{#each result.actions as action}
					<div class="flex items-start gap-2 text-sm">
						<span class={action.success ? 'text-green-500' : 'text-red-500'}>
							{action.success ? '✓' : '✗'}
						</span>
						<div>
							<span class="font-medium">{action.action}</span>
							<p class="text-gray-500 text-xs mt-0.5">{action.details}</p>
						</div>
					</div>
				{/each}
			</div>
		</div>
	{:else}
		<!-- Form view -->
		<form on:submit|preventDefault={handleSubmit} class="space-y-4">
			<Input
				id="ticketEmail"
				type="email"
				label="Submitted By"
				bind:value={submittedBy}
				required
				error={errors.submittedBy}
				placeholder="employee@company.com"
			/>
			<Input
				id="ticketSubject"
				label="Subject"
				bind:value={subject}
				required
				error={errors.subject}
				placeholder="Address change and documentation"
			/>
			<Textarea
				id="ticketText"
				label="Description"
				bind:value={text}
				required
				error={errors.text}
				rows={6}
				placeholder="Describe your request in detail…"
			/>
		</form>
	{/if}

	<svelte:fragment slot="footer">
		{#if result}
			<Button variant="primary" on:click={handleClose}>Done</Button>
		{:else}
			<Button variant="secondary" on:click={handleClose} disabled={submitting}>Cancel</Button>
			<Button variant="primary" on:click={handleSubmit} loading={submitting}>Submit Ticket</Button>
		{/if}
	</svelte:fragment>
</Modal>
