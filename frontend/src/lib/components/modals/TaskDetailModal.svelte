<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Pencil, Trash2 } from 'lucide-svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import Textarea from '$lib/components/ui/Textarea.svelte';
	import { editTask } from '$lib/stores/tasks';
	import type { ITTask, Status } from '$lib/types';

	export let open = false;
	export let task: ITTask | null = null;

	const dispatch = createEventDispatcher<{ close: void; deleted: string }>();

	let editing = false;
	let submitting = false;
	let confirmOpen = false;
	let errors: Record<string, string> = {};

	let title = '';
	let description = '';
	let assignee = '';
	let dueDate = '';
	let status: Status | '' = '';

	const statusOptions = [
		{ value: 'Pending', label: 'Pending' },
		{ value: 'Completed', label: 'Completed' },
		{ value: 'Canceled', label: 'Canceled' }
	];

	$: if (task && open) { editing = false; }

	function startEdit() {
		if (!task) return;
		title = task.title;
		description = task.description ?? '';
		assignee = task.assignee ?? '';
		dueDate = task.due_date?.split('T')[0] ?? '';
		status = task.status ?? '';
		editing = true;
	}

	function cancelEdit() {
		editing = false;
		errors = {};
	}

	function validate() {
		errors = {};
		if (!title.trim()) errors.title = 'Required';
		if (!description.trim()) errors.description = 'Required';
		if (!assignee.trim()) errors.assignee = 'Required';
		if (!dueDate) errors.dueDate = 'Required';
		if (!status) errors.status = 'Required';
		return Object.keys(errors).length === 0;
	}

	async function handleSave() {
		if (!task || !validate()) return;
		submitting = true;
		await editTask(task.task_id, { title, description, assignee, due_date: dueDate, status: status as Status });
		submitting = false;
		editing = false;
	}

	async function handleDelete() {
		if (!task) return;
		dispatch('deleted', task.task_id);
		confirmOpen = false;
	}

	function statusVariant(s: Status | null | undefined) {
		if (s === 'Completed') return 'completed';
		if (s === 'Canceled') return 'canceled';
		return 'pending';
	}

	function formatDate(d: string | null | undefined) {
		if (!d) return '—';
		return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
	}

	function handleClose() {
		editing = false;
		dispatch('close');
	}
</script>

<Modal {open} maxWidth="lg" on:close={handleClose}>
	<svelte:fragment slot="title">
		{#if task}
			{task.title}
			{#if !editing}
				<button
					class="p-1 rounded-lg transition-colors text-gray-400 hover:text-[#C05B28]"
					style="background: var(--modal-subtle-bg); border: 1px solid var(--modal-section-border);"
					on:click={startEdit} aria-label="Edit task"
				>
					<Pencil size={14} />
				</button>
				<button
					class="p-1 rounded-lg transition-colors text-red-400 hover:text-red-600"
					style="background: var(--modal-subtle-bg); border: 1px solid var(--modal-section-border);"
					on:click={() => (confirmOpen = true)} aria-label="Delete task"
				>
					<Trash2 size={14} />
				</button>
			{/if}
		{/if}
	</svelte:fragment>

	{#if task}
		{#if editing}
			<form class="space-y-4">
				<Input id="taskTitle" label="Title" bind:value={title} required error={errors.title} />
				<Textarea id="taskDesc" label="Description" bind:value={description} rows={3} required error={errors.description} />
				<Input id="taskAssignee" type="email" label="Assignee" bind:value={assignee} required error={errors.assignee} placeholder="it-team@company.com" />
				<Input id="taskDue" type="date" label="Due Date" bind:value={dueDate} required error={errors.dueDate} />
				<Select id="taskStatus" label="Status" bind:value={status} options={statusOptions} required error={errors.status} />
			</form>
		{:else}
			<div class="space-y-4">
				<div class="rounded-2xl p-4" style="background: var(--modal-section-bg); border: 1px solid var(--modal-section-border);">
					<div class="space-y-3">
						<div>
							<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">Task ID</p>
							<p class="text-sm font-mono text-gray-600">{task.task_id}</p>
						</div>
						<div>
							<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Status</p>
							<Badge variant={statusVariant(task.status)}>{task.status ?? 'Pending'}</Badge>
						</div>
					</div>
				</div>

				{#if task.description}
					<div class="rounded-2xl p-4" style="background: var(--modal-section-bg); border: 1px solid var(--modal-section-border);">
						<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Description</p>
						<p class="text-sm text-gray-700 whitespace-pre-wrap">{task.description}</p>
					</div>
				{/if}

				<div class="rounded-2xl p-4" style="background: var(--modal-section-bg); border: 1px solid var(--modal-section-border);">
					<div class="grid grid-cols-2 gap-4">
						<div>
							<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">Assignee</p>
							<p class="text-sm text-gray-700">{task.assignee ?? '—'}</p>
						</div>
						<div>
							<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">Due Date</p>
							<p class="text-sm text-gray-700">{formatDate(task.due_date)}</p>
						</div>
						{#if task.employee_email}
							<div class="col-span-2">
								<p class="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">Employee Email</p>
								<p class="text-sm text-gray-700">{task.employee_email}</p>
							</div>
						{/if}
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
	title="Delete Task"
	message="Delete task '{task?.title ?? ''}'? This cannot be undone."
	confirmLabel="Delete"
	on:confirm={handleDelete}
	on:cancel={() => (confirmOpen = false)}
/>
