<script lang="ts">
	import { onMount } from 'svelte';
	import { UserPlus, Search, SlidersHorizontal, RefreshCw } from 'lucide-svelte';
	import Card from '$lib/components/ui/Card.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import EmployeesTable from '$lib/components/tables/EmployeesTable.svelte';
	import NewHireModal from '$lib/components/modals/NewHireModal.svelte';
	import EmployeeDetailModal from '$lib/components/modals/EmployeeDetailModal.svelte';
	import {
		employeeStore,
		fetchEmployees,
		setEmployeeFilter,
		filterEmployees,
		refreshRiskScores
	} from '$lib/stores/employees';
	import Pagination from '$lib/components/ui/Pagination.svelte';
	import type { Department, FullEmployee } from '$lib/types';

	onMount(() => {
		fetchEmployees();
	});

	let showNewHire = false;
	let showEmployeeDetail = false;
	let selectedEmployee: FullEmployee | null = null;
	let showFilters = false;
	let refreshing = false;

	let sortKey: keyof FullEmployee = 'last_name';
	let sortDir: 'asc' | 'desc' = 'asc';

	function handleSort(e: CustomEvent<keyof FullEmployee>) {
		const key = e.detail;
		if (sortKey === key) {
			sortDir = sortDir === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortDir = 'asc';
		}
		employeeStore.update((s) => ({ ...s, page: 1 }));
	}

	async function handleRefreshRisk() {
		refreshing = true;
		await refreshRiskScores();
		refreshing = false;
	}

	$: store = $employeeStore;
	$: filtered = filterEmployees(store.items, store.filters);
	$: sortedFiltered = [...filtered].sort((a, b) => {
		const av = a[sortKey] ?? '';
		const bv = b[sortKey] ?? '';
		const cmp = String(av).localeCompare(String(bv), undefined, { numeric: true });
		return sortDir === 'asc' ? cmp : -cmp;
	});
	$: displayed = sortedFiltered.slice((store.page - 1) * store.pageSize, store.page * store.pageSize);
	$: totalPages = Math.max(1, Math.ceil(filtered.length / store.pageSize));

	const deptOptions: { value: Department | ''; label: string }[] = [
		{ value: '', label: 'All departments' },
		{ value: 'accounting', label: 'Accounting' },
		{ value: 'engineering', label: 'Engineering' },
		{ value: 'hr', label: 'HR' },
		{ value: 'IT', label: 'IT' },
		{ value: 'management', label: 'Management' },
		{ value: 'marketing', label: 'Marketing' },
		{ value: 'product_management', label: 'Product Management' },
		{ value: 'r&d', label: 'R&D' },
		{ value: 'sales', label: 'Sales' },
		{ value: 'support', label: 'Support' }
	];

	function handleSearchInput(e: Event) {
		setEmployeeFilter({ search: (e.target as HTMLInputElement).value });
	}

	function handleDeptChange(e: Event) {
		setEmployeeFilter({ department: (e.target as HTMLSelectElement).value as Department | '' });
	}

	function handleRiskMinInput(e: Event) {
		setEmployeeFilter({ attritionRiskMin: parseFloat((e.target as HTMLInputElement).value) });
	}

	function handleRiskMaxInput(e: Event) {
		setEmployeeFilter({ attritionRiskMax: parseFloat((e.target as HTMLInputElement).value) });
	}
</script>

<svelte:head>
	<title>Employees — HR Hub</title>
</svelte:head>

<div class="flex flex-col h-full">
<!-- Page header -->
<div class="flex items-center justify-between mb-6 shrink-0">
	<div>
		<h2 class="text-xl font-semibold text-gray-900">Employees</h2>
		<p class="text-sm text-gray-500 mt-0.5">
			{#if store.loading}Loading…{:else}{filtered.length} employees{/if}
		</p>
	</div>
	<div class="flex gap-2">
		<Button variant="secondary" size="sm" on:click={() => (showFilters = !showFilters)}>
			<SlidersHorizontal size={15} />
			Filters
		</Button>
		<Button variant="secondary" size="sm" on:click={handleRefreshRisk} loading={refreshing} disabled={refreshing}>
			<RefreshCw size={15} />
			Score All
		</Button>
		<Button variant="primary" size="sm" on:click={() => (showNewHire = true)}>
			<UserPlus size={15} />
			New Hire
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
				placeholder="Search by name or email…"
				value={store.filters.search}
				on:input={handleSearchInput}
				class="w-full pl-9 pr-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C05B28]-500"
			/>
		</div>

		{#if showFilters}
			<div class="grid grid-cols-2 md:grid-cols-3 gap-3 pt-2 border-t border-gray-100">
				<Select
					id="deptFilter"
					label="Department"
					value={store.filters.department}
					options={deptOptions}
					on:change={handleDeptChange}
				/>
				<div class="flex flex-col gap-1">
					<label for="riskMin" class="text-sm font-medium text-gray-700">Min Attrition Risk</label>
					<input
						id="riskMin"
						type="range"
						min="0"
						max="1"
						step="0.05"
						value={store.filters.attritionRiskMin}
						on:input={handleRiskMinInput}
						class="accent-[#C05B28]"
					/>
					<span class="text-xs text-gray-500">{Math.round(store.filters.attritionRiskMin * 100)}%</span>
				</div>
				<div class="flex flex-col gap-1">
					<label for="riskMax" class="text-sm font-medium text-gray-700">Max Attrition Risk</label>
					<input
						id="riskMax"
						type="range"
						min="0"
						max="1"
						step="0.05"
						value={store.filters.attritionRiskMax}
						on:input={handleRiskMaxInput}
						class="accent-[#C05B28]"
					/>
					<span class="text-xs text-gray-500">{Math.round(store.filters.attritionRiskMax * 100)}%</span>
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
			on:first={() => employeeStore.update((s) => ({ ...s, page: 1 }))}
			on:prev={() => employeeStore.update((s) => ({ ...s, page: s.page - 1 }))}
			on:next={() => employeeStore.update((s) => ({ ...s, page: s.page + 1 }))}
			on:last={() => employeeStore.update((s) => ({ ...s, page: totalPages }))}
		/>
	{/if}
	<div class="flex-1 min-h-0">
		<EmployeesTable
			items={displayed}
			loading={store.loading}
			error={store.error}
			{sortKey}
			{sortDir}
			on:sort={handleSort}
			on:select={(e) => { selectedEmployee = e.detail; showEmployeeDetail = true; }}
		/>
	</div>
	{#if !store.loading && filtered.length > store.pageSize}
		<Pagination
			position="bottom"
			page={store.page}
			{totalPages}
			totalItems={filtered.length}
			pageSize={store.pageSize}
			on:first={() => employeeStore.update((s) => ({ ...s, page: 1 }))}
			on:prev={() => employeeStore.update((s) => ({ ...s, page: s.page - 1 }))}
			on:next={() => employeeStore.update((s) => ({ ...s, page: s.page + 1 }))}
			on:last={() => employeeStore.update((s) => ({ ...s, page: totalPages }))}
		/>
	{/if}
</Card>
</div>

<!-- Modals -->
<NewHireModal bind:open={showNewHire} on:close={() => (showNewHire = false)} />

<EmployeeDetailModal
	bind:open={showEmployeeDetail}
	employee={selectedEmployee}
	on:close={() => { showEmployeeDetail = false; selectedEmployee = null; }}
/>
