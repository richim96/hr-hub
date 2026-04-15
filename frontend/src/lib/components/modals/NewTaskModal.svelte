<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import { addTask } from '$lib/stores/tasks';

	export let open = false;
	export let prefillEmployeeId = '';

	const dispatch = createEventDispatcher<{ close: void }>();

	let employeeId = '';
	let title = '';
	let description = '';
	let assignee = '';
	let dueDate = '';
	const status = 'Pending';
	let submitting = false;
	let errors: Record<string, string> = {};

	$: if (open) employeeId = prefillEmployeeId;


	function validate() {
		errors = {};
		if (!employeeId.trim()) errors.employeeId = 'Required';
		if (!title.trim()) errors.title = 'Required';
		if (!description.trim()) errors.description = 'Required';
		if (!assignee.trim()) errors.assignee = 'Required';
		if (!dueDate) errors.dueDate = 'Required';
		return Object.keys(errors).length === 0;
	}

	async function handleSubmit() {
		if (!validate()) return;
		submitting = true;
		const ok = await addTask({
			employee_id: employeeId,
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
		employeeId = title = description = assignee = dueDate = '';
		errors = {};
	}
</script>

<Modal {open} title="New Task" maxWidth="lg" on:close={() => { reset(); dispatch('close'); }}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<Input
			id="ntEmployeeId"
			label="Employee ID"
			bind:value={employeeId}
			required
			error={errors.employeeId}
			placeholder="emp_abc123"
		/>
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
