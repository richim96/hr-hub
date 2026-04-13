<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { ChevronUp, ChevronDown, Eye } from 'lucide-svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Skeleton from '$lib/components/ui/Skeleton.svelte';
	import type { FullEmployee } from '$lib/types';

	export let items: FullEmployee[] = [];
	export let loading = false;
	export let error: string | null = null;

	const dispatch = createEventDispatcher<{ select: FullEmployee }>();

	type SortKey = keyof FullEmployee;
	let sortKey: SortKey = 'last_name';
	let sortDir: 'asc' | 'desc' = 'asc';

	function toggleSort(key: SortKey) {
		if (sortKey === key) {
			sortDir = sortDir === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDir = 'asc';
		}
	}

	$: sorted = [...items].sort((a, b) => {
		const av = a[sortKey] ?? '';
		const bv = b[sortKey] ?? '';
		const cmp = String(av).localeCompare(String(bv), undefined, { numeric: true });
		return sortDir === 'asc' ? cmp : -cmp;
	});

	function riskClass(risk: number | null | undefined) {
		if (risk == null) return 'text-gray-400';
		if (risk >= 0.7) return 'risk-high font-semibold';
		if (risk >= 0.4) return 'risk-medium';
		return 'risk-low';
	}

	function riskLabel(risk: number | null | undefined) {
		if (risk == null) return '—';
		return `${Math.round(risk * 100)}%`;
	}

	const columns = [
		{ key: 'employee_id' as SortKey, label: 'ID' },
		{ key: 'last_name' as SortKey, label: 'Name' },
		{ key: 'department' as SortKey, label: 'Department' },
		{ key: 'manager_email' as SortKey, label: 'Manager' },
		{ key: 'laptop' as SortKey, label: 'Laptop' },
		{ key: 'attrition_risk' as SortKey, label: 'Attrition Risk' }
	];
</script>

<div class="overflow-x-auto">
	<table class="w-full text-sm">
		<thead>
			<tr class="border-b border-gray-200 bg-gray-50">
				{#each columns as col}
					<th class="px-4 py-3 text-left font-medium text-gray-600 whitespace-nowrap">
						<button
							class="flex items-center gap-1 hover:text-gray-900"
							on:click={() => toggleSort(col.key)}
						>
							{col.label}
							{#if sortKey === col.key}
								{#if sortDir === 'asc'}<ChevronUp size={14} />{:else}<ChevronDown size={14} />{/if}
							{/if}
						</button>
					</th>
				{/each}
				<th class="px-4 py-3 text-left font-medium text-gray-600">Equipment</th>
				<th class="w-10" />
			</tr>
		</thead>
		<tbody>
			{#if loading}
				<tr>
					<td colspan="8" class="px-4 py-6">
						<Skeleton rows={8} cols={7} />
					</td>
				</tr>
			{:else if error}
				<tr>
					<td colspan="8" class="px-4 py-12 text-center text-gray-500">
						<p class="text-red-500 font-medium">{error}</p>
						<p class="text-sm mt-1 text-gray-400">Employee list endpoint is not yet available on the backend.</p>
					</td>
				</tr>
			{:else if sorted.length === 0}
				<tr>
					<td colspan="8" class="px-4 py-12 text-center text-gray-500">
						<p class="font-medium">No employees found</p>
						<p class="text-xs mt-1">Try adjusting your filters or hire a new employee.</p>
					</td>
				</tr>
			{:else}
				{#each sorted as emp}
					<tr
						class="border-b border-gray-100 hover:bg-[#fdf4ef]/40 cursor-pointer transition-colors"
						on:click={() => dispatch('select', emp)}
					>
						<td class="px-4 py-3 font-mono text-xs text-gray-500">{emp.employee_id}</td>
						<td class="px-4 py-3 font-medium text-gray-900">
							{emp.first_name} {emp.last_name}
							<div class="text-xs text-gray-500 font-normal">{emp.email}</div>
						</td>
						<td class="px-4 py-3">
							<Badge variant="info">{emp.department ?? '—'}</Badge>
						</td>
						<td class="px-4 py-3 text-gray-600 text-xs">{emp.manager_email}</td>
						<td class="px-4 py-3 text-gray-700">{emp.laptop ?? '—'}</td>
						<td class="px-4 py-3 {riskClass(emp.attrition_risk)}">
							{riskLabel(emp.attrition_risk)}
						</td>
						<td class="px-4 py-3 text-xs text-gray-500">
							{#if emp.monitor}<span class="mr-1">🖥</span>{/if}
							{#if emp.headset}<span>🎧</span>{/if}
						</td>
						<td class="px-4 py-3">
							<button
								class="p-1.5 rounded text-gray-400 hover:text-[#C05B28] hover:bg-[#fdf4ef] transition-colors"
								on:click|stopPropagation={() => dispatch('select', emp)}
								aria-label="View employee"
							>
								<Eye size={15} />
							</button>
						</td>
					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
</div>
