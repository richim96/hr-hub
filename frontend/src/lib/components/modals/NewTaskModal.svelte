<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import { addTask } from '$lib/stores/tasks';
	import { employeeStore } from '$lib/stores/employees';

	export let open = false;

	const dispatch = createEventDispatcher<{ close: void }>();

	let selectedEmail = '';
	let emailQuery = '';
	let dropdownOpen = false;
	let title = '';
	let description = '';
	let assignee = '';
	let dueDate = '';
	const status = 'Pending';
	let submitting = false;
	let errors: Record<string, string> = {};

	$: employees = $employeeStore.items;
	$: filtered = emailQuery
		? employees.filter((e) => e.email.toLowerCase().includes(emailQuery.toLowerCase()))
		: employees;
	$: selectedEmployee = employees.find((e) => e.email === selectedEmail) ?? null;

	function selectEmail(email: string) {
		selectedEmail = email;
		emailQuery = email;
		dropdownOpen = false;
	}

	function handleEmailInput(e: Event) {
		emailQuery = (e.target as HTMLInputElement).value;
		selectedEmail = '';
		dropdownOpen = true;
	}

	function validate() {
		errors = {};
		if (!selectedEmployee) errors.email = 'Select a valid employee email';
		if (!title.trim()) errors.title = 'Required';
		if (!description.trim()) errors.description = 'Required';
		if (!assignee.trim()) errors.assignee = 'Required';
		if (!dueDate) errors.dueDate = 'Required';
		return Object.keys(errors).length === 0;
	}

	async function handleSubmit() {
		if (!validate() || !selectedEmployee) return;
		submitting = true;
		const ok = await addTask({
			employee_id: selectedEmployee.employee_id,
			employee_email: selectedEmployee.email,
			title,
			description,
			assignee,
			due_date: dueDate,
			status
		});
		submitting = false;
		if (ok) {
			reset();
			dispatch('close');
		}
	}

	function reset() {
		selectedEmail = emailQuery = title = description = assignee = dueDate = '';
		dropdownOpen = false;
		errors = {};
	}
</script>

<Modal {open} title="New Task" maxWidth="lg" on:close={() => { reset(); dispatch('close'); }}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div class="flex flex-col gap-1 relative">
			<label for="ntEmail" class="text-sm font-medium text-gray-600">Employee Email</label>
			<input
				id="ntEmail"
				type="text"
				autocomplete="off"
				placeholder="Search employee email…"
				value={emailQuery}
				on:input={handleEmailInput}
				on:focus={() => (dropdownOpen = true)}
				on:blur={() => setTimeout(() => (dropdownOpen = false), 150)}
				class="w-full px-3 py-2 text-sm rounded-2xl focus:outline-none focus:ring-2 focus:ring-[#C05B28]/50 transition-all"
				style="background: var(--glass-bg-input); backdrop-filter: var(--glass-blur-sm); -webkit-backdrop-filter: var(--glass-blur-sm); border: 1px solid {errors.email ? 'rgba(248,113,113,0.6)' : 'var(--glass-border-subtle)'};"
			/>
			{#if errors.email}
				<p class="text-xs text-red-500">{errors.email}</p>
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

		<Input id="ntTitle" label="Title" bind:value={title} required error={errors.title} placeholder="Set up email account" />
		<Textarea id="ntDesc" label="Description" bind:value={description} rows={3} required error={errors.description} />
		<Input id="ntAssignee" type="email" label="Assignee" bind:value={assignee} required error={errors.assignee} placeholder="it-team@company.com" />
		<Input id="ntDue" type="date" label="Due Date" bind:value={dueDate} required error={errors.dueDate} />
	</form>

	<svelte:fragment slot="footer">
		<Button variant="secondary" on:click={() => { reset(); dispatch('close'); }} disabled={submitting}>Cancel</Button>
		<Button variant="primary" on:click={handleSubmit} loading={submitting}>Create Task</Button>
	</svelte:fragment>
</Modal>
