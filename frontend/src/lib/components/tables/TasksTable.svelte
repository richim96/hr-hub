<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { ChevronUp, ChevronDown } from 'lucide-svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Skeleton from '$lib/components/ui/Skeleton.svelte';
	import type { ITTask, TaskStatus } from '$lib/types';

	export let items: ITTask[] = [];
	export let loading = false;
	export let error: string | null = null;
	export let sortKey: keyof ITTask = 'due_date';
	export let sortDir: 'asc' | 'desc' = 'asc';

	const dispatch = createEventDispatcher<{ select: ITTask; sort: keyof ITTask }>();

	function statusVariant(status: TaskStatus | null | undefined) {
		if (status === 'Completed') return 'completed';
		if (status === 'Canceled') return 'canceled';
		return 'pending';
	}

	function formatDate(d: string | null | undefined) {
		if (!d) return '—';
		return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
	}

	const columns: { key: keyof ITTask; label: string }[] = [
		{ key: 'employee_email', label: 'Employee' },
		{ key: 'title', label: 'Title' },
		{ key: 'assignee', label: 'Assignee' },
		{ key: 'status', label: 'Status' },
		{ key: 'due_date', label: 'Due Date' },
		{ key: 'task_id', label: 'Task ID' }
	];
</script>

<div class="overflow-auto h-full">
	<table class="w-full text-sm">
		<thead class="sticky top-0 z-10 bg-gray-50">
			<tr class="border-b border-gray-200">
				{#each columns as col}
					<th class="px-4 py-2 text-left font-medium text-gray-600 whitespace-nowrap">
						<button class="flex items-center gap-1 hover:text-gray-900" on:click={() => dispatch('sort', col.key)}>
							{col.label}
							{#if sortKey === col.key}
								{#if sortDir === 'asc'}<ChevronUp size={14} />{:else}<ChevronDown size={14} />{/if}
							{/if}
						</button>
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#if loading}
				<tr><td colspan="6" class="px-4 py-6"><Skeleton rows={8} cols={6} /></td></tr>
			{:else if error}
				<tr>
					<td colspan="6" class="px-4 py-12 text-center text-gray-500">
						<p class="text-red-500 font-medium">{error}</p>
						<p class="text-sm mt-1 text-gray-400">Tasks endpoint is not yet available on the backend.</p>
					</td>
				</tr>
			{:else if items.length === 0}
				<tr>
					<td colspan="6" class="px-4 py-12 text-center text-gray-500">
						<p class="font-medium">No tasks found</p>
						<p class="text-xs mt-1">Tasks are created automatically during new hire onboarding.</p>
					</td>
				</tr>
			{:else}
				{#each items as task}
					<tr
						class="border-b border-gray-100 hover:bg-[#fdf4ef]/30 transition-colors cursor-pointer"
						on:click={() => dispatch('select', task)}
					>
						<td class="px-4 py-3 text-xs text-gray-600">{task.employee_email ?? '—'}</td>
						<td class="px-4 py-3 font-medium text-gray-900">
							{task.title}
							{#if task.description}
								<p class="text-xs text-gray-500 font-normal truncate max-w-xs">{task.description}</p>
							{/if}
						</td>
						<td class="px-4 py-3 text-gray-600 text-xs">{task.assignee ?? '—'}</td>
						<td class="px-4 py-2">
							<Badge variant={statusVariant(task.status)}>{task.status ?? 'Pending'}</Badge>
						</td>
						<td class="px-4 py-3 text-gray-600">{formatDate(task.due_date)}</td>
						<td class="px-4 py-3 font-mono text-xs text-gray-400">{task.task_id}</td>
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
</div>
