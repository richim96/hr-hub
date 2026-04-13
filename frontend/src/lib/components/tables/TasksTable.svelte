<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Pencil, Trash2, ChevronUp, ChevronDown } from 'lucide-svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Skeleton from '$lib/components/ui/Skeleton.svelte';
	import type { ITTask, TaskStatus } from '$lib/types';

	export let items: ITTask[] = [];
	export let loading = false;
	export let error: string | null = null;

	const dispatch = createEventDispatcher<{ edit: ITTask; delete: string }>();

	type SortKey = keyof ITTask;
	let sortKey: SortKey = 'due_date';
	let sortDir: 'asc' | 'desc' = 'asc';

	function toggleSort(key: SortKey) {
		sortKey === key ? (sortDir = sortDir === 'asc' ? 'desc' : 'asc') : ((sortKey = key), (sortDir = 'asc'));
	}

	$: sorted = [...items].sort((a, b) => {
		const av = a[sortKey] ?? '';
		const bv = b[sortKey] ?? '';
		const cmp = String(av).localeCompare(String(bv));
		return sortDir === 'asc' ? cmp : -cmp;
	});

	function statusVariant(status: TaskStatus | null | undefined) {
		if (status === 'Completed') return 'completed';
		if (status === 'Canceled') return 'canceled';
		return 'pending';
	}

	function formatDate(d: string | null | undefined) {
		if (!d) return '—';
		return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
	}

	const columns: { key: SortKey; label: string }[] = [
		{ key: 'task_id', label: 'Task ID' },
		{ key: 'title', label: 'Title' },
		{ key: 'employee_id', label: 'Employee' },
		{ key: 'assignee', label: 'Assignee' },
		{ key: 'status', label: 'Status' },
		{ key: 'due_date', label: 'Due Date' }
	];
</script>

<div class="overflow-x-auto">
	<table class="w-full text-sm">
		<thead>
			<tr class="border-b border-gray-200 bg-gray-50">
				{#each columns as col}
					<th class="px-4 py-3 text-left font-medium text-gray-600 whitespace-nowrap">
						<button class="flex items-center gap-1 hover:text-gray-900" on:click={() => toggleSort(col.key)}>
							{col.label}
							{#if sortKey === col.key}
								{#if sortDir === 'asc'}<ChevronUp size={14} />{:else}<ChevronDown size={14} />{/if}
							{/if}
						</button>
					</th>
				{/each}
				<th class="w-20" />
			</tr>
		</thead>
		<tbody>
			{#if loading}
				<tr><td colspan="7" class="px-4 py-6"><Skeleton rows={8} cols={6} /></td></tr>
			{:else if error}
				<tr>
					<td colspan="7" class="px-4 py-12 text-center text-gray-500">
						<p class="text-red-500 font-medium">{error}</p>
						<p class="text-sm mt-1 text-gray-400">Tasks endpoint is not yet available on the backend.</p>
					</td>
				</tr>
			{:else if sorted.length === 0}
				<tr>
					<td colspan="7" class="px-4 py-12 text-center text-gray-500">
						<p class="font-medium">No tasks found</p>
						<p class="text-xs mt-1">Tasks are created automatically during new hire onboarding.</p>
					</td>
				</tr>
			{:else}
				{#each sorted as task}
					<tr class="border-b border-gray-100 hover:bg-[#fdf4ef]/30 transition-colors">
						<td class="px-4 py-3 font-mono text-xs text-gray-500">{task.task_id}</td>
						<td class="px-4 py-3 font-medium text-gray-900">
							{task.title}
							{#if task.description}
								<p class="text-xs text-gray-500 font-normal truncate max-w-xs">{task.description}</p>
							{/if}
						</td>
						<td class="px-4 py-3 font-mono text-xs text-gray-600">{task.employee_id}</td>
						<td class="px-4 py-3 text-gray-600 text-xs">{task.assignee ?? '—'}</td>
						<td class="px-4 py-3">
							<Badge variant={statusVariant(task.status)}>{task.status ?? 'Pending'}</Badge>
						</td>
						<td class="px-4 py-3 text-gray-600">{formatDate(task.due_date)}</td>
						<td class="px-4 py-3">
							<div class="flex gap-1">
								<button
									class="p-1.5 rounded text-gray-400 hover:text-[#C05B28] hover:bg-[#fdf4ef] transition-colors"
									on:click={() => dispatch('edit', task)}
									aria-label="Edit task"
								>
									<Pencil size={14} />
								</button>
								<button
									class="p-1.5 rounded text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
									on:click={() => dispatch('delete', task.task_id)}
									aria-label="Delete task"
								>
									<Trash2 size={14} />
								</button>
							</div>
						</td>
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
</div>
