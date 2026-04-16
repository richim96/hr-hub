<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { ChevronUp, ChevronDown } from 'lucide-svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Skeleton from '$lib/components/ui/Skeleton.svelte';
	import type { FullEmployee } from '$lib/types';

	export let items: FullEmployee[] = [];
	export let loading = false;
	export let error: string | null = null;
	export let sortKey: keyof FullEmployee = 'last_name';
	export let sortDir: 'asc' | 'desc' = 'asc';
	export let maxHeight = 'calc(100vh - 20rem)';

	const dispatch = createEventDispatcher<{ select: FullEmployee; sort: keyof FullEmployee }>();

	function riskBadgeVariant(risk: number | null | undefined): 'failed' | 'pending' | 'completed' | 'default' {
		if (risk == null) return 'default';
		if (risk >= 0.7) return 'failed';
		if (risk >= 0.4) return 'pending';
		return 'completed';
	}

	function riskLabel(risk: number | null | undefined) {
		if (risk == null) return '—';
		return `${Math.round(risk * 100)}%`;
	}

const columns: { key: keyof FullEmployee; label: string }[] = [
		{ key: 'last_name', label: 'Name' },
		{ key: 'email', label: 'Email' },
		{ key: 'department', label: 'Department' },
		{ key: 'salary', label: 'Salary' },
		{ key: 'years_at_company', label: 'Tenure' },
		{ key: 'avg_monthly_hours', label: 'Avg Hrs/mo' },
		{ key: 'active_projects', label: 'Projects' },
		{ key: 'manager_email', label: 'Manager' },
		{ key: 'attrition_risk', label: 'Attrition Risk' }
	];
</script>

<div class="overflow-auto" style="max-height: {maxHeight}">
	<table class="w-full text-sm">
		<thead class="sticky top-0 z-10 bg-gray-50">
			<tr class="border-b border-gray-200">
				{#each columns as col}
					<th class="px-4 py-2 text-left font-medium text-gray-600 whitespace-nowrap">
						<button
							class="flex items-center gap-1 hover:text-gray-900"
							on:click={() => dispatch('sort', col.key)}
						>
							{col.label}
							{#if sortKey === col.key}
								{#if sortDir === 'asc'}<ChevronUp size={14} />{:else}<ChevronDown size={14} />{/if}
							{/if}
						</button>
					</th>
				{/each}
				<th class="w-10" />
			</tr>
		</thead>
		<tbody>
			{#if loading}
				<tr>
					<td colspan="13" class="px-4 py-6">
						<Skeleton rows={8} cols={12} />
					</td>
				</tr>
			{:else if error}
				<tr>
					<td colspan="13" class="px-4 py-12 text-center text-gray-500">
						<p class="text-red-500 font-medium">{error}</p>
						<p class="text-sm mt-1 text-gray-400">Employee list endpoint is not yet available on the backend.</p>
					</td>
				</tr>
			{:else if items.length === 0}
				<tr>
					<td colspan="13" class="px-4 py-12 text-center text-gray-500">
						<p class="font-medium">No employees found</p>
						<p class="text-xs mt-1">Try adjusting your filters or hire a new employee.</p>
					</td>
				</tr>
			{:else}
				{#each items as emp}
					<tr
						class="border-b border-gray-100 hover:bg-[#fdf4ef]/40 cursor-pointer transition-colors"
						on:click={() => dispatch('select', emp)}
					>
						<!-- Name -->
						<td class="px-4 py-2">
							<div class="font-semibold text-gray-900">{emp.last_name}</div>
							<div class="text-xs text-gray-500">{emp.first_name}</div>
						</td>
						<!-- Email -->
						<td class="px-4 py-3 text-sm text-gray-600">{emp.email}</td>

						<!-- EmployeeInfo fields -->
						<td class="px-4 py-2">
							<Badge variant="info">{emp.department ?? '—'}</Badge>
						</td>
						<td class="px-4 py-3 text-gray-600 capitalize">{emp.salary ?? '—'}</td>
						<td class="px-4 py-3 text-gray-700">
							{emp.years_at_company != null ? `${emp.years_at_company} yr` : '—'}
						</td>
						<td class="px-4 py-3 text-gray-700">{emp.avg_monthly_hours ?? '—'}</td>
						<td class="px-4 py-3 text-gray-700">{emp.active_projects ?? '—'}</td>
						<!-- Manager -->
						<td class="px-4 py-3 text-gray-600 text-xs">{emp.manager_email}</td>

						<!-- Attrition risk -->
						<td class="px-4 py-2">
							{#if emp.attrition_risk != null}
								<Badge variant={riskBadgeVariant(emp.attrition_risk)}>
									{riskLabel(emp.attrition_risk)}
								</Badge>
							{:else}
								<span class="text-gray-400">—</span>
							{/if}
						</td>


					</tr>
				{/each}
			{/if}
		</tbody>
	</table>
</div>
