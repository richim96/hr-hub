<script lang="ts">
	export let value: string = '';
	export let label = '';
	export let id = '';
	export let required = false;
	export let disabled = false;
	export let error = '';
	export let placeholder = 'Select…';

	// options: array of { value: string; label: string }
	export let options: { value: string; label: string }[] = [];
</script>

<div class="flex flex-col gap-1">
	{#if label}
		<label for={id} class="text-sm font-medium text-gray-700">
			{label}{#if required}<span class="text-red-500 ml-0.5">*</span>{/if}
		</label>
	{/if}
	<select
		{id}
		{required}
		{disabled}
		bind:value
		class="w-full px-3 py-2 text-sm bg-white border rounded-lg shadow-sm transition-colors
			   focus:outline-none focus:ring-2 focus:ring-[#C05B28]-500 focus:border-transparent
			   disabled:bg-gray-50 disabled:text-gray-400
			   {error ? 'border-red-400' : 'border-gray-300'}"
		on:change
		{...$$restProps}
	>
		<option value="">{placeholder}</option>
		{#each options as opt}
			<option value={opt.value}>{opt.label}</option>
		{/each}
	</select>
	{#if error}
		<p class="text-xs text-red-600">{error}</p>
	{/if}
</div>
