<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import { submitTicket } from '$lib/stores/tickets';
	import { employeeStore } from '$lib/stores/employees';
	import type { APIResponse, TicketRequest } from '$lib/types';

	export let open = false;

	const dispatch = createEventDispatcher<{ close: void; submitted: APIResponse }>();

	let submittedBy = '';
	let emailQuery = '';
	let dropdownOpen = false;
	let subject = '';
	let text = '';
	let submitting = false;
	let result: APIResponse | null = null;
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
		if (!subject.trim()) errors.subject = 'Required';
		if (!text.trim()) errors.text = 'Required';
		return Object.keys(errors).length === 0;
	}

	async function handleSubmit() {
		if (!validate()) return;
		submitting = true;

		const payload: TicketRequest = {
			request_id: `ticket_${crypto.randomUUID()}`,
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
		submittedBy = emailQuery = subject = text = '';
		dropdownOpen = false;
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
			<!-- Submitted By — searchable employee email -->
			<div class="flex flex-col gap-1 relative">
				<label for="ticketEmail" class="text-sm font-medium text-gray-700">Submitted By</label>
				<input
					id="ticketEmail"
					type="text"
					autocomplete="off"
					placeholder="Search employee email…"
					value={emailQuery}
					on:input={handleEmailInput}
					on:focus={() => (dropdownOpen = true)}
					on:blur={() => setTimeout(() => (dropdownOpen = false), 150)}
					class="w-full px-3 py-2 text-sm border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C05B28]
					       {errors.submittedBy ? 'border-red-400' : 'border-gray-300'}"
				/>
				{#if errors.submittedBy}
					<p class="text-xs text-red-500">{errors.submittedBy}</p>
				{/if}
				{#if dropdownOpen && filtered.length > 0}
					<ul class="absolute top-full left-0 right-0 z-50 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto">
						{#each filtered.slice(0, 50) as emp}
							<li>
								<button
									type="button"
									class="w-full text-left px-3 py-2 text-sm hover:bg-[#fdf4ef] transition-colors"
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
