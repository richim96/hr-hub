<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { Pencil, Trash2 } from 'lucide-svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import ConfirmModal from '$lib/components/ui/ConfirmModal.svelte';
	import { changeEmployee, removeEmployee } from '$lib/stores/employees';
	import type { Department, FullEmployee, Gender, SalaryTier, UpdateEmployeeRequest } from '$lib/types';

	export let open = false;
	export let employee: FullEmployee | null = null;

	const dispatch = createEventDispatcher<{ close: void }>();

	let editing = false;
	let submitting = false;
	let confirmOpen = false;

	// --- Edit shadow copies ---
	let editFirstName = '';
	let editLastName = '';
	let editGender: Gender | '' = '';
	let editEmail = '';
	let editManagerEmail = '';
	let editLaptop = '';
	let editMonitor = false;
	let editHeadset = false;
	let editDepartment: Department | '' = '';
	let editSalary: SalaryTier | '' = '';
	let editActiveProjects = '';
	let editAvgMonthlyHours = '';
	let editYearsAtCompany = '';
	let editWorkAccidents = false;
	let editReceivedPromotion = false;
	let editLastEvaluation = '';
	let editSatisfactionScore = '';

	const deptOptions = [
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

	const salaryOptions = [
		{ value: 'low', label: 'Low' },
		{ value: 'medium', label: 'Medium' },
		{ value: 'high', label: 'High' }
	];

	const genderOptions = [
		{ value: 'M', label: 'Male' },
		{ value: 'F', label: 'Female' }
	];

	function startEdit() {
		if (!employee) return;
		editFirstName = employee.first_name;
		editLastName = employee.last_name;
		editGender = employee.gender ?? '';
		editEmail = employee.email;
		editManagerEmail = employee.manager_email ?? '';
		editLaptop = employee.laptop ?? '';
		editMonitor = employee.monitor ?? false;
		editHeadset = employee.headset ?? false;
		editDepartment = employee.department;
		editSalary = employee.salary;
		editActiveProjects = employee.active_projects != null ? String(employee.active_projects) : '';
		editAvgMonthlyHours = employee.avg_monthly_hours != null ? String(employee.avg_monthly_hours) : '';
		editYearsAtCompany = employee.years_at_company != null ? String(employee.years_at_company) : '';
		editWorkAccidents = employee.work_accidents ?? false;
		editReceivedPromotion = employee.received_promotion ?? false;
		editLastEvaluation = employee.last_evaluation != null ? String(Math.round(employee.last_evaluation * 100)) : '';
		editSatisfactionScore = employee.satisfaction_score != null ? String(Math.round(employee.satisfaction_score * 100)) : '';
		editing = true;
	}

	async function saveEdit() {
		if (!employee) return;
		submitting = true;

		const payload: UpdateEmployeeRequest = {};

		if (editFirstName !== employee.first_name) payload.first_name = editFirstName;
		if (editLastName !== employee.last_name) payload.last_name = editLastName;

		const newGender = (editGender as Gender) || null;
		if (newGender !== (employee.gender ?? null)) payload.gender = newGender;

		if (editEmail !== employee.email) payload.email = editEmail;

		const newManager = editManagerEmail || null;
		if (newManager !== (employee.manager_email ?? null)) payload.manager_email = newManager;

		const newLaptop = editLaptop || null;
		if (newLaptop !== (employee.laptop ?? null)) payload.laptop = newLaptop;
		if (editMonitor !== (employee.monitor ?? false)) payload.monitor = editMonitor;
		if (editHeadset !== (employee.headset ?? false)) payload.headset = editHeadset;

		if (editDepartment && editDepartment !== employee.department)
			payload.department = editDepartment as Department;
		if (editSalary && editSalary !== employee.salary)
			payload.salary = editSalary as SalaryTier;

		const newActiveProjects = editActiveProjects !== '' ? parseInt(editActiveProjects) : null;
		if (newActiveProjects !== (employee.active_projects ?? null)) payload.active_projects = newActiveProjects;

		const newAvgMonthlyHours = editAvgMonthlyHours !== '' ? parseInt(editAvgMonthlyHours) : null;
		if (newAvgMonthlyHours !== (employee.avg_monthly_hours ?? null)) payload.avg_monthly_hours = newAvgMonthlyHours;

		const newYearsAtCompany = editYearsAtCompany !== '' ? parseInt(editYearsAtCompany) : null;
		if (newYearsAtCompany !== (employee.years_at_company ?? null)) payload.years_at_company = newYearsAtCompany;

		if (editWorkAccidents !== (employee.work_accidents ?? false)) payload.work_accidents = editWorkAccidents;
		if (editReceivedPromotion !== (employee.received_promotion ?? false)) payload.received_promotion = editReceivedPromotion;

		const newLastEval = editLastEvaluation !== '' ? parseFloat(editLastEvaluation) / 100 : null;
		if (newLastEval !== (employee.last_evaluation ?? null)) payload.last_evaluation = newLastEval;

		const newSatisfaction = editSatisfactionScore !== '' ? parseFloat(editSatisfactionScore) / 100 : null;
		if (newSatisfaction !== (employee.satisfaction_score ?? null)) payload.satisfaction_score = newSatisfaction;

		if (Object.keys(payload).length === 0) {
			editing = false;
			submitting = false;
			return;
		}

		await changeEmployee(employee.employee_id, payload);
		submitting = false;
		editing = false;
		dispatch('close');
	}

	async function confirmDelete() {
		if (!employee) return;
		submitting = true;
		await removeEmployee(employee.employee_id);
		submitting = false;
		confirmOpen = false;
		dispatch('close');
	}

	function riskBadgeVariant(risk: number | null | undefined): 'failed' | 'pending' | 'completed' | 'default' {
		if (risk == null) return 'default';
		if (risk >= 0.7) return 'failed';
		if (risk >= 0.4) return 'pending';
		return 'completed';
	}

	function pct(v: number | null | undefined) {
		return v != null ? `${Math.round(v * 100)}%` : '—';
	}

	function boolLabel(v: boolean | null | undefined) {
		if (v == null) return '—';
		return v ? 'Yes' : 'No';
	}
</script>

<Modal {open} maxWidth="2xl" on:close={() => dispatch('close')}>
	<svelte:fragment slot="title">
		{#if employee}
			{employee.first_name} {employee.last_name}
			{#if !editing}
				<button
					class="p-1 rounded text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
					on:click={startEdit}
					aria-label="Edit employee"
				>
					<Pencil size={14} />
				</button>
				<button
					class="p-1 rounded text-red-400 hover:text-red-600 hover:bg-red-50 transition-colors"
					on:click={() => (confirmOpen = true)}
					aria-label="Delete employee"
				>
					<Trash2 size={14} />
				</button>
			{/if}
		{/if}
	</svelte:fragment>

	{#if employee}
		<div class="space-y-6">
			<!-- Identity -->
			<div class="flex items-start gap-4">
				<div
					class="w-12 h-12 rounded-full bg-[#f5ddd0] text-[#9a3d1a] flex items-center justify-center text-lg font-bold shrink-0"
				>
					{employee.first_name[0]}{employee.last_name[0]}
				</div>
				<div>
					<p class="text-sm text-gray-500">{employee.email}</p>
					<div class="flex items-center gap-2 mt-1">
						<Badge variant="info">{employee.department ?? '—'}</Badge>
						{#if employee.salary}
							<Badge variant="default">{employee.salary} salary</Badge>
						{/if}
					</div>
				</div>
			</div>

			{#if editing}
				<!-- Edit mode -->
				<div class="space-y-5 max-h-[60vh] overflow-y-auto pr-1">
					<!-- Identity -->
					<fieldset class="space-y-3">
						<legend class="text-xs font-semibold uppercase tracking-wide text-gray-400 pb-1 border-b border-gray-100 w-full">Identity</legend>
						<div class="grid grid-cols-2 gap-3">
							<Input id="editFirst" label="First Name" bind:value={editFirstName} />
							<Input id="editLast" label="Last Name" bind:value={editLastName} />
						</div>
						<div class="grid grid-cols-2 gap-3">
							<Input id="editEmail" type="email" label="Email" bind:value={editEmail} />
							<Input id="editManager" type="email" label="Manager Email" bind:value={editManagerEmail} />
						</div>
						<Select id="editGender" label="Gender" bind:value={editGender} options={genderOptions} placeholder="Select gender…" />
					</fieldset>

					<!-- Equipment -->
					<fieldset class="space-y-3">
						<legend class="text-xs font-semibold uppercase tracking-wide text-gray-400 pb-1 border-b border-gray-100 w-full">Equipment</legend>
						<Input id="editLaptop" label="Laptop Model" bind:value={editLaptop} placeholder='MacBook Pro 14"' />
						<div class="flex gap-6">
							<label class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
								<input type="checkbox" bind:checked={editMonitor} class="rounded border-gray-300" />
								Monitor
							</label>
							<label class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
								<input type="checkbox" bind:checked={editHeadset} class="rounded border-gray-300" />
								Headset
							</label>
						</div>
					</fieldset>

					<!-- Employment Info -->
					<fieldset class="space-y-3">
						<legend class="text-xs font-semibold uppercase tracking-wide text-gray-400 pb-1 border-b border-gray-100 w-full">Employment Info</legend>
						<div class="grid grid-cols-2 gap-3">
							<Select id="editDept" label="Department" bind:value={editDepartment} options={deptOptions} placeholder="Select department…" />
							<Select id="editSalary" label="Salary Tier" bind:value={editSalary} options={salaryOptions} placeholder="Select tier…" />
						</div>
						<div class="grid grid-cols-3 gap-3">
							<Input id="editProjects" type="number" label="Active Projects" bind:value={editActiveProjects} placeholder="0" />
							<Input id="editHours" type="number" label="Avg Monthly Hours" bind:value={editAvgMonthlyHours} placeholder="160" />
							<Input id="editYears" type="number" label="Years at Company" bind:value={editYearsAtCompany} placeholder="0" />
						</div>
						<div class="grid grid-cols-2 gap-3">
							<Input id="editLastEval" type="number" label="Last Evaluation (%)" bind:value={editLastEvaluation} placeholder="72" />
							<Input id="editSatisfaction" type="number" label="Satisfaction Score (%)" bind:value={editSatisfactionScore} placeholder="61" />
						</div>
						<div class="flex gap-6">
							<label class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
								<input type="checkbox" bind:checked={editWorkAccidents} class="rounded border-gray-300" />
								Work Accident
							</label>
							<label class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
								<input type="checkbox" bind:checked={editReceivedPromotion} class="rounded border-gray-300" />
								Received Promotion
							</label>
						</div>
					</fieldset>
				</div>
			{:else}
				<!-- View mode: two sections — Employee identity + EmployeeInfo -->
				<div class="space-y-4">
					<!-- Section: Employee -->
					<div>
						<p class="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-2">Identity</p>
						<div class="grid grid-cols-2 gap-x-8 gap-y-3 text-sm">
							<div>
								<span class="text-gray-500">Employee ID</span>
								<p class="font-mono text-gray-900 text-xs mt-0.5">{employee.employee_id}</p>
							</div>
							<div>
								<span class="text-gray-500">Gender</span>
								<p class="text-gray-900 mt-0.5">{employee.gender ?? '—'}</p>
							</div>
						</div>
					</div>

					<!-- Section: EmployeeInfo -->
					<div class="pt-3 border-t border-gray-100">
						<p class="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-2">Employment Info</p>
						<div class="grid grid-cols-2 gap-x-8 gap-y-3 text-sm">
							<div>
								<span class="text-gray-500">Manager</span>
								<p class="text-gray-900 mt-0.5">{employee.manager_email ?? '—'}</p>
							</div>
							<div>
								<span class="text-gray-500">Years at Company</span>
								<p class="text-gray-900 mt-0.5">{employee.years_at_company ?? '—'}</p>
							</div>
							<div>
								<span class="text-gray-500">Avg Monthly Hours</span>
								<p class="text-gray-900 mt-0.5">{employee.avg_monthly_hours ?? '—'}</p>
							</div>
							<div>
								<span class="text-gray-500">Active Projects</span>
								<p class="text-gray-900 mt-0.5">{employee.active_projects ?? '—'}</p>
							</div>
							<div>
								<span class="text-gray-500">Received Promotion</span>
								<p class="text-gray-900 mt-0.5">{boolLabel(employee.received_promotion)}</p>
							</div>
							<div>
								<span class="text-gray-500">Work Accidents</span>
								<p class="text-gray-900 mt-0.5">{boolLabel(employee.work_accidents)}</p>
							</div>
							<div>
								<span class="text-gray-500">Last Evaluation</span>
								<p class="text-gray-900 mt-0.5">{pct(employee.last_evaluation)}</p>
							</div>
							<div>
								<span class="text-gray-500">Satisfaction Score</span>
								<p class="text-gray-900 mt-0.5">{pct(employee.satisfaction_score)}</p>
							</div>
						</div>
					</div>

					<!-- Section: Attrition Risk -->
					<div class="pt-3 border-t border-gray-100">
						<p class="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-2">Attrition Risk</p>
						{#if employee.attrition_risk != null}
							<div class="flex items-center gap-3">
								<div class="flex-1 bg-gray-100 rounded-full h-2">
									<div
										class="h-2 rounded-full transition-all {employee.attrition_risk >= 0.7 ? 'bg-red-500' : employee.attrition_risk >= 0.4 ? 'bg-amber-400' : 'bg-green-500'}"
										style="width: {Math.round(employee.attrition_risk * 100)}%"
									/>
								</div>
								<Badge variant={riskBadgeVariant(employee.attrition_risk)}>
									{pct(employee.attrition_risk)}
								</Badge>
							</div>
						{:else}
							<p class="text-sm text-gray-400 italic">Not scored yet — use "Score Risk" to run the prediction model.</p>
						{/if}
					</div>

					<!-- Section: Equipment -->
					<div class="pt-3 border-t border-gray-100">
						<p class="text-xs font-semibold uppercase tracking-wide text-gray-400 mb-2">Equipment</p>
						<div class="flex gap-4 text-sm text-gray-700">
							<span>💻 {employee.laptop ?? '—'}</span>
							<span>🖥 Monitor: {boolLabel(employee.monitor)}</span>
							<span>🎧 Headset: {boolLabel(employee.headset)}</span>
						</div>
					</div>
				</div>
			{/if}
		</div>
	{/if}

	<svelte:fragment slot="footer">
		{#if editing}
			<Button variant="secondary" on:click={() => (editing = false)} disabled={submitting}>
				Cancel
			</Button>
			<Button variant="primary" on:click={saveEdit} loading={submitting}>Save Changes</Button>
		{:else}
			<Button variant="secondary" on:click={() => dispatch('close')}>Close</Button>
		{/if}
	</svelte:fragment>
</Modal>

<ConfirmModal
	open={confirmOpen}
	title="Delete Employee"
	message="Are you sure you want to delete this employee? This will also remove all their tasks and employment info."
	confirmLabel="Delete"
	loading={submitting}
	on:confirm={confirmDelete}
	on:cancel={() => (confirmOpen = false)}
/>
