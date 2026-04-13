<script lang="ts">
	export let value: string | number = '';
	export let type = 'text';
	export let placeholder = '';
	export let label = '';
	export let error = '';
	export let id = '';
	export let required = false;
	export let disabled = false;

	function handleInput(e: Event) {
		value = (e.target as HTMLInputElement).value;
	}
</script>

<div class="flex flex-col gap-1">
	{#if label}
		<label for={id} class="text-sm font-medium text-gray-700">
			{label}{#if required}<span class="text-red-500 ml-0.5">*</span>{/if}
		</label>
	{/if}
	<input
		{id}
		{type}
		{placeholder}
		{required}
		{disabled}
		value={value}
		on:input={handleInput}
		on:change
		on:blur
		class="w-full px-3 py-2 text-sm bg-white border rounded-lg shadow-sm transition-colors
			   focus:outline-none focus:ring-2 focus:ring-[#C05B28]-500 focus:border-transparent
			   disabled:bg-gray-50 disabled:text-gray-400
			   {error ? 'border-red-400' : 'border-gray-300'}"
		{...$$restProps}
	/>
	{#if error}
		<p class="text-xs text-red-600">{error}</p>
	{/if}
</div>
