<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { submitTicket } from '$lib/stores/tickets';
	import { randomUUID } from '$lib/utils';
	import { employeeStore } from '$lib/stores/employees';
	import type { Ticket, TicketRequest } from '$lib/types';

	export let open = false;

	const dispatch = createEventDispatcher<{ close: void; submitted: Ticket }>();

	let submittedBy = '';
	let emailQuery = '';
	let dropdownOpen = false;
	let title = '';
	let text = '';
	let submitting = false;
	let result: Ticket | null = null;
	let errors: Record<string, string> = {};

	$: employees = $employeeStore.items;
	$: filtered = emailQuery
		? employees.filter((e) => e.email.toLowerCase().includes(emailQuery.toLowerCase()))
		: employees;

	function selectEmail(email: string) {
		submittedBy = email;
		emailQuery = email;
		dropdownOpen = false;
	}

	function handleEmailInput(e: Event) {
		emailQuery = (e.target as HTMLInputElement).value;
		submittedBy = '';
		dropdownOpen = true;
	}

	function validate() {
		errors = {};
		if (!submittedBy) errors.submittedBy = 'Select a valid employee email';
		if (!title.trim()) errors.title = 'Required';
		if (!text.trim()) errors.text = 'Required';
		return Object.keys(errors).length === 0;
	}

	async function handleSubmit() {
		if (!validate()) return;
		submitting = true;

		const payload: TicketRequest = {
			request_id: `ticket_${randomUUID()}`,
			request_type: 'people_ticket',
			submitted_by: submittedBy,
			title,
			text
		};

		result = await submitTicket(payload);
		submitting = false;
		if (result) dispatch('submitted', result);
	}

	function handleClose() {
		submittedBy = emailQuery = title = text = '';
		dropdownOpen = false;
		errors = {};
		result = null;
		dispatch('close');
	}
</script>

<Modal {open} title="Submit a Ticket" maxWidth="xl" on:close={handleClose}>
	{#if result}
		<div class="space-y-4">
			<div class="flex items-center gap-3">
				<Badge variant={result.status === 'Completed' ? 'completed' : result.status === 'Canceled' ? 'failed' : 'pending'}>
					{result.status}
				</Badge>
				<span class="text-sm text-gray-500 font-mono">{result.request_id}</span>
			</div>

			{#if result.llm_result}
				<div class="space-y-3">
					<div class="rounded-2xl p-4" style="background: rgba(255,255,255,0.3); border: 1px solid rgba(255,255,255,0.4);">
						<p class="text-sm font-medium text-gray-700 mb-2">Detected Topics</p>
						<div class="flex flex-wrap gap-1">
							{#each result.llm_result.topics as topic}
								<span class="px-2 py-0.5 rounded-full text-xs font-medium" style="background: rgba(192,91,40,0.12); color: #9a3d1a; border: 1px solid rgba(192,91,40,0.2);">{topic}</span>
							{/each}
						</div>
					</div>

					<div class="rounded-2xl p-4" style="background: rgba(255,255,255,0.3); border: 1px solid rgba(255,255,255,0.4);">
						<p class="text-sm font-medium text-gray-700 mb-2">
							Confidence: {Math.round(result.llm_result.confidence * 100)}%
						</p>
						<div class="h-1.5 rounded-full overflow-hidden" style="background: rgba(0,0,0,0.08);">
							<div
								class="h-full bg-[#C05B28] rounded-full"
								style="width: {result.llm_result.confidence * 100}%"
							/>
						</div>
					</div>

					<div class="rounded-2xl p-4" style="background: rgba(255,255,255,0.3); border: 1px solid rgba(255,255,255,0.4);">
						<p class="text-sm font-medium text-gray-700 mb-2">Draft Response</p>
						<p class="text-sm text-gray-700 whitespace-pre-wrap">{result.llm_result.draft_response}</p>
					</div>
				</div>
			{/if}

			<div class="rounded-2xl p-4 space-y-2" style="background: rgba(255,255,255,0.3); border: 1px solid rgba(255,255,255,0.4);">
				<p class="text-sm font-medium text-gray-700">Actions Taken</p>
				{#each result.actions as action}
					<div class="flex items-start gap-2 text-sm">
						<span class={action.success ? 'text-green-600' : 'text-red-500'}>{action.success ? '✓' : '✗'}</span>
						<div>
							<span class="font-medium">{action.action}</span>
							<p class="text-gray-500 text-xs mt-0.5">{action.details}</p>
						</div>
					</div>
				{/each}
			</div>
		</div>
	{:else}
		<form on:submit|preventDefault={handleSubmit} class="space-y-4">
			<div class="flex flex-col gap-1 relative">
				<label for="ticketEmail" class="text-sm font-medium text-gray-600">Submitted By</label>
				<input
					id="ticketEmail"
					type="text"
					autocomplete="off"
					placeholder="Search employee email…"
					value={emailQuery}
					on:input={handleEmailInput}
					on:focus={() => (dropdownOpen = true)}
					on:blur={() => setTimeout(() => (dropdownOpen = false), 150)}
					class="w-full px-3 py-2 text-sm rounded-2xl focus:outline-none focus:ring-2 focus:ring-[#C05B28]/50 transition-all"
					style="background: var(--glass-bg-input); backdrop-filter: var(--glass-blur-sm); -webkit-backdrop-filter: var(--glass-blur-sm); border: 1px solid {errors.submittedBy ? 'rgba(248,113,113,0.6)' : 'var(--glass-border-subtle)'};"
				/>
				{#if errors.submittedBy}
					<p class="text-xs text-red-500">{errors.submittedBy}</p>
				{/if}
				{#if dropdownOpen && filtered.length > 0}
					<ul class="absolute top-full left-0 right-0 z-50 mt-1 rounded-2xl max-h-48 overflow-y-auto" style="background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.6); box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
						{#each filtered.slice(0, 50) as emp}
							<li>
								<button
									type="button"
									class="w-full text-left px-3 py-2 text-sm transition-colors hover:bg-white/50 first:rounded-t-2xl last:rounded-b-2xl"
									on:mousedown={() => selectEmail(emp.email)}
								>
									<span class="font-medium text-gray-900">{emp.first_name} {emp.last_name}</span>
									<span class="text-gray-500 ml-2">{emp.email}</span>
								</button>
							</li>
						{/each}
					</ul>
				{/if}
			</div>

			<Input id="ticketTitle" label="Title" bind:value={title} required error={errors.title} placeholder="Address change and documentation" />
			<Textarea id="ticketText" label="Description" bind:value={text} required error={errors.text} rows={6} placeholder="Describe your request in detail…" />
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
