<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import { editTask, removeTask } from '$lib/stores/tasks';
	import type { ITTask, TaskStatus } from '$lib/types';

	export let open = false;
	export let task: ITTask | null = null;

	const dispatch = createEventDispatcher<{ close: void }>();

	let title = '';
	let description = '';
	let assignee = '';
	let dueDate = '';
	let status: TaskStatus | '' = '';
	let submitting = false;
	let confirmDelete = false;

	$: if (task && open) {
		title = task.title;
		description = task.description ?? '';
		assignee = task.assignee ?? '';
		dueDate = task.due_date?.split('T')[0] ?? '';
		status = task.status ?? '';
	}

	const statusOptions = [
		{ value: 'Pending', label: 'Pending' },
		{ value: 'Completed', label: 'Completed' },
		{ value: 'Canceled', label: 'Canceled' }
	];

	async function handleSave() {
		if (!task) return;
		submitting = true;
		await editTask(task.task_id, {
			title,
			description: description || null,
			assignee: assignee || null,
			due_date: dueDate || null,
			status: (status as TaskStatus) || null
		});
		submitting = false;
		dispatch('close');
	}

	async function handleDelete() {
		if (!task) return;
		submitting = true;
		await removeTask(task.task_id);
		submitting = false;
		confirmDelete = false;
		dispatch('close');
	}
</script>

<Modal {open} title="Edit Task" maxWidth="lg" on:close={() => dispatch('close')}>
	{#if task}
		{#if confirmDelete}
			<div class="text-center py-4 space-y-3">
				<p class="text-gray-700">Are you sure you want to delete this task?</p>
				<p class="text-sm font-mono text-gray-500">{task.task_id}</p>
			</div>
		{:else}
			<form class="space-y-4">
				<Input id="taskTitle" label="Title" bind:value={title} required />
				<Textarea id="taskDesc" label="Description" bind:value={description} rows={3} />
				<Input id="taskAssignee" type="email" label="Assignee" bind:value={assignee} placeholder="it-team@company.com" />
				<Input id="taskDue" type="date" label="Due Date" bind:value={dueDate} />
				<Select id="taskStatus" label="Status" bind:value={status} options={statusOptions} />
			</form>
		{/if}
	{/if}

	<svelte:fragment slot="footer">
		{#if confirmDelete}
			<Button variant="secondary" on:click={() => (confirmDelete = false)}>Cancel</Button>
			<Button variant="danger" on:click={handleDelete} loading={submitting}>Delete</Button>
		{:else}
			<Button variant="danger" size="sm" on:click={() => (confirmDelete = true)}>Delete Task</Button>
			<div class="flex-1" />
			<Button variant="secondary" on:click={() => dispatch('close')} disabled={submitting}>Cancel</Button>
			<Button variant="primary" on:click={handleSave} loading={submitting}>Save Changes</Button>
		{/if}
	</svelte:fragment>
</Modal>
