<script lang="ts">
	import { onMount } from 'svelte';
	import { UserPlus, Search, SlidersHorizontal } from 'lucide-svelte';
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
		filterEmployees
	} from '$lib/stores/employees';
	import type { Department, FullEmployee } from '$lib/types';

	onMount(() => {
		fetchEmployees();
	});

	let showNewHire = false;
	let showEmployeeDetail = false;
	let selectedEmployee: FullEmployee | null = null;
	let showFilters = false;

	$: store = $employeeStore;
	$: filtered = filterEmployees(store.items, store.filters);
	$: displayed = filtered.slice((store.page - 1) * store.pageSize, store.page * store.pageSize);
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

<!-- Page header -->
<div class="flex items-center justify-between mb-6">
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
		<Button variant="primary" size="sm" on:click={() => (showNewHire = true)}>
			<UserPlus size={15} />
			New Hire
		</Button>
	</div>
</div>

<!-- Search + filter bar -->
<Card padding="sm" class="mb-4">
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
					<label class="text-sm font-medium text-gray-700">Min Attrition Risk</label>
					<input
						type="range"
						min="0"
						max="1"
						step="0.05"
						value={store.filters.attritionRiskMin}
						on:input={handleRiskMinInput}
						class="accent-[#C05B28]-600"
					/>
					<span class="text-xs text-gray-500">{Math.round(store.filters.attritionRiskMin * 100)}%</span>
				</div>
				<div class="flex flex-col gap-1">
					<label class="text-sm font-medium text-gray-700">Max Attrition Risk</label>
					<input
						type="range"
						min="0"
						max="1"
						step="0.05"
						value={store.filters.attritionRiskMax}
						on:input={handleRiskMaxInput}
						class="accent-[#C05B28]-600"
					/>
					<span class="text-xs text-gray-500">{Math.round(store.filters.attritionRiskMax * 100)}%</span>
				</div>
			</div>
		{/if}
	</div>
</Card>

<!-- Table -->
<Card padding="none">
	<EmployeesTable
		items={displayed}
		loading={store.loading}
		error={store.error}
		on:select={(e) => { selectedEmployee = e.detail; showEmployeeDetail = true; }}
	/>

	<!-- Pagination -->
	{#if !store.loading && filtered.length > store.pageSize}
		<div class="flex items-center justify-between px-4 py-3 border-t border-gray-100 text-sm text-gray-600">
			<span>
				{(store.page - 1) * store.pageSize + 1}–{Math.min(
					store.page * store.pageSize,
					filtered.length
				)} of {filtered.length}
			</span>
			<div class="flex gap-2">
				<Button
					variant="ghost"
					size="sm"
					disabled={store.page <= 1}
					on:click={() => employeeStore.update((s) => ({ ...s, page: s.page - 1 }))}
				>
					Previous
				</Button>
				<Button
					variant="ghost"
					size="sm"
					disabled={store.page >= totalPages}
					on:click={() => employeeStore.update((s) => ({ ...s, page: s.page + 1 }))}
				>
					Next
				</Button>
			</div>
		</div>
	{/if}
</Card>

<!-- Modals -->
<NewHireModal bind:open={showNewHire} on:close={() => (showNewHire = false)} />

<EmployeeDetailModal
	bind:open={showEmployeeDetail}
	employee={selectedEmployee}
	on:close={() => { showEmployeeDetail = false; selectedEmployee = null; }}
/>
