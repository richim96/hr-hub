<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Badge from '$lib/components/ui/Badge.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import { changeEmployee } from '$lib/stores/employees';
	import type { ChangeField, EmployeeChangeRequest, EmployeeField, FullEmployee } from '$lib/types';

	export let open = false;
	export let employee: FullEmployee | null = null;

	const dispatch = createEventDispatcher<{ close: void }>();

	let editing = false;
	let submitting = false;

	// Editable shadow copies
	let editFirstName = '';
	let editLastName = '';
	let editManagerEmail = '';

	function startEdit() {
		if (!employee) return;
		editFirstName = employee.first_name;
		editLastName = employee.last_name;
		editManagerEmail = employee.manager_email;
		editing = true;
	}

	async function saveEdit() {
		if (!employee) return;
		submitting = true;
		const changes: Partial<Record<EmployeeField, ChangeField>> = {};

		if (editFirstName !== employee.first_name)
			changes.first_name = { from_value: employee.first_name, to: editFirstName };
		if (editLastName !== employee.last_name)
			changes.last_name = { from_value: employee.last_name, to: editLastName };
		if (editManagerEmail !== employee.manager_email)
			changes.manager = { from_value: employee.manager_email, to: editManagerEmail };

		if (Object.keys(changes).length === 0) {
			editing = false;
			submitting = false;
			return;
		}

		const payload: EmployeeChangeRequest = {
			request_id: `req_${crypto.randomUUID()}`,
			request_type: 'employee_change',
			employee_email: employee.email,
			changes,
			effective_date: new Date().toISOString().split('T')[0]
		};

		await changeEmployee(payload);
		submitting = false;
		editing = false;
		dispatch('close');
	}

	function riskClass(risk: number | null | undefined) {
		if (risk == null) return 'text-gray-400';
		if (risk >= 0.7) return 'text-red-600 font-semibold';
		if (risk >= 0.4) return 'text-[#C05B28]';
		return 'text-green-600';
	}

	function pct(v: number | null | undefined) {
		return v != null ? `${Math.round(v * 100)}%` : '—';
	}
</script>

<Modal {open} title="Employee Details" maxWidth="2xl" on:close={() => dispatch('close')}>
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
					<h3 class="text-lg font-semibold text-gray-900">
						{employee.first_name}
						{employee.last_name}
					</h3>
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
				<div class="space-y-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
					<p class="text-sm font-medium text-gray-700">Edit Employee</p>
					<div class="grid grid-cols-2 gap-4">
						<Input id="editFirst" label="First Name" bind:value={editFirstName} />
						<Input id="editLast" label="Last Name" bind:value={editLastName} />
					</div>
					<Input
						id="editManager"
						type="email"
						label="Manager Email"
						bind:value={editManagerEmail}
					/>
				</div>
			{:else}
				<!-- View mode: two-column info grid -->
				<div class="grid grid-cols-2 gap-x-8 gap-y-3 text-sm">
					<div>
						<span class="text-gray-500">Employee ID</span>
						<p class="font-mono text-gray-900 text-xs mt-0.5">{employee.employee_id}</p>
					</div>
					<div>
						<span class="text-gray-500">Manager</span>
						<p class="text-gray-900 mt-0.5">{employee.manager_email}</p>
					</div>
					<div>
						<span class="text-gray-500">Gender</span>
						<p class="text-gray-900 mt-0.5">{employee.gender ?? '—'}</p>
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
						<span class="text-gray-500">Last Evaluation</span>
						<p class="text-gray-900 mt-0.5">{pct(employee.last_evaluation)}</p>
					</div>
					<div>
						<span class="text-gray-500">Satisfaction</span>
						<p class="text-gray-900 mt-0.5">{pct(employee.satisfaction_score)}</p>
					</div>
					<div>
						<span class="text-gray-500">Attrition Risk</span>
						<p class={`mt-0.5 ${riskClass(employee.attrition_risk)}`}>
							{pct(employee.attrition_risk)}
						</p>
					</div>
					<div>
						<span class="text-gray-500">Work Accidents</span>
						<p class="text-gray-900 mt-0.5">{employee.work_accidents ? 'Yes' : employee.work_accidents === false ? 'No' : '—'}</p>
					</div>
				</div>

				<!-- Equipment -->
				<div class="pt-4 border-t border-gray-100">
					<p class="text-sm font-medium text-gray-700 mb-2">Equipment</p>
					<div class="flex gap-4 text-sm text-gray-700">
						<span>💻 {employee.laptop ?? '—'}</span>
						<span>🖥 Monitor: {employee.monitor ? 'Yes' : 'No'}</span>
						<span>🎧 Headset: {employee.headset ? 'Yes' : 'No'}</span>
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
			<Button variant="primary" on:click={startEdit}>Edit</Button>
		{/if}
	</svelte:fragment>
</Modal>
