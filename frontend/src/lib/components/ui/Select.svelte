<script lang="ts">
	export let value: string = '';
	export let label = '';
	export let id = '';
	export let required = false;
	export let disabled = false;
	export let error = '';
	export let placeholder = 'Select…';

	export let options: { value: string; label: string }[] = [];
</script>

<div class="flex flex-col gap-1">
	{#if label}
		<label for={id} class="text-sm font-medium text-gray-600">
			{label}{#if required}<span class="text-red-500 ml-0.5">*</span>{/if}
		</label>
	{/if}
	<select
		{id}
		{required}
		{disabled}
		bind:value
		class="w-full px-3 py-2 text-sm rounded-2xl transition-all
			   focus:outline-none focus:ring-2 focus:ring-[#C05B28]/50
			   disabled:opacity-50
			   {error ? 'ring-1 ring-red-400' : ''}"
		style="background: var(--glass-bg-input); backdrop-filter: var(--glass-blur-sm); -webkit-backdrop-filter: var(--glass-blur-sm); border: 1px solid {error ? 'rgba(248,113,113,0.6)' : 'var(--glass-border-subtle)'};"
		on:change
		{...$$restProps}
	>
		{#if !options.some(o => o.value === '')}
			<option value="">{placeholder}</option>
		{/if}
		{#each options as opt}
			<option value={opt.value}>{opt.label}</option>
		{/each}
	</select>
	{#if error}
		<p class="text-xs text-red-500">{error}</p>
	{/if}
</div>
