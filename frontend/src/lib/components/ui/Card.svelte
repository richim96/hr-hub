<script lang="ts">
	export let padding: 'none' | 'sm' | 'md' | 'lg' = 'md';
	let extraClass = '';
	export { extraClass as class };
	const paddings = { none: '', sm: 'p-4', md: 'p-6', lg: 'p-8' };
</script>

<div class="bg-white rounded-xl border border-gray-200 shadow-sm {paddings[padding]} {extraClass}">
	<slot />
</div>
