<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import Modal from '$lib/components/ui/Modal.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Select from '$lib/components/ui/Select.svelte';
	import { hireEmployee } from '$lib/stores/employees';
	import type { Department, EmployeeEquipment, EmployeeInfo, Gender, NewHireRequest, SalaryTier } from '$lib/types';

	export let open = false;

	const dispatch = createEventDispatcher<{ close: void }>();

	// Form state
	let firstName = '';
	let lastName = '';
	let email = '';
	let managerEmail = '';
	let gender: Gender | '' = '';
	let department: Department | '' = '';
	let salary: SalaryTier | '' = '';
	let laptop = '';
	let monitor = false;
	let headset = false;
	let submitting = false;
	let errors: Record<string, string> = {};

	const deptOptions: { value: Department; label: string }[] = [
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

	function validate(): boolean {
		errors = {};
		if (!firstName.trim()) errors.firstName = 'Required';
		if (!lastName.trim()) errors.lastName = 'Required';
		if (!email.trim() || !email.includes('@')) errors.email = 'Valid email required';
		if (!managerEmail.trim() || !managerEmail.includes('@'))
			errors.managerEmail = 'Valid email required';
		if (!department) errors.department = 'Required';
		return Object.keys(errors).length === 0;
	}

	async function handleSubmit() {
		if (!validate()) return;
		submitting = true;

		const payload: NewHireRequest = {
			request_id: `req_${crypto.randomUUID()}`,
			request_type: 'new_hire',
			employee: {
				employee_id: `emp_${crypto.randomUUID().split('-')[0]}`,
				first_name: firstName,
				last_name: lastName,
				email,
				manager_email: managerEmail,
				gender: (gender as Gender) || null
			},
			equipment: {
				laptop: laptop || null,
				monitor,
				headset
			},
			info: {
				department: department as Department,
				salary: (salary as SalaryTier) || null
			}
		};

		const ok = await hireEmployee(payload);
		submitting = false;
		if (ok) {
			reset();
			dispatch('close');
		}
	}

	function reset() {
		firstName = lastName = email = managerEmail = laptop = '';
		gender = '';
		department = '';
		salary = '';
		monitor = headset = false;
		errors = {};
	}

	function handleClose() {
		reset();
		dispatch('close');
	}
</script>

<Modal {open} title="New Hire" maxWidth="xl" on:close={handleClose}>
	<form on:submit|preventDefault={handleSubmit} class="space-y-6">
		<!-- Employee details -->
		<fieldset class="space-y-4">
			<legend class="text-sm font-semibold text-gray-700 border-b pb-1 w-full">Employee Details</legend>
			<div class="grid grid-cols-2 gap-4">
				<Input id="firstName" label="First Name" bind:value={firstName} required error={errors.firstName} placeholder="Jane" />
				<Input id="lastName" label="Last Name" bind:value={lastName} required error={errors.lastName} placeholder="Smith" />
			</div>
			<Input id="email" type="email" label="Work Email" bind:value={email} required error={errors.email} placeholder="jane.smith@company.com" />
			<Input id="managerEmail" type="email" label="Manager Email" bind:value={managerEmail} required error={errors.managerEmail} placeholder="manager@company.com" />
			<Select id="gender" label="Gender" bind:value={gender} options={genderOptions} placeholder="Select gender…" />
		</fieldset>

		<!-- Role & compensation -->
		<fieldset class="space-y-4">
			<legend class="text-sm font-semibold text-gray-700 border-b pb-1 w-full">Role & Compensation</legend>
			<div class="grid grid-cols-2 gap-4">
				<Select
					id="department"
					label="Department"
					bind:value={department}
					options={deptOptions}
					required
					error={errors.department}
					placeholder="Select department…"
				/>
				<Select id="salary" label="Salary Tier" bind:value={salary} options={salaryOptions} placeholder="Select tier…" />
			</div>
		</fieldset>

		<!-- Equipment -->
		<fieldset class="space-y-4">
			<legend class="text-sm font-semibold text-gray-700 border-b pb-1 w-full">Equipment</legend>
			<Input id="laptop" label="Laptop Model" bind:value={laptop} placeholder='MacBook Pro 14"' />
			<div class="flex gap-6">
				<label class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
					<input type="checkbox" bind:checked={monitor} class="rounded border-gray-300 text-[#C05B28]" />
					Monitor
				</label>
				<label class="flex items-center gap-2 text-sm text-gray-700 cursor-pointer">
					<input type="checkbox" bind:checked={headset} class="rounded border-gray-300 text-[#C05B28]" />
					Headset
				</label>
			</div>
		</fieldset>
	</form>

	<svelte:fragment slot="footer">
		<Button variant="secondary" on:click={handleClose} disabled={submitting}>Cancel</Button>
		<Button variant="primary" on:click={handleSubmit} loading={submitting}>
			Create Employee
		</Button>
	</svelte:fragment>
</Modal>
