<script lang="ts">
	import { onMount } from 'svelte';
	import { Plus, Search, SlidersHorizontal } from 'lucide-svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import TasksTable from '$lib/components/tables/TasksTable.svelte';
	import NewTaskModal from '$lib/components/modals/NewTaskModal.svelte';
	import TaskDetailModal from '$lib/components/modals/TaskDetailModal.svelte';
	import { taskStore, fetchTasks, setTaskFilter, filterTasks, removeTask } from '$lib/stores/tasks';
	import Pagination from '$lib/components/ui/Pagination.svelte';
	import type { ITTask, TaskStatus } from '$lib/types';

	onMount(() => {
		fetchTasks();
	});

	let showNewTask = false;
	let showTaskDetail = false;
	let selectedTask: ITTask | null = null;
	let showFilters = false;

	let sortKey: keyof ITTask = 'due_date';
	let sortDir: 'asc' | 'desc' = 'asc';

	function handleSort(e: CustomEvent<keyof ITTask>) {
		const key = e.detail;
		if (sortKey === key) {
			sortDir = sortDir === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDir = 'asc';
		}
		taskStore.update((s) => ({ ...s, page: 1 }));
	}

	$: store = $taskStore;
	$: filtered = filterTasks(store.items, store.filters);
	$: sortedFiltered = [...filtered].sort((a, b) => {
		const av = a[sortKey] ?? '';
		const bv = b[sortKey] ?? '';
		const cmp = String(av).localeCompare(String(bv), undefined, { numeric: true });
		return sortDir === 'asc' ? cmp : -cmp;
	});
	$: displayed = sortedFiltered.slice((store.page - 1) * store.pageSize, store.page * store.pageSize);
	$: totalPages = Math.max(1, Math.ceil(filtered.length / store.pageSize));

	const statusOptions: { value: TaskStatus | ''; label: string }[] = [
		{ value: '', label: 'All statuses' },
		{ value: 'Pending', label: 'Pending' },
		{ value: 'Completed', label: 'Completed' },
		{ value: 'Canceled', label: 'Canceled' }
	];

	function handleSearchInput(e: Event) {
		setTaskFilter({ search: (e.target as HTMLInputElement).value });
	}

	function handleStatusChange(e: Event) {
		setTaskFilter({ status: (e.target as HTMLSelectElement).value as TaskStatus | '' });
	}

	function handleEmployeeEmailInput(e: Event) {
		setTaskFilter({ employeeEmail: (e.target as HTMLInputElement).value });
	}

	function handleAssigneeInput(e: Event) {
		setTaskFilter({ assignee: (e.target as HTMLInputElement).value });
	}
</script>

<svelte:head>
	<title>IT Tasks — HR Hub</title>
</svelte:head>

<div class="flex flex-col h-full">
<!-- Page header -->
<div class="flex items-center justify-between mb-6 shrink-0">
	<div>
		<h2 class="text-xl font-semibold text-gray-900">IT Tasks</h2>
		<p class="text-sm text-gray-500 mt-0.5">
			{#if store.loading}Loading…{:else}{filtered.length} tasks{/if}
		</p>
	</div>
	<div class="flex gap-2">
		<Button variant="secondary" size="sm" on:click={() => (showFilters = !showFilters)}>
			<SlidersHorizontal size={15} />
			Filters
		</Button>
		<Button variant="primary" size="sm" on:click={() => (showNewTask = true)}>
			<Plus size={15} />
			New Task
		</Button>
	</div>
</div>

<!-- Search + filter bar -->
<Card padding="sm" class="mb-4 shrink-0">
	<div class="flex flex-col gap-3">
		<div class="relative">
			<Search size={15} class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
			<input
				type="text"
				placeholder="Search tasks…"
				value={store.filters.search}
				on:input={handleSearchInput}
				class="w-full pl-9 pr-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C05B28]-500"
			/>
		</div>

		{#if showFilters}
			<div class="grid grid-cols-2 md:grid-cols-3 gap-3 pt-2 border-t border-gray-100">
				<Select
					id="statusFilter"
					label="Status"
					value={store.filters.status}
					options={statusOptions}
					on:change={handleStatusChange}
				/>
				<div class="flex flex-col gap-1">
					<label for="empFilter" class="text-sm font-medium text-gray-700">Employee Email</label>
					<input
						id="empFilter"
						type="text"
						placeholder="employee@company.com"
						value={store.filters.employeeEmail}
						on:input={handleEmployeeEmailInput}
						class="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C05B28]-500"
					/>
				</div>
				<div class="flex flex-col gap-1">
					<label for="assigneeFilter" class="text-sm font-medium text-gray-700">Assignee</label>
					<input
						id="assigneeFilter"
						type="text"
						placeholder="it-team@company.com"
						value={store.filters.assignee}
						on:input={handleAssigneeInput}
						class="px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C05B28]-500"
					/>
				</div>
			</div>
		{/if}
	</div>
</Card>

<!-- Table -->
<Card padding="none" class="flex-1 min-h-0 flex flex-col overflow-hidden">
	{#if !store.loading && filtered.length > store.pageSize}
		<Pagination
			position="top"
			page={store.page}
			{totalPages}
			totalItems={filtered.length}
			pageSize={store.pageSize}
			on:first={() => taskStore.update((s) => ({ ...s, page: 1 }))}
			on:prev={() => taskStore.update((s) => ({ ...s, page: s.page - 1 }))}
			on:next={() => taskStore.update((s) => ({ ...s, page: s.page + 1 }))}
			on:last={() => taskStore.update((s) => ({ ...s, page: totalPages }))}
		/>
	{/if}
	<div class="flex-1 min-h-0">
		<TasksTable
			items={displayed}
			loading={store.loading}
			error={store.error}
			{sortKey}
			{sortDir}
			on:sort={handleSort}
			on:select={(e) => { selectedTask = e.detail; showTaskDetail = true; }}
		/>
	</div>
	{#if !store.loading && filtered.length > store.pageSize}
		<Pagination
			position="bottom"
			page={store.page}
			{totalPages}
			totalItems={filtered.length}
			pageSize={store.pageSize}
			on:first={() => taskStore.update((s) => ({ ...s, page: 1 }))}
			on:prev={() => taskStore.update((s) => ({ ...s, page: s.page - 1 }))}
			on:next={() => taskStore.update((s) => ({ ...s, page: s.page + 1 }))}
			on:last={() => taskStore.update((s) => ({ ...s, page: totalPages }))}
		/>
	{/if}
</Card>
</div>

<!-- Modals -->
<NewTaskModal bind:open={showNewTask} on:close={() => (showNewTask = false)} />

<TaskDetailModal
	bind:open={showTaskDetail}
	task={selectedTask}
	on:close={() => { showTaskDetail = false; selectedTask = null; }}
	on:deleted={async (e) => {
		showTaskDetail = false;
		selectedTask = null;
		await removeTask(e.detail);
	}}
/>
